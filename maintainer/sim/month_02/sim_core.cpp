// Logic simulator for Month 2: a PIC18F47K42's pins RC3/RC4/RD0/RD3, an I2C bus,
// and an MCP23017 that follows the datasheet protocol (BANK=0, address 0x20).
//
// It checks LOGIC, not electronics: register values, I2C protocol sequence, button
// handling, timing against the I2C standard-mode limits. It cannot tell you whether
// your breadboard wiring is right or whether XC8 accepts the code.
#include "sim_core.h"
#include "xc.h"
#include <algorithm>
#include <cstdio>
#include <cstring>

Reg8 TRISC, TRISD, LATC, LATD, ANSELC, ANSELD, OSCFRQ;
Sim sim;

static const uint8_t SCL_MASK = 0x08, SDA_MASK = 0x10;     // RC3, RC4

// ---------- bus / slave state ----------
static int prev_scl = 1, prev_sdam = 1;
enum St { IDLE, RX, ACK, TX, MACK };
static St st = IDLE;
static int bits, shift_, byte_index, rw, slave_sda = 1, tx_byte, mack_ack;
static bool addressed, next_tx, next_rx;
static double t_scl_rise = -1, t_scl_fall = -1, t_sda_rise = -1, t_sda_change = -1, t_start = -1;
static int prev_led = 0, prev_piezo = 0;
static bool warned_drive_high = false;

struct Trans { uint64_t t; int idx; int state; };
static std::vector<Trans> trans;
static size_t trans_next = 0;

static void err(const std::string& s) {
    char buf[64]; snprintf(buf, sizeof buf, " [t=%.3f ms]", sim.now_us / 1000.0);
    if (sim.errors.size() < 20) sim.errors.push_back(s + buf);
}

static int line(uint8_t mask) {
    if (TRISC.v & mask) return 1;                    // released: pulled HIGH by 4.7k
    if (LATC.v & mask) {                             // driven HIGH: never do this on I2C
        if (!warned_drive_high) { warned_drive_high = true; err("MCU drove an I2C line HIGH"); }
        return 1;
    }
    return 0;
}

// ---------- MCP23017 ----------
static uint8_t pinsB() {
    uint8_t r = 0;
    for (int i = 0; i < 8; i++) {
        int level;
        if (sim.regs[0x01] & (1 << i)) {             // input
            if (sim.pressed_mask & (1 << i)) level = 0;
            else level = (sim.regs[0x0D] >> i) & 1;  // pull-up on -> 1; floating -> 0 (exposes a missing pull-up)
        } else level = (sim.regs[0x15] >> i) & 1;    // output
        r |= (uint8_t)(level << i);
    }
    return r;
}
static uint8_t pinsA() { return sim.regs[0x14] & (uint8_t)~sim.regs[0x00]; }

static uint8_t read_reg(int r) {
    uint8_t v;
    if (r == 0x12) v = pinsA();
    else if (r == 0x13) v = pinsB();
    else v = sim.regs[r];
    sim.reads_done++;
    if (sim.slave_corrupts_reads) v ^= 0x01;
    return v;
}
static void write_reg(int r, uint8_t v) {
    sim.regs[r] = v;
    if (r == 0x12) { sim.regs[0x14] = v; r = 0x14; }
    if (r == 0x14) sim.olata_events.push_back({sim.now_us, v});
    sim.writes_done++;
}

static void handle_byte() {
    bool ack = false; next_tx = next_rx = false;
    if (byte_index == 0) {
        if (sim.slave_present && (shift_ >> 1) == 0x20) {
            addressed = true; rw = shift_ & 1;
            if (rw && sim.slave_nacks_read_address) ack = false;
            else { ack = true; if (rw) next_tx = true; else next_rx = true; }
        } else addressed = false;
    } else if (addressed && rw == 0) {
        if (byte_index == 1) {
            sim.ptr = (uint8_t)shift_;
            if (sim.ptr >= 0x16) err("register pointer out of range");
        } else {
            write_reg(sim.ptr % 0x16, (uint8_t)shift_);
            sim.ptr = (uint8_t)((sim.ptr + 1) % 0x16);
        }
        ack = true; next_rx = true;
    }
    slave_sda = ack ? 0 : 1;
    byte_index++;
}
static void load_tx() { tx_byte = read_reg(sim.ptr % 0x16); sim.ptr = (uint8_t)((sim.ptr + 1) % 0x16); }

static void on_scl_rise(int sdam) {
    int bus = sdam & slave_sda;
    if (st == RX) { shift_ = ((shift_ << 1) | bus) & 0xFF; bits++; }
    else if (st == MACK) mack_ack = (bus == 0);
}
static void on_scl_fall() {
    switch (st) {
    case RX:   if (bits == 8) { handle_byte(); st = ACK; } break;
    case ACK:
        slave_sda = 1;
        if (next_tx) { load_tx(); st = TX; bits = 0; slave_sda = (tx_byte >> 7) & 1; }
        else if (next_rx) { st = RX; bits = 0; shift_ = 0; }
        else st = IDLE;
        break;
    case TX:
        bits++;
        if (bits == 8) { slave_sda = 1; st = MACK; }
        else slave_sda = (tx_byte >> (7 - bits)) & 1;
        break;
    case MACK:
        if (mack_ack) { load_tx(); st = TX; bits = 0; slave_sda = (tx_byte >> 7) & 1; }
        else { slave_sda = 1; st = IDLE; }
        break;
    default: break;
    }
}

