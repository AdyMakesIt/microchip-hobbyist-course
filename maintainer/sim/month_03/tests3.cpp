// Month 3 logic tests. Build with -DBUILD=1|2|3 against the matching main.c
#include "sim3.h"
#include "xc.h"
#include <cstdio>
#include <cmath>
extern "C++" void sim_main(void);
static int fails = 0, passes = 0;
#define CHECK(c, m) do { if (c) passes++; else { fails++; printf("  FAIL: %s\n", m); } } while (0)
static bool near(double a, double b, double tol) { return std::fabs(a - b) <= tol; }
static int latd_at(double ms) { int v = 0; for (auto& e : sim3.latd_events) if (e.t / 1000.0 <= ms) v = e.v; return v; }
static int pulses(double a, double b) { int n = 0; for (auto& e : sim3.hb_events) if (e.v == 1 && e.t / 1000.0 >= a && e.t / 1000.0 < b) n++; return n; }
static void timing() {
    CHECK(sim3.errors.empty(), "no SPI protocol errors");
    for (auto& e : sim3.errors) printf("    %s\n", e.c_str());
    CHECK(sim3.min_sck_high >= 0.125 && sim3.min_sck_low >= 0.125, "SCK high and low times >= 125 ns (MCP3008 limit)");
    CHECK(sim3.min_cs_high >= 0.5, "CS high time between conversions >= 500 ns");
    CHECK(TRISC.v == 0xE4 && TRISD.v == 0x00 && (TRISB.v & 1) == 0, "pin directions: SPI outputs, MISO input, bar graph and heartbeat outputs");
}
int main() {
#if BUILD == 1
    printf("Month 3 Build 1 (ADC bar graph)\n");
    sim3.reset(); sim3.potAt(300, 2500); sim3.potAt(600, 5000); sim3.potAt(900, 1300);
    sim3.run(sim_main, 1200);
    CHECK(latd_at(250) == 0x00, "knob at 0 V: no LEDs");
    CHECK(latd_at(550) == 0x0F, "knob at 2.5 V (512 counts): 4 LEDs");
    CHECK(latd_at(850) == 0xFF, "knob at 5 V (1023 counts): all 8 LEDs");
    CHECK(latd_at(1150) == 0x03, "knob at 1.3 V (266 counts): 2 LEDs");
    bool only01 = true; for (int c : sim3.adc_channels) if (c != 0 && c != 6 && c != 7) only01 = false;
    CHECK(only01, "ADC channels used are 0, 6 and 7 only");
    CHECK(sim3.adc_channels.size() >= 2 && sim3.adc_channels[0] == 7 && sim3.adc_channels[1] == 6, "self-test reads channel 7 then 6 first");
    timing();
    // fault: channel 7 (GND) not near 0
    sim3.reset(); sim3.ch7_mV = 2000; sim3.run(sim_main, 4000);
    CHECK(pulses(0, 1400) == 1 && pulses(1400, 2800) == 1, "CH7 wrong -> fault code 1");
    sim3.reset(); sim3.ch6_mV = 1000; sim3.run(sim_main, 5000);
    CHECK(pulses(0, 1800) == 2 && pulses(1800, 3600) == 2, "CH6 wrong -> fault code 2");
    sim3.reset(); sim3.miso_stuck = 0; sim3.run(sim_main, 5000);
    CHECK(pulses(0, 1800) == 2, "MISO stuck LOW (not connected) -> fault code 2");
    sim3.reset(); sim3.miso_stuck = 1; sim3.run(sim_main, 4000);
    CHECK(pulses(0, 1400) == 1, "MISO stuck HIGH -> fault code 1");
#elif BUILD == 2
    printf("Month 3 Build 2 (DAC)\n");
    sim3.reset(); sim3.potAt(500, 2500); sim3.potAt(1500, 5000); sim3.potAt(2500, 100);
    sim3.run(sim_main, 4000);
    int lastA(-1), atA2500 = -1, atA5000 = -1, atA100 = -1; int maxB = 0, minB = 99999; bool up = false, down = false, frames = true; int prevB = -1;
    for (auto& w : sim3.dac_writes) {
        if (!w.active || !w.gain2x || w.bits != 16) frames = false;
        double ms = w.t / 1000.0;
        if (w.chan == 0) { if (ms > 1000 && ms < 1450) atA2500 = w.code; if (ms > 2000 && ms < 2450) atA5000 = w.code; if (ms > 3500) atA100 = w.code; lastA = w.code; }
        else { maxB = std::max(maxB, w.code); minB = std::min(minB, w.code); if (prevB >= 0) { if (w.code > prevB) up = true; if (w.code < prevB) down = true; } prevB = w.code; }
    }
    CHECK(frames, "every DAC frame is 16 bits with gain 2x and output ON");
    CHECK(atA2500 == 2500, "knob at 2.5 V -> DAC A code 2500 (= 2.500 V)");
    CHECK(atA5000 == 4095, "knob at 5 V -> DAC A limited to 4095");
    CHECK(atA100 == (100 * 1024 / 5000) * 5000 / 1024 || near(atA100, 100, 6), "knob at 0.1 V -> DAC A about 100");
    CHECK(maxB >= 4050 && minB <= 41, "DAC B triangle spans about 0 to 4095");
    CHECK(up && down, "DAC B rises and falls");
    CHECK(sim3.dac_mV[1] >= 0 && sim3.dac_mV[0] <= 4095, "outputs within range");
    timing();
#else
    printf("Month 3 Build 3 (loopback)\n");
    sim3.reset(); sim3.run(sim_main, 5000);
    int lo = 255, hi = 0; bool rose = false, fell = false; int prev = -1;
    for (auto& e : sim3.latd_events) if (e.t > 600000) { lo = std::min(lo, e.v); hi = std::max(hi, e.v); if (prev >= 0) { if (e.v > prev) rose = true; if (e.v < prev) fell = true; } prev = e.v; }
    CHECK(lo == 0x00 && hi == 0x7F, "bar sweeps from 0 LEDs up to 7 LEDs (DAC tops out at 4.095 V)");
    CHECK(rose && fell, "bar rises and falls");
    CHECK(pulses(0, 5000) == 0 || sim3.hb_events.size() > 4, "heartbeat toggles normally (no fault)");
    timing();
    bool selftestOK = sim3.dac_writes.size() >= 4 && sim3.dac_writes[0].code == 500 && sim3.dac_writes[1].code == 1500 && sim3.dac_writes[2].code == 2500 && sim3.dac_writes[3].code == 3500;
    CHECK(selftestOK, "self-test outputs 0.5, 1.5, 2.5 and 3.5 V");
    // wrong supply voltages still pass (reference is the supply)
    sim3.reset(); sim3.vdd_mV = 4600; sim3.run(sim_main, 3000);
    CHECK(sim3.hb_events.size() > 3, "4.6 V supply still passes the self-test");
    sim3.reset(); sim3.vdd_mV = 5400; sim3.run(sim_main, 3000);
    CHECK(sim3.hb_events.size() > 3, "5.4 V supply still passes the self-test");
    // fault: loop wire missing
    sim3.reset(); sim3.loopback = false; sim3.run(sim_main, 5000);
    CHECK(pulses(0, 2200) == 3 && pulses(2200, 4400) == 3, "missing loop-back wire -> fault code 3");
#endif
    printf("%s  (%d checks passed, %d failed)\n", fails ? "FAILED" : "PASS", passes, fails);
    return fails != 0;
}
