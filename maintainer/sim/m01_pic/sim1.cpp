#include "xc.h"
#include "sim1.h"
#include <algorithm>
Reg8 TRISA(1), TRISC(2), LATA(3), LATC(4), ANSELA(5), ANSELC(6), WPUA(7);
Sim1 sim1;
struct Tr { uint64_t t; int s; };
static std::vector<Tr> tr; static size_t tn = 0;
void sim_reg_written(int which) {
    if (which == 4) sim1.latc_events.push_back({sim1.now_us, LATC.v});
}
uint8_t sim_porta() {
    sim_delay_us(20);   // one polling-loop iteration takes ~20 us at 1 MHz; this also lets simulated time pass
    // RA0 is an input with weak pull-up: HIGH unless the button pulls it LOW.
    // With NO pull-up and button open the pin would float; we model that as LOW so a missing pull-up is caught.
    uint8_t v = 0;
    bool input = TRISA.v & 1, pullup = WPUA.v & 1, digital = !(ANSELA.v & 1);
    if (input && digital) v = sim1.pressed ? 0 : (pullup ? 1 : 0);
    return v;
}
void sim_delay_us(unsigned long us) {
    uint64_t target = sim1.now_us + us;
    while (tn < tr.size() && tr[tn].t <= target) { sim1.pressed = tr[tn].s; tn++; }
    sim1.now_us = target;
    if (sim1.now_us >= sim1.end_us) throw SimEnd1();
}
void Sim1::reset() {
    now_us = 0; pressed = 0; latc_events.clear(); tr.clear(); tn = 0;
    TRISA.v = TRISC.v = 0xFF; LATA.v = LATC.v = 0; ANSELA.v = ANSELC.v = 0xFF; WPUA.v = 0;
}
void Sim1::press(uint64_t down_ms, uint64_t up_ms) {
    uint64_t d = down_ms * 1000, u = up_ms * 1000;
    uint64_t dd[] = {0, 300, 700, 1500}; int ds[] = {1, 0, 1, 1};
    for (int i = 0; i < 4; i++) tr.push_back({d + dd[i], ds[i]});
    uint64_t uu[] = {0, 400, 900, 1700}; int us[] = {0, 1, 0, 0};
    for (int i = 0; i < 4; i++) tr.push_back({u + uu[i], us[i]});
    std::sort(tr.begin(), tr.end(), [](const Tr& a, const Tr& b) { return a.t < b.t; });
}
void Sim1::run(void (*entry)(void), uint64_t ms) { end_us = ms * 1000; try { entry(); } catch (SimEnd1&) {} }
