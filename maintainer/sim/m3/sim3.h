#pragma once
#include <cstdint>
#include <string>
#include <vector>
struct SimEnd3 {};
struct Ev { uint64_t t; int v; };
struct DacWrite { uint64_t t; int chan; int code; bool gain2x; bool active; int bits; };
struct Sim3 {
    uint64_t now_us = 0, end_us = 0;
    // analogue world (millivolts)
    int vdd_mV = 5000, pot_mV = 0, ch6_mV = 5000, ch7_mV = 0;
    bool loopback = true;                 // DAC A wired to ADC channel 1
    int miso_stuck = -1;                  // -1 normal, 0 or 1 = MISO stuck
    struct PotChange { uint64_t t; int mV; };
    std::vector<PotChange> pot_changes;
    // observations
    std::vector<Ev> latd_events, hb_events;
    std::vector<DacWrite> dac_writes;
    int dac_mV[2] = {0, 0};
    int adc_conversions = 0;
    std::vector<int> adc_channels;        // channel of every conversion
    std::vector<std::string> errors;
    double min_sck_high = 1e9, min_sck_low = 1e9, min_cs_high = 1e9, min_cs_to_clk = 1e9;
    void reset(); void run(void (*entry)(void), uint64_t ms); void potAt(uint64_t ms, int mV);
};
extern Sim3 sim3;
