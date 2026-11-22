#include "tests.h"
int main() {
    printf("Month 2 Build 3 (LED chase + button)\n");
    sim.reset();
    // 8 presses with contact bounce, 300 ms apart; then one long 2-second hold; then a press on the WRONG button
    uint64_t t0 = 1500;
    for (int i = 0; i < 8; i++) sim.press(0, t0 + i * 300, t0 + i * 300 + 120, true);
    sim.press(0, 5000, 7000, true);        // long hold = still one step
    sim.press(1, 8000, 8200, true);        // GPB1: must do nothing in this build
    sim.run(sim_main, 9000);
    CHECK(sim.regs[0x00] == 0x00 && sim.regs[0x01] == 0xFF && sim.regs[0x0D] == 0xFF, "IODIRA=0x00, IODIRB=0xFF, GPPUB=0xFF");
    auto& ev = sim.olata_events;
    CHECK(ev.size() >= 3 && ev[0].v == 0xFF, "lamp test: all 8 LEDs on first");
    CHECK(ev.size() >= 3 && ev[1].v == 0x01 && near(ev[1].t / 1000.0, 500, 5), "then LED 1 only, after ~500 ms");
    int expect[] = {0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x01, 0x02};   // 8 presses, then the long hold
    bool seq = ev.size() == 2 + 9; 
    CHECK(seq, "exactly one OLATA write per press (bounce and long hold cause no extra steps)");
    if (seq) { bool ok = true; for (int i = 0; i < 9; i++) if (ev[2 + i].v != expect[i]) ok = false;
        CHECK(ok, "sequence 02 04 08 10 20 40 80 then wraps to 01, then 02 on the long hold"); }
    CHECK(sim.ledsOn() == 0x02, "final state: LED 2 lit (GPB1 press ignored)");
    CHECK(led_times().size() >= 16, "heartbeat keeps toggling while the program runs");
    report_timing();
    // --- expander disappears mid-run -> fault code (write fail = 1)
    printf("%s  (%d checks passed, %d failed)\n", g_fail ? "FAILED" : "PASS", g_pass, g_fail); return g_fail != 0;
}
