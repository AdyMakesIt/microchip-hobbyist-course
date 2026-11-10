/*
 * Month 1 (ATmega328P) - Build 1: Blink an LED
 *
 * Chip     : ATmega328P-PU (28-pin PDIP)
 * Compiler : avr-gcc (with avr-libc)
 * Supply   : 5 V
 * Clock    : internal oscillator, 1 MHz (the chip's factory setting: no crystal needed)
 * LED      : PD0 (pin 2) -> 680 ohm -> LED -> GND
 *
 * What it does: LED on for half a second, off for half a second, forever.
 * If you see this, the chip, the programmer and your wiring all work.
 */

#ifndef F_CPU                    /* (the build tool may already have set it) */
#define F_CPU 1000000UL          /* tells _delay_ms() the clock speed: 1 MHz */
#endif

#include <avr/io.h>
#include <util/delay.h>

#define LED  (1 << PD0)          /* a mask with only bit 0 set (port D) */

int main(void)
{
    DDRD |= LED;                 /* DDRD: a 1 bit makes the pin an OUTPUT */

    while (1)
    {
        PORTD |= LED;            /* LED on  (PORTD sets the output level) */
        _delay_ms(500);
        PORTD &= ~LED;           /* LED off */
        _delay_ms(500);
    }
}
