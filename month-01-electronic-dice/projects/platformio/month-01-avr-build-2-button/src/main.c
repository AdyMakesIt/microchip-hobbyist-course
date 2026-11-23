/*
 * Month 1 (ATmega328P) - Build 2: A button controls the LED
 *
 * Chip     : ATmega328P-PU (28-pin PDIP)
 * Compiler : avr-gcc (with avr-libc)
 * Supply   : 5 V
 * Clock    : internal oscillator, 1 MHz (factory setting)
 * LED      : PD0 (pin 2)  -> 680 ohm -> LED -> GND
 * Button   : PC0 (pin 23) -> button -> GND
 *
 * What it does: the LED is on while you hold the button down.
 * The chip's own pull-up resistor holds PC0 HIGH until the button connects it
 * to GND, so a pressed button reads as 0 (LOW).
 */

#ifndef F_CPU
#define F_CPU 1000000UL
#endif

#include <avr/io.h>
#include <util/delay.h>

#define LED     (1 << PD0)       /* port D, bit 0 */
#define BUTTON  (1 << PC0)       /* port C, bit 0 */

int main(void)
{
    DDRD  |= LED;                /* LED pin: output                        */

    DDRC  &= ~BUTTON;            /* button pin: input (DDR bit = 0)        */
    PORTC |= BUTTON;             /* for an INPUT, PORT bit = 1 turns on the pull-up */

    while (1)
    {
        if ((PINC & BUTTON) == 0)    /* PINC reads the pins: 0 = pressed   */
        {
            PORTD |= LED;
        }
        else
        {
            PORTD &= ~LED;
        }
    }
}
