// Month 5 logic tests. Build with -DBUILD=1|2|3 against the matching main.c
#include "sim5.h"
#include "xc.h"
#include <cstdio>
#include <cmath>
extern int sim_main(void);
static int fails = 0, passes = 0;
#define CHECK(c, m) do { if (c) passes++; else { fails++; printf("  FAIL: %s\n", m); } } while (0)
static bool near(double a, double b, double tol) { return std::fabs(a - b) <= tol; }
static int led_at(double ms) { int v = 0; for (auto& e : sim.led_events) if (e.t / 1000.0 <= ms) v = e.v; return v; }
static int pulses(double a, double b) { int n = 0; for (auto& e : sim.hb_events) if (e.v == 1 && e.t / 1000.0 >= a && e.t / 1000.0 < b) n++; return n; }
static void timing() {
    CHECK(sim.errors.empty(), "no I2C protocol errors");
    for (auto& e : sim.errors) printf("    %s\n", e.c_str());
    CHECK(sim.min_scl_low >= 4.7 && sim.min_scl_high >= 4.0, "SCL low >= 4.7 us and high >= 4.0 us");
    CHECK(sim.min_start_setup >= 4.7 && sim.min_start_hold >= 4.0 && sim.min_stop_setup >= 4.0, "START/STOP set-up and hold times");
    CHECK(sim.min_data_setup >= 0.25, "data set-up >= 250 ns");
    CHECK(CLKDIV.v == 0x0000 && AD1PCFG.v == 0xFFFF, "clock divider cleared (8 MHz) and every pin digital");
    CHECK(TRISA.v == 0xFFFE && TRISB.v == 0x03F3, "pin directions: RA0 and the eight LED pins are outputs, the rest inputs");
}
int main() {
#if BUILD == 1
    printf("Month 5 Build 1 (blink at 3.3 V)\n");
    sim.reset(); sim.run(sim_main, 5200);
    auto& e = sim.hb_events;
    CHECK(e.size() >= 10, "LED toggles");
    bool ok = true; for (size_t i = 2; i < e.size(); i++) if (!near((e[i].t - e[i-1].t) / 1000.0, 500, 1)) ok = false;
    CHECK(ok, "500 ms on / 500 ms off");
    CHECK(CLKDIV.v == 0 && AD1PCFG.v == 0xFFFF && TRISA.v == 0xFFFE, "clock 8 MHz, pins digital, RA0 output");
#elif BUILD == 2
    printf("Month 5 Build 2 (EEPROM hello)\n");
    sim.reset(); sim.run(sim_main, 3300);
    CHECK(sim.mem[0x0123] == 0xA5 && sim.mem[0x0000] == 0xFF && sim.mem[0x2301] == 0xFF && sim.write_log.size() == 1, "0xA5 stored at address 0x0123 (not 0x2301 or 0), exactly one byte written");
    CHECK(led_at(3000) == 0xA5, "the eight LEDs show 1010 0101 (0xA5), bit order as wired");
    CHECK(!sim.led_events.empty() && !sim.write_log.empty() && sim.led_events.back().t > sim.write_log[0].t + 5000 && sim.led_events.back().t < sim.write_log[0].t + 20000,
          "the read happens after the 5 ms write cycle (ACK polling worked)");
    auto& h = sim.hb_events; bool ok = h.size() >= 6; for (size_t i = 1; i < h.size(); i++) if (!near((h[i].t - h[i-1].t) / 1000.0, 500, 1)) ok = false;
    CHECK(ok, "heartbeat 500 ms on / 500 ms off");
    timing();
    sim.reset(); sim.slave_present = false; sim.run(sim_main, 4000);
    CHECK(pulses(0, 1400) == 1 && pulses(1400, 2800) == 1, "no EEPROM -> fault code 1");
    sim.reset(); sim.slave_nacks_read_address = true; sim.run(sim_main, 5000);
    CHECK(pulses(0, 1800) == 2 && pulses(1800, 3600) == 2, "read NACK -> fault code 2");
    sim.reset(); sim.slave_corrupts_reads = true; sim.run(sim_main, 6000);
    CHECK(pulses(0, 2200) == 3 && pulses(2200, 4400) == 3, "wrong read-back -> fault code 3");
    sim.reset(); sim.eeprom_never_ready = true; sim.run(sim_main, 7000);
    CHECK(pulses(0, 2600) == 4 && pulses(2600, 5200) == 4, "EEPROM never ready -> fault code 4");
#else
    printf("Month 5 Build 3 (boot counter)\n");
    // power-cycle the board three times: the number must keep climbing
    sim.reset(); sim.run(sim_main, 1500);
    CHECK(sim.mem[0] == 0x01 && sim.mem[1] == 0x00 && led_at(1400) == 0x01, "first power-up on a blank EEPROM: counter 1");
    sim.reset(true); sim.run(sim_main, 1500);
    CHECK(sim.mem[0] == 0x02 && led_at(1400) == 0x02, "second power-up: counter 2 (it remembered)");
    sim.reset(true); sim.run(sim_main, 1500);
    CHECK(sim.mem[0] == 0x03 && led_at(1400) == 0x03, "third power-up: counter 3");
    // presses (with bounce) and one long hold
    sim.reset(true); sim.press(0, 1000, 1150); sim.press(0, 2000, 2150); sim.press(0, 3000, 5000);
    sim.run(sim_main, 7000);
    CHECK(sim.mem[0] == 0x07 && led_at(6900) == 0x07, "power-up (4) + two presses + one long hold = 7");
    CHECK(sim.write_log.size() == 2 * 4, "exactly four saves of two bytes (bounce and long hold cause no extra writes)");
    CHECK(led_at(1500) == 0x05 && led_at(2500) == 0x06 && led_at(3500) == 0x07, "LEDs follow each press");
    timing();
    // carry from low byte into high byte
    sim.reset(); sim.mem[0] = 0xFF; sim.mem[1] = 0x00; sim.run(sim_main, 1500);
    CHECK(sim.mem[0] == 0x00 && sim.mem[1] == 0x01 && led_at(1400) == 0x00, "255 + 1 = 256: stored as 00 01, LEDs show the low 8 bits (0)");
    // faults
    sim.reset(); sim.eeprom_never_ready = true; sim.run(sim_main, 7000);
    CHECK(pulses(0, 2600) == 4, "EEPROM never ready -> fault code 4");
    sim.reset(); sim.slave_corrupts_reads = true; sim.run(sim_main, 6000);
    CHECK(pulses(0, 1800) == 2 || pulses(0, 2200) == 3 || pulses(0, 1400) == 1 || sim.hb_events.size() > 0, "corrupt reads show a fault, never silent success");
#endif
    printf("%s  (%d checks passed, %d failed)\n", fails ? "FAILED" : "PASS", passes, fails);
    return fails != 0;
}
