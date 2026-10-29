// Stand-in for avr-libc's <avr/io.h> for the ATmega328P logic tests. PC use only.
#pragma once
#include <cstdint>
void sim_reg_written(int which);
uint8_t sim_pinc();
struct Reg8 {
    uint8_t v; int id;
    Reg8(int i = 0) : v(0), id(i) {}
    operator uint8_t() const { return v; }
    Reg8& operator=(int x)  { v = (uint8_t)x;  sim_reg_written(id); return *this; }
    Reg8& operator|=(int x) { v |= (uint8_t)x; sim_reg_written(id); return *this; }
    Reg8& operator&=(int x) { v &= (uint8_t)x; sim_reg_written(id); return *this; }
    Reg8& operator^=(int x) { v ^= (uint8_t)x; sim_reg_written(id); return *this; }
};
extern Reg8 DDRC, PORTC, DDRD, PORTD;
#define PINC sim_pinc()
enum { PC0 = 0, PC1, PC2, PC3, PC4, PC5, PC6 };
enum { PD0 = 0, PD1, PD2, PD3, PD4, PD5, PD6, PD7 };
