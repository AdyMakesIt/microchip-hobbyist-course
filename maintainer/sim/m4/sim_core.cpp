// Logic simulator for Month 4: a PIC16F18446's pins RB4/RB6, RA2, port C LEDs, an I2C bus,
// and an MCP7940N real-time clock (address 0x6F).
//
// It checks LOGIC, not electronics: register values, I2C protocol sequence, button
// handling, timing against the I2C standard-mode limits. It cannot tell you whether
// your breadboard wiring is right or whether XC8 accepts the code.
#include "sim4.h"
#include "xc.h"
#include <algorithm>
#include <cstdio>
#include <cstring>

Reg8 TRISA, TRISB, TRISC, LATA, LATB, LATC, ANSELA, ANSELB, ANSELC, WPUA;
Sim sim;

static const uint8_t SCL_MASK = 0x40, SDA_MASK = 0x10;     // RB6, RB4

// ---------- bus / slave state ----------
static int prev_scl = 1, prev_sdam = 1;
enum St { IDLE, RX, ACK, TX, MACK };
static St st = IDLE;
static int bits, shift_, byte_index, rw, slave_sda = 1, tx_byte, mack_ack;
static bool addressed, next_tx, next_rx;
static double t_scl_rise = -1, t_scl_fall = -1, t_sda_rise = -1, t_sda_change = -1, t_start = -1;
static int prev_latc = 0;
static bool warned_drive_high = false;

struct Trans { uint64_t t; int idx; int state; };
static std::vector<Trans> trans;
static size_t trans_next = 0;

static void err(const std::string& s) {
    char buf[64]; snprintf(buf, sizeof buf, " [t=%.3f ms]", sim.now_us / 1000.0);
    if (sim.errors.size() < 20) sim.errors.push_back(s + buf);
}

static int line(uint8_t mask) {
    if (TRISB.v & mask) return 1;                    // released: pulled HIGH by 4.7k
    if (LATB.v & mask) {                             // driven HIGH: never do this on I2C
        if (!warned_drive_high) { warned_drive_high = true; err("MCU drove an I2C line HIGH"); }
        return 1;
    }
    return 0;
}

// ---------- MCP7940N real-time clock ----------
static int bcd2(int b) { return ((b >> 4) & 0x0F) * 10 + (b & 0x0F); }
static int tobcd(int v) { return ((v / 10) << 4) | (v % 10); }
static uint64_t osc_run_at = 0; static bool st_prev = false; static uint64_t accum = 0;
static bool osc_running() { return sim.regs[0x00] & 0x80 && !sim.osc_dead && sim.now_us >= osc_run_at; }
static uint8_t read_reg(int r) {
    uint8_t v = sim.regs[r];
    if (r == 0x03) { v = (uint8_t)(v & ~0x20); if (osc_running()) v |= 0x20; }     // OSCRUN is read-only
    sim.reads_done++;
    if (sim.slave_corrupts_reads && r == 0x00) v ^= 0x01;
    return v;
}
static void write_reg(int r, uint8_t v) {
    sim.regs[r] = v; sim.writes_done++;
    if (r == 0x00) {
        bool st = v & 0x80;
        if (st && !st_prev) { osc_run_at = sim.now_us + 100000; sim.st_set_us = sim.now_us; sim.set_sec = bcd2(v & 0x7F); }
        if (!st) osc_run_at = ~0ULL;
        st_prev = st; accum = 0;
    }
    if (r == 0x01) sim.set_min = bcd2(v & 0x7F);
    if (r == 0x02) { sim.set_hour = bcd2(v & 0x3F); if (v & 0x40) sim.errors.push_back("12-hour mode selected"); }
}
void rtc_tick(uint64_t us) {                       // called whenever simulated time advances
    if (!osc_running()) return;
    accum += us;
    while (accum >= 1000000) {
        accum -= 1000000;
        int s = bcd2(sim.regs[0] & 0x7F) + 1, m = bcd2(sim.regs[1] & 0x7F), h = bcd2(sim.regs[2] & 0x3F);
        if (s >= 60) { s = 0; m++; }
        if (m >= 60) { m = 0; h++; }
        if (h >= 24) h = 0;
        sim.regs[0] = (uint8_t)(0x80 | tobcd(s)); sim.regs[1] = (uint8_t)tobcd(m); sim.regs[2] = (uint8_t)tobcd(h);
    }
}

