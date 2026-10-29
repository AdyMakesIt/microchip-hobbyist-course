/*
 * Month 2 - Build 1: Blink the heartbeat LED
 *
 * Chip     : PIC18F47K42-I/P (40-pin PDIP)
 * Compiler : MPLAB XC8
 * Supply   : 5 V
 * Clock    : 64 MHz internal oscillator
 * LED      : RD0 (pin 19) -> 680 ohm -> LED -> GND
 *
 * What it does: LED on for half a second, off for half a second, forever.
 * If you see this, the chip, the programmer and the minimum circuit all work.
 * Count 10 blinks with a stopwatch: it should take about 10 seconds.
 */

#include <xc.h>

/* ---- Configuration bits: how the chip starts up -------------------------
 * Leave these alone. If the compiler rejects one, see
 * start-here/03-software-setup.md  ("If a #pragma config line is rejected").
 */
#pragma config FEXTOSC  = OFF            /* no external crystal            */
#pragma config RSTOSC   = HFINTOSC_64MHZ /* start on the internal 64 MHz   */
#pragma config CLKOUTEN = OFF
#pragma config CSWEN    = ON
#pragma config FCMEN    = OFF
#pragma config WDTE     = OFF            /* watchdog OFF, or it keeps resetting */
#pragma config LVP      = ON
#pragma config XINST    = OFF

#define _XTAL_FREQ 64000000UL            /* tells __delay_ms() the clock speed */

#define LED  0x01                        /* RD0 */

void main(void)
{
    OSCFRQ = 0x08;               /* make sure the internal clock is 64 MHz */

    ANSELD = 0x00;               /* make all of port D digital             */
    LATD   = 0x00;               /* every output starts LOW (LED off)      */
    TRISD  = 0xFE;               /* bit 0 = 0 -> RD0 is an output          */

    while (1)
    {
        LATD |= LED;             /* LED on  */
        __delay_ms(500);
        LATD &= ~LED;            /* LED off */
        __delay_ms(500);
    }
}
