#pragma once
#include <cstdint>
#include <string>
#include <vector>
struct SimEnd {};
struct Event { uint64_t t; int v; };
struct Sim {
    uint64_t now_us = 0, end_us = 0;
    bool slave_present = true, slave_corrupts_reads = false, slave_nacks_read_address = false, osc_dead = false, battery_preset = false;
    uint8_t regs[0x60]; uint8_t ptr = 0;
    uint8_t pressed_mask = 0;
    struct Press { uint64_t t_down, t_up; int idx; bool bounce; };
    std::vector<Press> presses;
    std::vector<Event> latc_events;
    int reads_done = 0, writes_done = 0;
    uint64_t st_set_us = 0; int set_sec = -1, set_min = -1, set_hour = -1;
    std::vector<std::string> errors;
    double min_scl_low = 1e9, min_scl_high = 1e9, min_start_setup = 1e9, min_start_hold = 1e9, min_stop_setup = 1e9, min_data_setup = 1e9;
    void reset(); void run(void (*entry)(void), uint64_t duration_ms); void press(int idx, uint64_t down_ms, uint64_t up_ms, bool bounce = true);
    void preset_running(int h, int m, int s);
};
extern Sim sim;
