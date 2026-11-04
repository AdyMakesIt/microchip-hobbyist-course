// Stand-in for <xc.h> for the Month 3 logic tests (PIC18F47K42). PC use only.
#pragma once
#include <cstdint>
void sim_reg_written(int which);
void sim_delay_us(unsigned long us);
uint8_t sim_portc();
struct Reg8 {
    uint8_t v; int id;
    Reg8(int i = 0) : v(0), id(i) {}
    operator uint8_t() const { return v; }
    Reg8& operator=(int x)  { v = (uint8_t)x;  sim_reg_written(id); return *this; }
    Reg8& operator|=(int x) { v |= (uint8_t)x; sim_reg_written(id); return *this; }
    Reg8& operator&=(int x) { v &= (uint8_t)x; sim_reg_written(id); return *this; }
    Reg8& operator^=(int x) { v ^= (uint8_t)x; sim_reg_written(id); return *this; }
};
extern Reg8 TRISB, TRISC, TRISD, LATB, LATC, LATD, ANSELB, ANSELC, ANSELD, OSCFRQ;
#define PORTC sim_portc()
#define __delay_us(x) sim_delay_us((unsigned long)(x))
#define __delay_ms(x) sim_delay_us((unsigned long)(x) * 1000UL)
