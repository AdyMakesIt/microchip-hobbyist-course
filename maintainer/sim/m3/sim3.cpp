// Month 3 model: PIC18F47K42 pins RC0..RC4, RB0, port D; an MCP3008 ADC and an MCP4822 DAC on a shared SPI bus.
#include "xc.h"
#include "sim3.h"
#include <algorithm>
Reg8 TRISB(1), TRISC(2), TRISD(3), LATB(4), LATC(5), LATD(6), ANSELB(7), ANSELC(8), ANSELD(9), OSCFRQ(10);
Sim3 sim3;
static const uint8_t SCK = 0x01, MOSI = 0x02, MISO = 0x04, CS_ADC = 0x08, CS_DAC = 0x10;
static int p_sck, p_cs_adc, p_cs_dac;
static bool adc_sel, dac_sel, adc_parsed;
static int nclk, bitsIn[40], S, adc_result, dac_bits, dac_shift;
static double t_sck_rise = -1, t_sck_fall = -1, t_cs_rise = -1, t_cs_fall = -1, t_last_sck_fall = -1;
static int prev_hb = 0;

static void err(const std::string& s) { if (sim3.errors.size() < 20) sim3.errors.push_back(s); }
static int pin(uint8_t m) {                       // level of a PORTC output pin
    if (TRISC.v & m) return (m == CS_ADC || m == CS_DAC) ? 1 : 0;   // still an input (power-up): chip-selects idle HIGH, others LOW
    return (LATC.v & m) ? 1 : 0;
}
static int adc_value(int ch) {
    int mV = 0;
    switch (ch) {
        case 0: mV = sim3.pot_mV; break;
        case 1: mV = sim3.loopback ? sim3.dac_mV[0] : 0; break;
        case 6: mV = sim3.ch6_mV; break;
        case 7: mV = sim3.ch7_mV; break;
        default: mV = 0;
    }
    long v = (long)mV * 1024 / sim3.vdd_mV; return (int)std::min(1023L, std::max(0L, v));
}
static void spi_update() {
    double t = (double)sim3.now_us;
    int sck = pin(SCK), mosi = pin(MOSI), cs_adc = pin(CS_ADC), cs_dac = pin(CS_DAC);
    if (!cs_adc && !cs_dac) err("both chip-selects LOW at once");
    // chip-select edges
    if (p_cs_adc && !cs_adc) {                       // ADC selected
        if (t_cs_rise >= 0) sim3.min_cs_high = std::min(sim3.min_cs_high, t - t_cs_rise);
        adc_sel = true; nclk = 0; adc_parsed = false; t_cs_fall = t;
        if (sck) err("SCK HIGH when ADC selected");
    }
    if (!p_cs_adc && cs_adc) {                       // ADC deselected
        if (nclk != 24) err("ADC transaction was not 24 clocks");
        if (adc_parsed) { sim3.adc_conversions++; }
        if (t_last_sck_fall >= 0) sim3.min_cs_to_clk = std::min(sim3.min_cs_to_clk, t - t_last_sck_fall);
        adc_sel = false; t_cs_rise = t;
    }
    if (p_cs_dac && !cs_dac) { dac_sel = true; dac_bits = 0; dac_shift = 0; t_cs_fall = t; if (sck) err("SCK HIGH when DAC selected"); }
    if (!p_cs_dac && cs_dac) {                       // DAC deselected: latch
        if (dac_bits != 16) err("DAC frame was not 16 bits");
        else {
            int chan = (dac_shift >> 15) & 1, gain1x = (dac_shift >> 13) & 1, active = (dac_shift >> 12) & 1, code = dac_shift & 0xFFF;
            sim3.dac_writes.push_back({sim3.now_us, chan, code, !gain1x, (bool)active, dac_bits});
            sim3.dac_mV[chan] = active ? (int)((long)code * (gain1x ? 2048 : 4096) / 4096) : 0;
        }
        dac_sel = false;
    }
    // clock edges
    if (!p_sck && sck) {                             // SCK rising
        if (t_sck_fall >= 0) sim3.min_sck_low = std::min(sim3.min_sck_low, t - t_sck_fall);
        if (t_cs_fall >= 0 && (adc_sel || dac_sel) && (nclk == 0 || dac_bits == 0)) sim3.min_cs_to_clk = std::min(sim3.min_cs_to_clk, t - t_cs_fall);
        t_sck_rise = t;
        if (adc_sel) {
            nclk++; if (nclk < 40) bitsIn[nclk] = mosi;
            if (nclk == 12 && !adc_parsed) {
                S = 0; for (int i = 1; i <= 12; i++) if (bitsIn[i]) { S = i; break; }
                if (!S) err("no START bit seen by clock 12");
                else {
                    int sgl = bitsIn[S + 1], ch = (bitsIn[S + 2] << 2) | (bitsIn[S + 3] << 1) | bitsIn[S + 4];
                    if (!sgl) err("differential mode requested (not used in this course)");
                    adc_result = adc_value(ch); sim3.adc_channels.push_back(ch); adc_parsed = true;
                }
            }
        }
        if (dac_sel) { dac_shift = ((dac_shift << 1) | mosi) & 0xFFFF; dac_bits++; }
    }
    if (p_sck && !sck) {                             // SCK falling
        if (t_sck_rise >= 0) sim3.min_sck_high = std::min(sim3.min_sck_high, t - t_sck_rise);
        t_sck_fall = t; t_last_sck_fall = t;
    }
    p_sck = sck; p_cs_adc = cs_adc; p_cs_dac = cs_dac;
}
void sim_reg_written(int which) {
    spi_update();
    if (which == 6) sim3.latd_events.push_back({sim3.now_us, LATD.v});
    int hb = (!(TRISB.v & 1)) && (LATB.v & 1);
    if (hb != prev_hb) { sim3.hb_events.push_back({sim3.now_us, hb}); prev_hb = hb; }
}
uint8_t sim_portc() {
    uint8_t v = (uint8_t)(LATC.v & ~TRISC.v);
    int bit = 0;
    if (adc_sel && adc_parsed) {
        if (nclk == S + 6) bit = 0;                                  // the "null" bit
        else if (nclk >= S + 7 && nclk <= S + 16) bit = (adc_result >> (9 - (nclk - (S + 7)))) & 1;
    }
    if (sim3.miso_stuck >= 0) bit = sim3.miso_stuck;
    if (bit) v |= MISO;
    return v;
}
void sim_delay_us(unsigned long us) {
    uint64_t target = sim3.now_us + us;
    for (auto& c : sim3.pot_changes) if (c.t > sim3.now_us && c.t <= target) {}
    // apply pot changes that fall inside this interval
    for (auto& c : sim3.pot_changes) if (c.t <= target) sim3.pot_mV = c.mV;
    sim3.now_us = target;
    if (sim3.now_us >= sim3.end_us) throw SimEnd3();
}
void Sim3::reset() {
    now_us = 0; vdd_mV = 5000; pot_mV = 0; ch6_mV = 5000; ch7_mV = 0; loopback = true; miso_stuck = -1; pot_changes.clear();
    latd_events.clear(); hb_events.clear(); dac_writes.clear(); dac_mV[0] = dac_mV[1] = 0; adc_conversions = 0; adc_channels.clear(); errors.clear();
    min_sck_high = min_sck_low = min_cs_high = min_cs_to_clk = 1e9;
    TRISB.v = TRISC.v = TRISD.v = 0xFF; LATB.v = LATC.v = LATD.v = 0; ANSELB.v = ANSELC.v = ANSELD.v = 0xFF; OSCFRQ.v = 0;
    p_sck = 0; p_cs_adc = p_cs_dac = 1; adc_sel = dac_sel = adc_parsed = false; nclk = 0; prev_hb = 0;
    t_sck_rise = t_sck_fall = t_cs_rise = t_cs_fall = t_last_sck_fall = -1;
}
void Sim3::potAt(uint64_t ms, int mV) { pot_changes.push_back({ms * 1000, mV}); std::sort(pot_changes.begin(), pot_changes.end(), [](const PotChange& a, const PotChange& b) { return a.t < b.t; }); }
void Sim3::run(void (*entry)(void), uint64_t ms) { end_us = ms * 1000; try { entry(); } catch (SimEnd3&) {} }
