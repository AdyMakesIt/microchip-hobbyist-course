/*
 * Month 1 - Build 3: Electronic dice
 *
 * Chip     : PIC16F18857-I/SP (28-pin SPDIP)
 * Compiler : MPLAB XC8
 * Supply   : 5 V
 * Clock    : 1 MHz internal oscillator
 * Button   : RA0 (pin 2) -> button -> GND
 *
 * Seven LEDs ("pips"), each with its own 680 ohm resistor, on RC0..RC6.
 * Think of them laid out like the dots on a real die:
 *
 *        TOP_LEFT   (RC0, pin 11)      TOP_RIGHT    (RC4, pin 15)
 *        MID_LEFT   (RC1, pin 12)  CENTRE (RC3, pin 14)  MID_RIGHT (RC5, pin 16)
 *        BOTTOM_LEFT(RC2, pin 13)      BOTTOM_RIGHT (RC6, pin 17)
 *
 * What it does: the centre LED flashes 3 times to say "ready". Press the
 * button and the dice "rolls" through several faces, then stops on one.
 *
 * Where does the randomness come from? While you wait, the chip counts
 * 0,1,2,3,4,5,0,1,2... thousands of times a second. The instant you press
 * the button is unpredictable, so the count at that instant is too.
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

#define BUTTON        0x01       /* RA0 */

/* One bit per LED on port C */
#define TOP_LEFT      0x01
#define MID_LEFT      0x02
#define BOTTOM_LEFT   0x04
#define CENTRE        0x08
#define TOP_RIGHT     0x10
#define MID_RIGHT     0x20
#define BOTTOM_RIGHT  0x40

/* Which LEDs are lit for each face. faces[3] is the pattern for a "3". */
const unsigned char faces[7] =
{
    0x00,                                                    /* (unused) */
    CENTRE,                                                  /* 1 */
    TOP_LEFT | BOTTOM_RIGHT,                                 /* 2 */
    TOP_LEFT | CENTRE | BOTTOM_RIGHT,                        /* 3 */
    TOP_LEFT | TOP_RIGHT | BOTTOM_LEFT | BOTTOM_RIGHT,       /* 4 */
    TOP_LEFT | TOP_RIGHT | BOTTOM_LEFT | BOTTOM_RIGHT | CENTRE, /* 5 */
    TOP_LEFT | MID_LEFT | BOTTOM_LEFT |
    TOP_RIGHT | MID_RIGHT | BOTTOM_RIGHT                     /* 6 */
};

unsigned char counter = 0;       /* free-running 0..5 */

void showFace(unsigned char face)
{
    LATC = faces[face];
}

void readyFlash(void)
{
    unsigned char i;
    for (i = 0; i < 3; i++)
    {
        LATC = CENTRE;
        __delay_ms(150);
        LATC = 0x00;
        __delay_ms(150);
    }
}

void rollDice(void)
{
    unsigned char step;

    for (step = 0; step < 15; step++)
    {
        counter++;
        if (counter >= 6) counter = 0;

        showFace(counter + 1);   /* counter is 0..5, faces are 1..6 */

        if (step < 9)       __delay_ms(60);    /* fast at first...      */
        else if (step < 13) __delay_ms(120);   /* ...then slowing down  */
        else                __delay_ms(240);
    }
    /* The last face shown stays lit until the next roll. */
}

void main(void)
{
    ANSELA = 0x00;
    ANSELC = 0x00;

    LATC   = 0x00;
    TRISC  = 0x80;               /* RC0..RC6 outputs, RC7 unused input */
    TRISA  = 0xFF;
    WPUA   = BUTTON;

    readyFlash();
    showFace(1);

    while (1)
    {
        counter++;               /* keep counting while we wait        */
        if (counter >= 6) counter = 0;

        if ((PORTA & BUTTON) == 0)
        {
            __delay_ms(30);                  /* wait out contact bounce  */
            if ((PORTA & BUTTON) == 0)       /* still pressed? then it is real */
            {
                rollDice();
                while ((PORTA & BUTTON) == 0)
                {
                    /* wait here until the button is released */
                }
                __delay_ms(30);
            }
        }
    }
}
