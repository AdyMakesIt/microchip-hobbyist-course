#include "xc.h"
#include "tests.h"
#include <vector>
static std::vector<int> seq_between(double a, double b) { std::vector<int> r; for (auto& e : sim.olata_events) { double t = e.t/1000.0; if (t >= a && t < b) r.push_back(e.v); } return r; }
static bool eq(const std::vector<int>& v, std::initializer_list<int> w) { return v == std::vector<int>(w); }
int main() {
    printf("Month 2 Build 4 (Workshop Command Centre)\n");
    sim.reset();
    // timeline (ms): start-up ends ~ 940. Mode 0 steps every 400.
    sim.press(0, 3000, 3150);     // MODE   -> mode 1 (bar fill), still 400 ms
    sim.press(0, 6000, 6150);     // MODE   -> mode 2 (alternate)
    sim.press(1, 8000, 8150);     // SPEED  -> 200 ms
    sim.press(1, 9500, 9650);     // SPEED  -> 100 ms
    sim.press(0, 11000, 11150);   // MODE   -> mode 0 again (running light), 100 ms
    sim.press(1, 12000, 12150);   // SPEED  -> wraps to 400 ms
    sim.run(sim_main, 14000);

    auto& ev = sim.olata_events;
    CHECK(ev.size() > 10 && ev[0].v == 0xFF, "lamp test first");
    // mode 0 phase: 0x01 shown at start, then 02,04,08 ... every 400 ms
    auto m0 = seq_between(100, 3000);
    CHECK(m0.size() >= 4 && m0[0] == 0x01, "running light starts on LED 1");
    bool spacing = true; double prev = -1;
    for (auto& e : ev) { double t = e.t/1000.0; if (t > 1000 && t < 2950) { if (prev > 0 && !near(t - prev, 400, 30)) spacing = false; prev = t; } }
    CHECK(spacing, "mode 0 / slow speed: a step about every 0.4 s (400 ms + I2C time)");
    // mode 1 after first MODE press: restart at 01 then 03 07 0F 1F 3F 7F FF 00 01 ...
    auto m1 = seq_between(3000, 6000);
    CHECK(m1.size() >= 7 && m1[0] == 0x01 && m1[1] == 0x03 && m1[2] == 0x07 && m1[3] == 0x0F, "mode 1: bar fills 01 03 07 0F ...");
    // mode 2
    auto m2 = seq_between(6000, 8000);
    CHECK(m2.size() >= 4 && m2[0] == 0xAA && m2[1] == 0x55 && m2[2] == 0xAA && m2[3] == 0x55, "mode 2: AA 55 AA 55");
    // speed 200 ms: spacing between 8000 and 9500
    bool s2 = true; prev = -1;
    for (auto& e : ev) { double t = e.t/1000.0; if (t > 8250 && t < 9450) { if (prev > 0 && !near(t - prev, 200, 20)) s2 = false; prev = t; } }
    CHECK(s2, "after 1st SPEED press: a step about every 0.2 s");
    bool s3 = true; prev = -1;
    for (auto& e : ev) { double t = e.t/1000.0; if (t > 9750 && t < 10950) { if (prev > 0 && !near(t - prev, 100, 10)) s3 = false; prev = t; } }
    CHECK(s3, "after 2nd SPEED press: a step about every 0.1 s");
    auto m0b = seq_between(11000, 11400);
    CHECK(m0b.size() >= 3 && m0b[0] == 0x01 && m0b[1] == 0x02 && m0b[2] == 0x04, "MODE wraps back to the running light");
    bool s4 = true; prev = -1;
    for (auto& e : ev) { double t = e.t/1000.0; if (t > 12300 && t < 13950) { if (prev > 0 && !near(t - prev, 400, 30)) s4 = false; prev = t; } }
    CHECK(s4, "3rd SPEED press wraps back to 400 ms");
    // beeps: 1 at start + 6 presses = 7 beeps x 200 toggles
    CHECK(sim.piezo_toggles == 7 * 200, "one beep at start-up and one per button press (200 pin changes each)");
    CHECK((LATD.v & 0x08) == 0, "piezo pin left LOW after beeping");
    CHECK(led_times().size() >= 20, "heartbeat keeps toggling");
    report_timing();
    printf("%s  (%d checks passed, %d failed)\n", g_fail ? "FAILED" : "PASS", g_pass, g_fail); return g_fail != 0;
}
