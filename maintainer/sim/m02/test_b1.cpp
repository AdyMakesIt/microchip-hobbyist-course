#include "tests.h"
int main() {
    printf("Month 2 Build 1 (blink)\n");
    sim.reset(); sim.run(sim_main, 5200);
    auto t = led_times();
    CHECK(t.size() >= 10, "LED toggled at least 10 times in 5.2 s");
    bool ok = true; for (size_t i = 1; i < t.size(); i++) if (!near(t[i] - t[i-1], 500, 1)) ok = false;
    CHECK(ok, "every LED change is exactly 500 ms after the last");
    CHECK(sim.led_events.size() && sim.led_events[0].v == 1, "first event is LED ON");
    printf("%s  (%d checks passed, %d failed)\n", g_fail ? "FAILED" : "PASS", g_pass, g_fail); return g_fail != 0;
}
