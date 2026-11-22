// Stand-in for <xc.h> for the Month 4 logic tests (PIC16F18446). PC use only.
#pragma once
#include <cstdint>
void sim_reg_written();
void sim_delay_us(unsigned long us);
uint8_t sim_portb();
uint8_t sim_porta();
struct Reg8 {
    uint8_t v;
    Reg8() : v(0) {}
    operator uint8_t() const { return v; }
    Reg8& operator=(int x)  { v = (uint8_t)x;  sim_reg_written(); return *this; }
    Reg8& operator|=(int x) { v |= (uint8_t)x; sim_reg_written(); return *this; }
    Reg8& operator&=(int x) { v &= (uint8_t)x; sim_reg_written(); return *this; }
    Reg8& operator^=(int x) { v ^= (uint8_t)x; sim_reg_written(); return *this; }
};
extern Reg8 TRISA, TRISB, TRISC, LATA, LATB, LATC, ANSELA, ANSELB, ANSELC, WPUA;
#define PORTB sim_portb()
#define PORTA sim_porta()
#define __delay_us(x) sim_delay_us((unsigned long)(x))
#define __delay_ms(x) sim_delay_us((unsigned long)(x) * 1000UL)
