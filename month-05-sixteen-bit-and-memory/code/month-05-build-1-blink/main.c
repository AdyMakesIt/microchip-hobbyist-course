/*
 * Month 5 - Build 1: Blink at 3.3 V
 *
 * Chip     : PIC24FJ64GA002-I/SP (28-pin SPDIP, 16-bit)
 * Compiler : MPLAB XC16
 * Supply   : 3.3 V   (set your breadboard supply to 3.3 V BEFORE connecting the chip)
 * Clock    : internal 8 MHz oscillator (4 MHz instruction clock)
 * LED      : RA0 (pin 2) -> 330 ohm -> LED -> GND
 *
 * What it does: LED on for half a second, off for half a second, forever.
 * Ten blinks should take about ten seconds.
 */

#include <xc.h>

/* ---- Configuration bits: how the chip starts up -------------------------
 * Leave these alone. If the compiler rejects one, see
 * start-here/04-pic-setup.md  ("If a #pragma config line is rejected").
 */
#pragma config JTAGEN   = OFF    /* JTAG off: its pins are free for other uses   */
#pragma config GCP      = OFF    /* no code protection                           */
#pragma config GWRP     = OFF    /* no write protection                          */
#pragma config ICS      = PGx1   /* programmer on PGEC1 / PGED1 (pins 5 and 4)   */
#pragma config FWDTEN   = OFF    /* watchdog OFF, or the chip keeps resetting    */
#pragma config WINDIS   = OFF
#pragma config FWPSA    = PR32
#pragma config WDTPS    = PS1
#pragma config POSCMOD  = NONE   /* no external crystal                          */
#pragma config OSCIOFNC = ON
#pragma config FCKSM    = CSDCMD
#pragma config FNOSC    = FRC    /* start on the internal 8 MHz oscillator       */

#define FCY 4000000UL            /* instruction clock: 8 MHz / 2 = 4 MHz          */
#include <libpic30.h>            /* provides __delay_ms() and __delay_us()        */

#define HEARTBEAT  0x0001    /* RA0 */

int main(void)
{
    CLKDIV  = 0x0000;            /* run the internal oscillator at its full 8 MHz        */
    AD1PCFG = 0xFFFF;            /* every pin digital (a 1 means "digital" on this chip) */
    LATA    = 0x0000;            /* every output starts LOW (LED off)                    */
    TRISA   = 0xFFFE;            /* bit 0 = 0 -> RA0 is an output, the rest inputs       */

    while (1)
    {
        LATA |= HEARTBEAT;       /* LED on  */
        __delay_ms(500);
        LATA &= ~HEARTBEAT;      /* LED off */
        __delay_ms(500);
    }
}
