// Stand-in for XC16's <libpic30.h> (delay functions). PC use only.
#pragma once
void sim_delay_us(unsigned long us);
#define __delay_us(x) sim_delay_us((unsigned long)(x))
#define __delay_ms(x) sim_delay_us((unsigned long)(x) * 1000UL)
