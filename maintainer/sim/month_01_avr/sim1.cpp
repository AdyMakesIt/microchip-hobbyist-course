#include "avr/io.h"
#include "sim1.h"
#include <algorithm>
Reg8 DDRC(1), PORTC(2), DDRD(3), PORTD(4);
Sim1 sim1;
struct Tr { uint64_t t; int s; };
static std::vector<Tr> tr; static size_t tn = 0;
void sim_reg_written(int which) { if (which == 4) sim1.portd_events.push_back({sim1.now_us, PORTD.v}); }
void sim_delay_us(unsigned long us) {
    uint64_t target = sim1.now_us + us;
    while (tn < tr.size() && tr[tn].t <= target) { sim1.pressed = tr[tn].s; tn++; }
    sim1.now_us = target;
    if (sim1.now_us >= sim1.end_us) throw SimEnd1();
}
uint8_t sim_pinc() {
    sim_delay_us(20);                       // one polling-loop pass takes about 20 us at 1 MHz
    // PC0: button to GND. With the pin an INPUT and PORTC bit set, the pull-up is on (reads 1).
    // Without the pull-up an open button would float; model as 0 so a missing pull-up is caught.
    uint8_t v = 0;
    bool input = !(DDRC.v & 1), pullup = (PORTC.v & 1);
    if (input) v = sim1.pressed ? 0 : (pullup ? 1 : 0);
    return v;
}
void Sim1::reset() { now_us = 0; pressed = 0; portd_events.clear(); tr.clear(); tn = 0; DDRC.v = DDRD.v = PORTC.v = PORTD.v = 0; }
void Sim1::press(uint64_t down_ms, uint64_t up_ms) {
    uint64_t d = down_ms * 1000, u = up_ms * 1000;
    uint64_t dd[] = {0, 300, 700, 1500}; int ds[] = {1, 0, 1, 1};
    for (int i = 0; i < 4; i++) tr.push_back({d + dd[i], ds[i]});
    uint64_t uu[] = {0, 400, 900, 1700}; int us[] = {0, 1, 0, 0};
    for (int i = 0; i < 4; i++) tr.push_back({u + uu[i], us[i]});
    std::sort(tr.begin(), tr.end(), [](const Tr& a, const Tr& b) { return a.t < b.t; });
}
void Sim1::run(int (*entry)(void), uint64_t ms) { end_us = ms * 1000; try { entry(); } catch (SimEnd1&) {} }