static void bus_update() {
    int scl = line(SCL_MASK), sdam = line(SDA_MASK);
    double t = (double)sim.now_us;
    if (scl && prev_scl && sdam != prev_sdam) {
        if (prev_sdam == 1 && sdam == 0) {                       // START
            sim.min_start_setup = std::min(sim.min_start_setup, t - std::max(t_scl_rise, t_sda_rise));
            t_start = t; st = RX; bits = 0; shift_ = 0; byte_index = 0; addressed = false; slave_sda = 1;
        } else {                                                  // STOP
            sim.min_stop_setup = std::min(sim.min_stop_setup, t - t_scl_rise);
            st = IDLE; slave_sda = 1;
        }
    } else if (!prev_scl && scl) {                               // SCL rising
        if (t_scl_fall >= 0) sim.min_scl_low = std::min(sim.min_scl_low, t - t_scl_fall);
        if (t_sda_change >= 0) sim.min_data_setup = std::min(sim.min_data_setup, t - t_sda_change);
        t_scl_rise = t; on_scl_rise(sdam);
    } else if (prev_scl && !scl) {                               // SCL falling
        if (t_scl_rise >= 0) sim.min_scl_high = std::min(sim.min_scl_high, t - t_scl_rise);
        if (t_start >= 0) { sim.min_start_hold = std::min(sim.min_start_hold, t - t_start); t_start = -1; }
        t_scl_fall = t; on_scl_fall();
    }
    if (sdam != prev_sdam) { if (sdam) t_sda_rise = t; t_sda_change = t; }
    prev_scl = scl; prev_sdam = sdam;
}

void sim_reg_written() {
    bus_update();
    int led = (!(TRISD.v & 0x01)) && (LATD.v & 0x01);
    if (led != prev_led) { sim.led_events.push_back({sim.now_us, led}); prev_led = led; }
    int pz = (!(TRISD.v & 0x08)) && (LATD.v & 0x08);
    if (pz != prev_piezo) { sim.piezo_toggles++; prev_piezo = pz; }
}

uint8_t sim_portc() {
    uint8_t v = (uint8_t)(LATC.v & ~TRISC.v);
    if (line(SCL_MASK)) v |= SCL_MASK;
    if (line(SDA_MASK) && slave_sda) v |= SDA_MASK; else v &= (uint8_t)~SDA_MASK;
    return v;
}
uint8_t sim_portd() { return (uint8_t)(LATD.v & ~TRISD.v); }

void sim_delay_us(unsigned long us) {
    uint64_t target = sim.now_us + us;
    while (trans_next < trans.size() && trans[trans_next].t <= target) {
        sim.now_us = trans[trans_next].t;
        if (trans[trans_next].state) sim.pressed_mask |= (uint8_t)(1 << trans[trans_next].idx);
        else sim.pressed_mask &= (uint8_t)~(1 << trans[trans_next].idx);
        trans_next++;
    }
    sim.now_us = target;
    if (sim.now_us >= sim.end_us) throw SimEnd();
}

// ---------- Sim API ----------
void Sim::reset() {
    now_us = 0; slave_present = true; slave_corrupts_reads = false; slave_nacks_read_address = false;
    memset(regs, 0, sizeof regs); regs[0x00] = regs[0x01] = 0xFF; ptr = 0;
    pressed_mask = 0; presses.clear(); led_events.clear(); olata_events.clear();
    piezo_toggles = 0; reads_done = writes_done = 0; errors.clear();
    min_scl_low = min_scl_high = min_start_setup = min_start_hold = min_stop_setup = min_data_setup = 1e9;
    trans.clear(); trans_next = 0;
    TRISC.v = 0xFF; TRISD.v = 0xFF; LATC.v = LATD.v = 0; ANSELC.v = ANSELD.v = 0xFF; OSCFRQ.v = 0;
    prev_scl = prev_sdam = 1; st = IDLE; slave_sda = 1; prev_led = prev_piezo = 0; warned_drive_high = false;
    t_scl_rise = t_scl_fall = t_sda_rise = t_sda_change = t_start = -1;
}
void Sim::press(int idx, uint64_t down_ms, uint64_t up_ms, bool bounce) {
    uint64_t d = down_ms * 1000, u = up_ms * 1000;
    if (bounce) {           // contact bounce: a few ms of chatter on both edges
        uint64_t dd[] = {0, 400, 900, 1400, 2200}; int ds[] = {1, 0, 1, 0, 1};
        for (int i = 0; i < 5; i++) trans.push_back({d + dd[i], idx, ds[i]});
        uint64_t uu[] = {0, 500, 1100, 1900}; int us[] = {0, 1, 0, 1};
        for (int i = 0; i < 4; i++) trans.push_back({u + uu[i], idx, us[i]});
        trans.push_back({u + 3000, idx, 0});
    } else { trans.push_back({d, idx, 1}); trans.push_back({u, idx, 0}); }
    std::sort(trans.begin(), trans.end(), [](const Trans& a, const Trans& b) { return a.t < b.t; });
}
void Sim::run(void (*entry)(void), uint64_t duration_ms) {
    end_us = duration_ms * 1000;
    try { entry(); } catch (SimEnd&) {}
}
uint8_t Sim::ledsOn() const { return (uint8_t)(regs[0x14] & ~regs[0x00]); }
uint8_t Sim::lastOlata() const { return olata_events.empty() ? 0 : (uint8_t)olata_events.back().v; }
