/*
 * Month 1 (ATmega328P) - Build 3: Electronic dice
 *
 * Chip     : ATmega328P-PU (28-pin PDIP)
 * Compiler : avr-gcc (with avr-libc)
 * Supply   : 5 V
 * Clock    : internal oscillator, 1 MHz (factory setting)
 * Button   : PC0 (pin 23) -> button -> GND
 *
 * Seven LEDs ("pips"), each with its own 680 ohm resistor, on PD0..PD6.
 * Think of them laid out like the dots on a real die:
 *
 *        TOP_LEFT   (PD0, pin 2)       TOP_RIGHT    (PD4, pin 6)
 *        MID_LEFT   (PD1, pin 3)   CENTRE (PD3, pin 5)   MID_RIGHT (PD5, pin 11)
 *        BOTTOM_LEFT(PD2, pin 4)       BOTTOM_RIGHT (PD6, pin 12)
 *
 * What it does: the centre LED flashes 3 times to say "ready". Press the
 * button and the dice "rolls" through several faces, then stops on one.
 *
 * Where does the randomness come from? While you wait, the chip counts
 * 0,1,2,3,4,5,0,1,2... thousands of times a second. The instant you press
 * the button is unpredictable, so the count at that instant is too.
 */

#ifndef F_CPU
#define F_CPU 1000000UL
#endif

#include <avr/io.h>
#include <util/delay.h>

#define BUTTON        (1 << PC0)

/* One bit per LED on port D */
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
    PORTD = faces[face];
}

void readyFlash(void)
{
    unsigned char i;
    for (i = 0; i < 3; i++)
    {
        PORTD = CENTRE;
        _delay_ms(150);
        PORTD = 0x00;
        _delay_ms(150);
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

        if (step < 9)       _delay_ms(60);     /* fast at first...      */
        else if (step < 13) _delay_ms(120);    /* ...then slowing down  */
        else                _delay_ms(240);
    }
    /* The last face shown stays lit until the next roll. */
}

int main(void)
{
    DDRD  = 0x7F;                /* PD0..PD6 outputs, PD7 unused input  */
    PORTD = 0x00;

    DDRC  &= ~BUTTON;            /* button pin: input                   */
    PORTC |= BUTTON;             /* with its pull-up on                 */

    readyFlash();
    showFace(1);

    while (1)
    {
        counter++;               /* keep counting while we wait         */
        if (counter >= 6) counter = 0;

        if ((PINC & BUTTON) == 0)
        {
            _delay_ms(30);                   /* wait out contact bounce   */
            if ((PINC & BUTTON) == 0)        /* still pressed? then it is real */
            {
                rollDice();
                while ((PINC & BUTTON) == 0)
                {
                    /* wait here until the button is released */
                }
                _delay_ms(30);
            }
        }
    }
}
