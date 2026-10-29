/*
 * Month 1 - Build 1: Blink an LED
 *
 * Chip     : PIC16F18857-I/SP (28-pin SPDIP)
 * Compiler : MPLAB XC8
 * Supply   : 5 V
 * Clock    : 1 MHz internal oscillator
 * LED      : RC0 (pin 11) -> 680 ohm -> LED -> GND
 *
 * What it does: LED on for half a second, off for half a second, forever.
 * If you see this, the chip, the programmer and your wiring all work.
 */

#include <xc.h>

/* ---- Configuration bits: how the chip starts up -------------------------
 * Leave these alone. If the compiler rejects one, see
 * start-here/03-software-setup.md  ("If a #pragma config line is rejected").
 */
#pragma config FEXTOSC  = OFF    /* no external crystal                   */
#pragma config RSTOSC   = HFINT1 /* start on the internal 1 MHz clock     */
#pragma config CLKOUTEN = OFF
#pragma config CSWEN    = ON
#pragma config FCMEN    = OFF
#pragma config MCLRE    = ON     /* pin 1 is the reset pin                */
#pragma config PWRTE    = OFF
#pragma config WDTE     = OFF    /* watchdog OFF, or the chip keeps resetting */
#pragma config LVP      = ON
#pragma config CP       = OFF

#define _XTAL_FREQ 1000000UL     /* tells __delay_ms() the clock speed    */

#define LED  0x01                /* RC0 */

void main(void)
{
    ANSELC = 0x00;               /* make all of port C digital            */
    LATC   = 0x00;               /* every output starts LOW (LED off)     */
    TRISC  = 0xFE;               /* bit 0 = 0 -> RC0 is an output         */

    while (1)
    {
        LATC |= LED;             /* LED on  */
        __delay_ms(500);
        LATC &= ~LED;            /* LED off */
        __delay_ms(500);
    }
}
