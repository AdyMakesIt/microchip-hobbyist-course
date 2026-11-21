// Stand-in for Microchip's <xc.h>, used ONLY by the logic tests on a PC.
// It lets the course's main.c run unchanged against a simulated PIC18F47K42,
// I2C bus and MCP23017.  Compile main.c as C++ (see ../README.md).
#pragma once
#include <cstdint>

void sim_reg_written();
void sim_delay_us(unsigned long us);
uint8_t sim_portc();
uint8_t sim_portd();

struct Reg8 {
    uint8_t v;
    Reg8() : v(0) {}
    operator uint8_t() const { return v; }
    Reg8& operator=(int x)  { v = (uint8_t)x;  sim_reg_written(); return *this; }
    Reg8& operator|=(int x) { v |= (uint8_t)x; sim_reg_written(); return *this; }
    Reg8& operator&=(int x) { v &= (uint8_t)x; sim_reg_written(); return *this; }
    Reg8& operator^=(int x) { v ^= (uint8_t)x; sim_reg_written(); return *this; }
};

extern Reg8 TRISC, TRISD, LATC, LATD, ANSELC, ANSELD, OSCFRQ;
#define PORTC sim_portc()
#define PORTD sim_portd()

#define __delay_us(x) sim_delay_us((unsigned long)(x))
#define __delay_ms(x) sim_delay_us((unsigned long)(x) * 1000UL)
