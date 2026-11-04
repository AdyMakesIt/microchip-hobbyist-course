// Stand-in for <xc.h> for the Month 5 logic tests (PIC24FJ64GA002). PC use only.
#pragma once
#include <cstdint>
void sim_reg_written();
uint16_t sim_portb();
uint16_t sim_porta();
struct Reg16 {
    uint16_t v;
    Reg16() : v(0) {}
    operator uint16_t() const { return v; }
    Reg16& operator=(int x)  { v = (uint16_t)x;  sim_reg_written(); return *this; }
    Reg16& operator|=(int x) { v |= (uint16_t)x; sim_reg_written(); return *this; }
    Reg16& operator&=(int x) { v &= (uint16_t)x; sim_reg_written(); return *this; }
    Reg16& operator^=(int x) { v ^= (uint16_t)x; sim_reg_written(); return *this; }
};
extern Reg16 TRISA, TRISB, LATA, LATB, AD1PCFG, CLKDIV;
#define PORTB sim_portb()
#define PORTA sim_porta()
