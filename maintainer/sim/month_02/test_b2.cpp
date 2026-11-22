#include "tests.h"
// Count blink pulses in the first N ms and pause structure.
static int pulses_between(double a, double b) { int n = 0; for (auto& e : sim.led_events) if (e.v == 1 && e.t/1000.0 >= a && e.t/1000.0 < b) n++; return n; }
int main() {
    printf("Month 2 Build 2 (hello expander)\n");
    // --- normal
    sim.reset(); sim.run(sim_main, 3300);
    CHECK(sim.regs[0x00] == 0xFE, "IODIRA = 0xFE (GPA0 output, rest inputs)");
    CHECK(sim.regs[0x14] == 0x01, "OLATA = 0x01");
    CHECK(sim.ledsOn() == 0x01, "exactly the GPA0 LED is lit");
    auto t = led_times();
    CHECK(t.size() >= 6, "heartbeat toggles");
    bool ok = true; for (size_t i = 1; i < t.size(); i++) if (!near(t[i] - t[i-1], 500, 1)) ok = false;
    CHECK(ok, "heartbeat period = 500 ms on / 500 ms off");
    CHECK(sim.reads_done >= 1 && sim.writes_done >= 2, "register read-back actually performed");
    report_timing();
    // --- no expander at all -> fault 1
    sim.reset(); sim.slave_present = false; sim.run(sim_main, 5000);
    // pattern: 1 pulse (200 on, 200 off), pause 1000, repeat -> period 1400
    CHECK(pulses_between(0, 1400) == 1 && pulses_between(1400, 2800) == 1, "no expander -> fault code 1 (one blink per cycle)");
    // --- answers writes but NACKs read address -> fault 2
    sim.reset(); sim.slave_nacks_read_address = true; sim.run(sim_main, 5000);
    CHECK(pulses_between(0, 1800) == 2 && pulses_between(1800, 3600) == 2, "read NACK -> fault code 2 (two blinks per cycle)");
    // --- wrong read-back -> fault 3
    sim.reset(); sim.slave_corrupts_reads = true; sim.run(sim_main, 6000);
    CHECK(pulses_between(0, 2200) == 3 && pulses_between(2200, 4400) == 3, "wrong read-back -> fault code 3 (three blinks per cycle)");
    printf("%s  (%d checks passed, %d failed)\n", g_fail ? "FAILED" : "PASS", g_pass, g_fail); return g_fail != 0;
}
