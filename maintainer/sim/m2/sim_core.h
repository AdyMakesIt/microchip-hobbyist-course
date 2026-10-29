#pragma once
#include <cstdint>
#include <string>
#include <vector>

struct SimEnd {};

struct Event { uint64_t t; int v; };

struct Sim {
    // ---- time
    uint64_t now_us = 0, end_us = 0;
    // ---- MCP23017 model
    bool     slave_present = true;
    bool     slave_corrupts_reads = false;   // for the "fault 3" test
    bool     slave_nacks_read_address = false; // for the "fault 2" test
    uint8_t  regs[0x16];
    uint8_t  ptr = 0;
    // ---- external world
    uint8_t  pressed_mask = 0;               // buttons on MCP GPB bits (1 = pressed)
    struct Press { uint64_t t_down, t_up; int idx; bool bounce; };
    std::vector<Press> presses;
    // ---- observations
    std::vector<Event> led_events;           // RD0 changes
    std::vector<Event> olata_events;         // every value written to OLATA
    std::vector<Event> gpioa_events;         // reads that returned (for debugging)
    int      piezo_toggles = 0;
    int      reads_done = 0, writes_done = 0;
    std::vector<std::string> errors;         // protocol / timing violations
    // timing minima (microseconds)
    double min_scl_low = 1e9, min_scl_high = 1e9, min_start_setup = 1e9,
           min_start_hold = 1e9, min_stop_setup = 1e9, min_data_setup = 1e9;
    // ---- API
    void reset();
    void run(void (*entry)(void), uint64_t duration_ms);
    void press(int idx, uint64_t down_ms, uint64_t up_ms, bool bounce = true);
    uint8_t ledsOn() const;                  // which GPA LEDs are lit right now
    uint8_t lastOlata() const;
};
extern Sim sim;
