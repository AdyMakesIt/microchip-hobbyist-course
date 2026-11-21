#pragma once
#include <cstdint>
#include <vector>
struct SimEnd1 {};
struct Ev1 { uint64_t t; int v; };
struct Sim1 {
    uint64_t now_us = 0, end_us = 0; int pressed = 0; std::vector<Ev1> latc_events;
    void reset(); void press(uint64_t down_ms, uint64_t up_ms); void run(void (*entry)(void), uint64_t ms);
};
extern Sim1 sim1;
