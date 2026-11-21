#pragma once
#include "sim_core.h"
#include <cstdio>
#include <cmath>
extern "C++" void sim_main(void);
static int g_fail = 0, g_pass = 0;
#define CHECK(cond, msg) do { if (cond) { g_pass++; } else { g_fail++; printf("  FAIL: %s\n", msg); } } while (0)
static void report_timing() {
    CHECK(sim.errors.empty(), "no I2C protocol errors");
    for (auto& e : sim.errors) printf("    %s\n", e.c_str());
    CHECK(sim.min_scl_low  >= 4.7, "SCL low time >= 4.7 us (I2C standard mode)");
    CHECK(sim.min_scl_high >= 4.0, "SCL high time >= 4.0 us");
    CHECK(sim.min_start_setup >= 4.7, "START set-up >= 4.7 us");
    CHECK(sim.min_start_hold  >= 4.0, "START hold >= 4.0 us");
    CHECK(sim.min_stop_setup  >= 4.0, "STOP set-up >= 4.0 us");
    CHECK(sim.min_data_setup  >= 0.25,"data set-up >= 250 ns");
}
// toggles of the heartbeat LED: returns times (ms) of every change
static std::vector<double> led_times() { std::vector<double> r; for (auto& e : sim.led_events) r.push_back(e.t / 1000.0); return r; }
static bool near(double a, double b, double tol) { return std::fabs(a - b) <= tol; }
