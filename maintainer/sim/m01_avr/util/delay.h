#pragma once
void sim_delay_us(unsigned long us);
#define _delay_ms(x) sim_delay_us((unsigned long)((x) * 1000.0))
#define _delay_us(x) sim_delay_us((unsigned long)(x))
