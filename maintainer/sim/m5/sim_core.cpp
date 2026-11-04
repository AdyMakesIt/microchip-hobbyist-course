// Logic simulator for Month 5: a PIC24FJ64GA002's pins RB8/RB9, RA0/RA1, eight LEDs on port B, an I2C bus,
// and a 24LC512 EEPROM (address 0x50, 16-bit addressing, 128-byte pages, 5 ms write cycle).
//
// It checks LOGIC, not electronics: register values, I2C protocol sequence, button
// handling, timing against the I2C standard-mode limits. It cannot tell you whether
// your breadboard wiring is right or whether XC8 accepts the code.
#include "sim5.h"
#include "xc.h"
#include <algorithm>
#include <cstdio>
#include <cstring>

Reg16 TRISA, TRISB, LATA, LATB, AD1PCFG, CLKDIV;
Sim sim;

static const uint16_t SCL_MASK = 0x0100, SDA_MASK = 0x0200;   // RB8, RB9

// ---------- bus / slave state ----------
static int prev_scl = 1, prev_sdam = 1;
enum St { IDLE, RX, ACK, TX, MACK };
static St st = IDLE;
static int bits, shift_, byte_index, rw, slave_sda = 1, tx_byte, mack_ack;
static bool addressed, next_tx, next_rx;
static double t_scl_rise = -1, t_scl_fall = -1, t_sda_rise = -1, t_sda_change = -1, t_start = -1;
static int prev_led = 0, prev_hb = 0;
static bool warned_drive_high = false;

struct Trans { uint64_t t; int idx; int state; };
static std::vector<Trans> trans;
static size_t trans_next = 0;

static void err(const std::string& s) {
    char buf[64]; snprintf(buf, sizeof buf, " [t=%.3f ms]", sim.now_us / 1000.0);
    if (sim.errors.size() < 20) sim.errors.push_back(s + buf);
}

static int line(uint16_t mask) {
    if (TRISB.v & mask) return 1;                    // released: pulled HIGH by 4.7k
    if (LATB.v & mask) {                             // driven HIGH: never do this on I2C
        if (!warned_drive_high) { warned_drive_high = true; err("MCU drove an I2C line HIGH"); }
        return 1;
    }
    return 0;
}

// ---------- 24LC512 EEPROM ----------
static uint16_t ptr16 = 0; static int wcount = 0; static uint8_t wbuf[300]; static uint16_t wstart = 0; static bool addressed_write = false;
static bool ee_busy() { return sim.now_us < sim.busy_until; }
static void ee_commit() {                       // STOP after a write sequence with data: store it (page wrap!) and go busy
    if (wcount <= 0) return;
    for (int i = 0; i < wcount; i++) {
        uint16_t a = (uint16_t)((wstart & ~0x7F) | ((wstart + i) & 0x7F));        // wraps inside the 128-byte page
        if (((wstart + i) & ~0x7F) != (wstart & ~0x7F)) sim.page_wraps++;
        sim.mem[a] = wbuf[i];
        sim.write_log.push_back({sim.now_us, a, wbuf[i]});
    }
    sim.busy_until = sim.eeprom_never_ready ? ~0ULL : sim.now_us + 5000;
    wcount = 0;
}
static void eeprom_stop() { if (addressed_write) ee_commit(); addressed_write = false; }
static void handle_byte() {
    bool ack = false; next_tx = next_rx = false;
    if (byte_index == 0) {
        if (sim.slave_present && (shift_ >> 1) == 0x50 && !ee_busy()) {
            addressed = true; rw = shift_ & 1;
            if (rw && sim.slave_nacks_read_address) ack = false;
            else { ack = true; if (rw) next_tx = true; else { next_rx = true; addressed_write = true; wcount = 0; } }
        } else addressed = false;
        if (addressed && rw == 0) sim.byte_after_addr = 0;
    } else if (addressed && rw == 0) {
        sim.byte_after_addr++;
        if (sim.byte_after_addr == 1) ptr16 = (uint16_t)((shift_ & 0xFF) << 8);
        else if (sim.byte_after_addr == 2) { ptr16 |= (uint16_t)(shift_ & 0xFF); wstart = ptr16; }
        else { if (wcount < 300) wbuf[wcount++] = (uint8_t)shift_; }
        ack = true; next_rx = true;
    }
    slave_sda = ack ? 0 : 1;
    byte_index++;
}
static void load_tx() {
    uint8_t v = sim.mem[ptr16]; ptr16++;
    if (sim.slave_corrupts_reads) v ^= 0x01;
    tx_byte = v; sim.reads_done++;
}

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
            st = IDLE; slave_sda = 1; eeprom_stop();
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
    int led = ((LATB.v >> 2) & 0x03) | (((LATB.v >> 10) & 0x3F) << 2);
    if (led != prev_led) { sim.led_events.push_back({sim.now_us, led}); prev_led = led; }
    int hb = (!(TRISA.v & 1)) && (LATA.v & 1);
    if (hb != prev_hb) { sim.hb_events.push_back({sim.now_us, hb}); prev_hb = hb; }
}
uint16_t sim_portb() {
    uint16_t v = (uint16_t)(LATB.v & ~TRISB.v);
    if (line(SCL_MASK)) v |= SCL_MASK;
    if (line(SDA_MASK) && slave_sda) v |= SDA_MASK; else v &= (uint16_t)~SDA_MASK;
    return v;
}
uint16_t sim_porta() {                      // RA1: button to GND, with an external pull-up to 3.3 V
    bool input = TRISA.v & 0x0002;
    int level = 0;
    if (input) level = (sim.pressed_mask & 1) ? 0 : 1;
    return (uint16_t)(level << 1);
}

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
void Sim::reset(bool keep_memory) {
    now_us = 0; slave_present = true; slave_corrupts_reads = false; slave_nacks_read_address = false; eeprom_never_ready = false;
    if (!keep_memory) memset(mem, 0xFF, sizeof mem);
    busy_until = 0; page_wraps = 0; byte_after_addr = 0; reads_done = 0;
    pressed_mask = 0; presses.clear(); led_events.clear(); hb_events.clear(); write_log.clear(); errors.clear();
    min_scl_low = min_scl_high = min_start_setup = min_start_hold = min_stop_setup = min_data_setup = 1e9;
    trans.clear(); trans_next = 0;
    TRISA.v = TRISB.v = 0xFFFF; LATA.v = LATB.v = 0; AD1PCFG.v = 0x0000; CLKDIV.v = 0x0100;     // real reset values: all pins analog, slow clock
    prev_scl = prev_sdam = 1; st = IDLE; slave_sda = 1; prev_led = prev_hb = 0; warned_drive_high = false;
    t_scl_rise = t_scl_fall = t_sda_rise = t_sda_change = t_start = -1; wcount = 0; addressed_write = false; ptr16 = 0;
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
void Sim::run(int (*entry)(void), uint64_t duration_ms) {
    end_us = duration_ms * 1000;
    try { entry(); } catch (SimEnd&) {}
}
