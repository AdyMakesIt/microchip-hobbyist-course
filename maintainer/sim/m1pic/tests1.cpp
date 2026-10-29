// Month 1 logic tests. Build with -DBUILD=1|2|3 against the matching main.c
#include "sim1.h"
#include "xc.h"
#include <cstdio>
#include <cmath>
#include <map>
#include <set>
extern "C++" void sim_main(void);
static int fails = 0, passes = 0;
#define CHECK(c, m) do { if (c) passes++; else { fails++; printf("  FAIL: %s\n", m); } } while (0)
static bool near(double a, double b, double tol) { return std::fabs(a - b) <= tol; }
int main() {
#if BUILD == 1
    printf("Month 1 Build 1 (blink)\n");
    sim1.reset(); sim1.run(sim_main, 5200);
    auto& e = sim1.latc_events;
    CHECK(e.size() >= 11, "LED toggles");
    bool ok = true; for (size_t i = 2; i < e.size(); i++) if (!near((e[i].t - e[i-1].t) / 1000.0, 500, 1)) ok = false;
    CHECK(ok, "500 ms on / 500 ms off");
    CHECK((TRISC.v & 1) == 0 && (ANSELC.v & 1) == 0, "RC0 is a digital output");
#elif BUILD == 2
    printf("Month 1 Build 2 (button)\n");
    sim1.reset(); sim1.press(1000, 1500); sim1.press(2000, 2100);
    sim1.run(sim_main, 3000);
    auto level = [&](double ms) { int v = 0; for (auto& e : sim1.latc_events) if (e.t / 1000.0 <= ms) v = e.v & 1; return v; };
    CHECK(level(500) == 0, "LED off before pressing");
    CHECK(level(1250) == 1, "LED on while button held");
    CHECK(level(1800) == 0, "LED off after release");
    CHECK(level(2050) == 1, "LED on during a short press");
    CHECK(level(2500) == 0, "LED off again");
    CHECK((WPUA.v & 1) == 1 && (TRISA.v & 1) == 1 && (ANSELA.v & 1) == 0, "RA0: digital input with pull-up");
#else
    printf("Month 1 Build 3 (dice)\n");
    // 60 rolls at awkward, different press times (30 ms pitch shifts so the count differs every time)
    sim1.reset();
    uint64_t t = 1500;
    for (int i = 0; i < 60; i++) { sim1.press(t, t + 80 + (i * 7) % 90); t += 2300 + (i * 37) % 211; }
    sim1.run(sim_main, t + 1000);
    const int valid[7] = {0, 0x08, 0x41, 0x49, 0x55, 0x5D, 0x77};
    auto& e = sim1.latc_events;
    // start-up: 3 centre flashes
    int flashes = 0; for (size_t i = 0; i < 6 && i < e.size(); i++) if (e[i].v == 0x08) flashes++;
    CHECK(flashes == 3, "centre LED flashes 3 times at start-up");
    // find final face of each roll: last event before the next press (gap > 1 s)
    std::map<int, int> count; int rolls = 0; bool allValid = true;
    for (size_t i = 0; i + 1 < e.size(); i++) {
        if (e[i+1].t - e[i].t > 1000000 && e[i].t > 1400000) {      // a pause of >1 s = final face of a roll
            int v = e[i].v; bool v_ok = false; for (int f = 1; f <= 6; f++) if (v == valid[f]) { v_ok = true; count[f]++; }
            if (!v_ok) allValid = false; rolls++;
        }
    }
    CHECK(allValid, "every resting pattern is a legal die face (1-6)");
    CHECK(rolls >= 55, "about 60 rolls detected");
    bool allSix = true; for (int f = 1; f <= 6; f++) if (count[f] == 0) allSix = false;
    CHECK(allSix, "all six faces occur across 60 rolls");
    int mx = 0, mn = 999; for (int f = 1; f <= 6; f++) { mx = std::max(mx, count[f]); mn = std::min(mn, count[f]); }
    printf("  face counts: "); for (int f = 1; f <= 6; f++) printf("%d:%d ", f, count[f]); printf("\n");
    CHECK(mx <= 22 && mn >= 2, "no face wildly over- or under-represented");
    // no bounce-double-rolls: number of animation bursts == number of presses
    // (each roll = 15 LATC writes; check total writes accordingly: 6 start-up + 1 + 60*15 + ...)
    size_t expect = 6 + 1 + 60 * 15;
    CHECK(e.size() >= expect - 2 && e.size() <= expect + 2, "exactly one roll per press (bounce and held button add nothing)");
#endif
    printf("%s  (%d checks passed, %d failed)\n", fails ? "FAILED" : "PASS", passes, fails);
    return fails != 0;
}