static void handle_byte() {
    bool ack = false; next_tx = next_rx = false;
    if (byte_index == 0) {
        if (sim.slave_present && (shift_ >> 1) == 0x6F) {
            addressed = true; rw = shift_ & 1;
            if (rw && sim.slave_nacks_read_address) ack = false;
            else { ack = true; if (rw) next_tx = true; else next_rx = true; }
        } else addressed = false;
    } else if (addressed && rw == 0) {
        if (byte_index == 1) {
            sim.ptr = (uint8_t)shift_;
            if (sim.ptr >= 0x60) err("register pointer out of range");
        } else {
            write_reg(sim.ptr % 0x60, (uint8_t)shift_);
            sim.ptr = (uint8_t)((sim.ptr + 1) % 0x60);
        }
        ack = true; next_rx = true;
    }
    slave_sda = ack ? 0 : 1;
    byte_index++;
}
static void load_tx() { tx_byte = read_reg(sim.ptr % 0x60); sim.ptr = (uint8_t)((sim.ptr + 1) % 0x60); }

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
    if (LATC.v != prev_latc) { sim.latc_events.push_back({sim.now_us, LATC.v}); prev_latc = LATC.v; }
}

uint8_t sim_portb() {
    uint8_t v = (uint8_t)(LATB.v & ~TRISB.v);
    if (line(SCL_MASK)) v |= SCL_MASK;
    if (line(SDA_MASK) && slave_sda) v |= SDA_MASK; else v &= (uint8_t)~SDA_MASK;
    return v;
}
uint8_t sim_porta() {
    // RA2: button to GND; weak pull-up needed (WPUA bit 2) and the pin must be an input and digital
    bool input = TRISA.v & 0x04, pullup = WPUA.v & 0x04, digital = !(ANSELA.v & 0x04);
    int level = 0;
    if (input && digital) level = (sim.pressed_mask & 1) ? 0 : (pullup ? 1 : 0);
    return (uint8_t)(level << 2);
}

void sim_delay_us(unsigned long us) {
    uint64_t target = sim.now_us + us;
    while (trans_next < trans.size() && trans[trans_next].t <= target) {
        sim.now_us = trans[trans_next].t;
        if (trans[trans_next].state) sim.pressed_mask |= (uint8_t)(1 << trans[trans_next].idx);
        else sim.pressed_mask &= (uint8_t)~(1 << trans[trans_next].idx);
        trans_next++;
    }
    uint64_t before = sim.now_us;
    sim.now_us = target;
    rtc_tick(target - before);
    if (sim.now_us >= sim.end_us) throw SimEnd();
}

// ---------- Sim API ----------
void Sim::reset() {
    now_us = 0; slave_present = true; slave_corrupts_reads = false; slave_nacks_read_address = false;
    memset(regs, 0, sizeof regs); ptr = 0; osc_dead = false; st_set_us = 0; set_sec = set_min = set_hour = -1; battery_preset = false;
    pressed_mask = 0; presses.clear(); latc_events.clear();
    reads_done = writes_done = 0; errors.clear(); osc_run_at = ~0ULL; st_prev = false; accum = 0;
    min_scl_low = min_scl_high = min_start_setup = min_start_hold = min_stop_setup = min_data_setup = 1e9;
    trans.clear(); trans_next = 0;
    TRISA.v = TRISB.v = TRISC.v = 0xFF; LATA.v = LATB.v = LATC.v = 0; ANSELA.v = ANSELB.v = ANSELC.v = 0xFF; WPUA.v = 0;
    prev_scl = prev_sdam = 1; st = IDLE; slave_sda = 1; prev_latc = 0; warned_drive_high = false;
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
void Sim::preset_running(int h, int m, int s) {      // as if a battery had kept the clock going before power-up
    regs[0] = (uint8_t)(0x80 | tobcd(s)); regs[1] = (uint8_t)tobcd(m); regs[2] = (uint8_t)tobcd(h);
    st_prev = true; osc_run_at = 0; accum = 0; battery_preset = true;
}
