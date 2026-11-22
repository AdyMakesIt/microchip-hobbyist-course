/*
 * Month 1 - Build 2: A button controls the LED
 *
 * Chip     : PIC16F18857-I/SP (28-pin SPDIP)
 * Compiler : MPLAB XC8
 * Supply   : 5 V
 * Clock    : 1 MHz internal oscillator
 * LED      : RC0 (pin 11) -> 680 ohm -> LED -> GND
 * Button   : RA0 (pin 2)  -> button -> GND
 *
 * What it does: the LED is on while you hold the button down.
 * The chip's own weak pull-up holds RA0 HIGH until the button connects it
 * to GND, so a pressed button reads as 0 (LOW).
 */

#include <xc.h>

#pragma config FEXTOSC  = OFF
#pragma config RSTOSC   = HFINT1
#pragma config CLKOUTEN = OFF
#pragma config CSWEN    = ON
#pragma config FCMEN    = OFF
#pragma config MCLRE    = ON
#pragma config PWRTE    = OFF
#pragma config WDTE     = OFF
#pragma config LVP      = ON
#pragma config CP       = OFF

#define _XTAL_FREQ 1000000UL

#define LED     0x01             /* RC0 */
#define BUTTON  0x01             /* RA0 */

void main(void)
{
    ANSELA = 0x00;               /* ports A and C are digital             */
    ANSELC = 0x00;

    LATC   = 0x00;
    TRISC  = 0xFE;               /* RC0 is an output                      */

    TRISA  = 0xFF;               /* port A: all inputs                    */
    WPUA   = BUTTON;             /* weak pull-up on RA0 only              */

    while (1)
    {
        if ((PORTA & BUTTON) == 0)   /* 0 means the button is pressed     */
        {
            LATC |= LED;
        }
        else
        {
            LATC &= ~LED;
        }
    }
}
