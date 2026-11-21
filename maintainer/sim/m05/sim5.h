#pragma once
#include <cstdint>
#include <string>
#include <vector>
struct SimEnd {};
struct Event { uint64_t t; int v; };
struct WriteRec { uint64_t t; uint16_t addr; uint8_t value; };
struct Sim {
    uint64_t now_us = 0, end_us = 0;
    bool slave_present = true, slave_corrupts_reads = false, slave_nacks_read_address = false, eeprom_never_ready = false;
    uint8_t mem[65536]; uint64_t busy_until = 0; int page_wraps = 0; int byte_after_addr = 0;
    uint8_t pressed_mask = 0;
    struct Press { uint64_t t_down, t_up; int idx; bool bounce; };
    std::vector<Press> presses;
    std::vector<Event> led_events, hb_events;
    std::vector<WriteRec> write_log;
    int reads_done = 0;
    std::vector<std::string> errors;
    double min_scl_low = 1e9, min_scl_high = 1e9, min_start_setup = 1e9, min_start_hold = 1e9, min_stop_setup = 1e9, min_data_setup = 1e9;
    void reset(bool keep_memory = false); void run(int (*entry)(void), uint64_t duration_ms); void press(int idx, uint64_t down_ms, uint64_t up_ms, bool bounce = true);
};
extern Sim sim;
