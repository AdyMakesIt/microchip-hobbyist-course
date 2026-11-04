// Month 4 logic tests. Build with -DBUILD=1|2|3 against the matching main.c
#include "sim4.h"
#include "xc.h"
#include <cstdio>
#include <cmath>
extern "C++" void sim_main(void);
static int fails = 0, passes = 0;
#define CHECK(c, m) do { if (c) passes++; else { fails++; printf("  FAIL: %s\n", m); } } while (0)
static bool near(double a, double b, double tol) { return std::fabs(a - b) <= tol; }
static int latc_at(double ms) { int v = 0; for (auto& e : sim.latc_events) if (e.t / 1000.0 <= ms) v = e.v; return v; }
static int pulses(double a, double b) { int n = 0; for (auto& e : sim.latc_events) if ((e.v & 1) && e.t / 1000.0 >= a && e.t / 1000.0 < b) n++; return n; }
static void timing() {
    CHECK(sim.errors.empty(), "no I2C protocol errors");
    for (auto& e : sim.errors) printf("    %s\n", e.c_str());
    CHECK(sim.min_scl_low >= 4.7 && sim.min_scl_high >= 4.0, "SCL low >= 4.7 us and high >= 4.0 us");
    CHECK(sim.min_start_setup >= 4.7 && sim.min_start_hold >= 4.0 && sim.min_stop_setup >= 4.0, "START/STOP set-up and hold times");
    CHECK(sim.min_data_setup >= 0.25, "data set-up >= 250 ns");
    CHECK(TRISC.v == 0x00 && (WPUA.v & 4) == 4 && (ANSELA.v & 4) == 0, "port C outputs; RA2 digital with pull-up");
}
// seconds shown at time T: the clock was set to set_sec at st_set, and counts after a 100 ms oscillator start
static int expect_sec(double ms) { double el = ms * 1000.0 - (double)sim.st_set_us - 100000.0; int k = (int)std::floor(el / 1e6); if (k < 0) k = 0; return (sim.set_sec + k) % 60; }
int main() {
#if BUILD == 1
    printf("Month 4 Build 1 (blink)\n");
    sim.reset(); sim.run(sim_main, 5200);
    auto& e = sim.latc_events;
    CHECK(e.size() >= 10, "LED toggles");
    bool ok = true; for (size_t i = 2; i < e.size(); i++) if (!near((e[i].t - e[i-1].t) / 1000.0, 500, 1)) ok = false;
    CHECK(ok, "500 ms on / 500 ms off");
    CHECK(TRISC.v == 0x00 && ANSELC.v == 0x00, "port C digital outputs");
#elif BUILD == 2
    printf("Month 4 Build 2 (RTC hello)  [__TIME__ = 12:34:50]\n");
    sim.reset(); sim.run(sim_main, 30000);
    CHECK(sim.set_hour == 12 && sim.set_min == 34 && sim.set_sec == 50, "clock set from the build time 12:34:50");
    CHECK(sim.regs[0x00] & 0x80, "oscillator start bit (ST) is set");
    double st = sim.st_set_us / 1000.0;
    bool allok = true;
    for (double off : {1.55, 3.55, 6.55, 9.55, 10.55, 14.55, 25.55}) {
        double T = st + 100 + off * 1000 - 100; int shown = latc_at(T), want = expect_sec(T);
        if (std::abs(shown - want) > 1 && !(shown == 0 && want == 59) && !(shown == 59 && want == 0)) { allok = false; printf("    at +%.2f s shown %d expected %d\n", off, shown, want); }
    }
    CHECK(allok, "LEDs show the seconds counting up, including the wrap 59 -> 0");
    CHECK(sim.regs[0x01] == 0x35 && sim.regs[0x02] == 0x12, "after the wrap the clock reads 12:35 (BCD 0x35, 0x12)");
    timing();
    // clock already running (battery kept it going): must not be overwritten
    sim.reset(); sim.preset_running(10, 20, 30); sim.run(sim_main, 3000);
    CHECK(sim.set_sec == -1 && sim.set_min == -1 && sim.set_hour == -1, "a running clock is left alone");
    CHECK(latc_at(2500) >= 32 && latc_at(2500) <= 33, "and keeps counting from 30 s");
    // faults
    sim.reset(); sim.slave_present = false; sim.run(sim_main, 4000);
    CHECK(pulses(0, 1400) == 1 && pulses(1400, 2800) == 1, "no clock chip -> fault code 1");
    sim.reset(); sim.osc_dead = true; sim.run(sim_main, 9000);
    CHECK(pulses(2100, 3900) == 3 || pulses(2100, 4300) == 3, "crystal never starts -> fault code 3 (after 2 s)");
#else
    printf("Month 4 Build 3 (binary clock)  [__TIME__ = 23:59:55]\n");
    sim.reset();
    sim.press(0, 2000, 2150); sim.press(0, 4000, 4150); sim.press(0, 6000, 6150);
    sim.run(sim_main, 9000);
    double st = sim.st_set_us / 1000.0;
    auto sec_at = [&](double ms) { return expect_sec(ms); };
    CHECK(sim.set_hour == 23 && sim.set_min == 59 && sim.set_sec == 55, "clock set from the build time 23:59:55");
    int v1 = latc_at(1250);                          // seconds mode
    CHECK((v1 & 0xC0) == 0 && std::abs((v1 & 0x3F) - sec_at(1250)) <= 1, "seconds mode: no mode LED, value = seconds");
    int v2 = latc_at(3250);                          // minutes mode (23:59:5x)
    CHECK((v2 & 0xC0) == 0x40 && (v2 & 0x3F) == 59, "first press: minutes mode, RC6 lit, minutes = 59");
    int v3 = latc_at(4250);                          // hours mode, before midnight rollover
    CHECK((v3 & 0xC0) == 0x80 && (v3 & 0x3F) == 23, "second press: hours mode, RC7 lit, hours = 23");
    int v4 = latc_at(5750);                          // after the rollover to 00:00
    CHECK((v4 & 0xC0) == 0x80 && (v4 & 0x3F) == 0, "midnight rollover: hours read 0");
    int v5 = latc_at(6750);
    CHECK((v5 & 0xC0) == 0 && std::abs((v5 & 0x3F) - sec_at(6750)) <= 1, "third press: back to seconds");
    CHECK(sim.regs[0x02] == 0x00 && sim.regs[0x01] == 0x00, "after midnight the registers read 00:00");
    timing();
#endif
    printf("%s  (%d checks passed, %d failed)\n", fails ? "FAILED" : "PASS", passes, fails);
    return fails != 0;
}
