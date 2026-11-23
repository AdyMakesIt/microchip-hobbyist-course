/*
 * Month 3 - Build 2: Add the DAC
 *
 * Chip     : PIC18F47K42-I/P with an MCP3008 (ADC) and an MCP4822 (2-channel 12-bit DAC)
 * Compiler : MPLAB XC8
 * Supply   : 5 V
 * Clock    : 64 MHz internal oscillator
 *
 * What it does (all with the same self-test and heartbeat as Build 1):
 *   - Reads the knob (ADC channel 0) and shows it as a bar graph.
 *   - DAC channel A copies the knob: measure it with a multimeter and it matches the voltage at the
 *     knob's middle leg (up to 4.095 V, the DAC's limit).
 *   - DAC channel B draws a slow triangle wave, 0 V up to 4.095 V and back, about every 2 seconds,
 *     so the LED on it slowly brightens and dims.
 */

#include <xc.h>

/* ---- Configuration bits: how the chip starts up -------------------------
 * Leave these alone. If the compiler rejects one, see
 * start-here/04-pic-setup.md  ("If a #pragma config line is rejected").
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

/* ---- Pins ----------------------------------------------------------------
 * The LED bar graph is port D: RD0 (pin 19) ... RD7 (pin 30), one LED each.
 */
#define SCK        0x01      /* RC0 (pin 15): SPI clock, to both chips        */
#define MOSI       0x02      /* RC1 (pin 16): data to the chips               */
#define MISO       0x04      /* RC2 (pin 17): data from the ADC               */
#define CS_ADC     0x08      /* RC3 (pin 18): chip select, MCP3008 (ADC)      */
#define CS_DAC     0x10      /* RC4 (pin 23): chip select, MCP4822 (DAC)      */
#define HEARTBEAT  0x01      /* RB0 (pin 33): heartbeat / fault LED, on LATB  */

/* ---- SPI "by hand" -----------------------------------------------------
 * SPI uses four wires: a clock (SCK), data out (MOSI), data in (MISO) and one
 * chip-select (CS) per chip. A chip listens only while its CS is LOW.
 * To send a byte we put each bit on MOSI (most significant first), raise SCK so
 * the chip reads it, read MISO at the same moment, then lower SCK again.
 * Unlike I2C there is no "acknowledge": a missing chip just looks like a 0 or a 1.
 */
#define SPI_DELAY()  __delay_us(1)     /* about 400 kHz: slow and forgiving */

static unsigned char spiTransfer(unsigned char out)
{
    unsigned char n, in = 0;

    for (n = 0; n < 8; n++)
    {
        if (out & 0x80) LATC |= MOSI; else LATC &= ~MOSI;
        out = (unsigned char)(out << 1);
        SPI_DELAY();
        LATC |= SCK;                   /* clock rises: the chip reads our bit    */
        SPI_DELAY();
        in = (unsigned char)(in << 1);
        if (PORTC & MISO) in |= 0x01;  /* ...and we read the bit it is sending   */
        LATC &= ~SCK;                  /* clock falls                             */
    }
    return in;
}

/* Read one channel (0 to 7) of the MCP3008. Returns 0 (0 V) to 1023 (the 5 V reference). */
static unsigned int adcRead(unsigned char channel)
{
    unsigned char high, low;

    LATC &= ~CS_ADC;                              /* select the ADC              */
    SPI_DELAY();
    spiTransfer(0x01);                            /* the START bit               */
    high = spiTransfer((unsigned char)(0x80 | (channel << 4)));  /* single-ended + channel;
                                                     the top bits of the answer come back */
    low  = spiTransfer(0x00);                     /* the rest of the answer      */
    LATC |= CS_ADC;                               /* deselect                    */
    SPI_DELAY();
    return (unsigned int)(((unsigned int)(high & 0x03) << 8) | low);
}

/* Turn a reading 0..1023 into a bar of 0..8 lit LEDs, as a bit pattern for port D. */
static unsigned char bar(unsigned int reading)
{
    unsigned char lit = (unsigned char)((reading * 9UL) / 1024UL);    /* 0 to 8 */
    return (unsigned char)((1u << lit) - 1u);                         /* 0x00 to 0xFF */
}

/* If something is wrong, flash the heartbeat LED 'code' times, pause, repeat, forever. */
static void fault(unsigned char code)
{
    unsigned char n;

    LATD = 0x00;
    while (1)
    {
        for (n = 0; n < code; n++)
        {
            LATB |= HEARTBEAT;  __delay_ms(200);
            LATB &= ~HEARTBEAT; __delay_ms(200);
        }
        __delay_ms(1000);
    }
}

/* Write a value 0..4095 to DAC channel 0 (A) or 1 (B) of the MCP4822.
 * We use its "2x gain" setting, so the output voltage is exactly 1 millivolt per step:
 * a value of 2500 gives 2.500 V (the largest value, 4095, gives 4.095 V).
 * The 16 bits are:  [A/B] [-] [gain: 0 = 2x] [on: 1] [12 bits of value]            */
static void dacWrite(unsigned char channel, unsigned int value)
{
    unsigned int word = (unsigned int)(0x1000 | (value & 0x0FFF));     /* gain 2x, output on */
    if (channel) word |= 0x8000;                                       /* channel B          */

    LATC &= ~CS_DAC;
    SPI_DELAY();
    spiTransfer((unsigned char)(word >> 8));
    spiTransfer((unsigned char)(word & 0xFF));
    LATC |= CS_DAC;                    /* the DAC output updates when CS goes HIGH */
    SPI_DELAY();
}

static void setup(void)
{
    OSCFRQ = 0x08;               /* make sure the internal clock is 64 MHz */

    ANSELB = 0x00; ANSELC = 0x00; ANSELD = 0x00;      /* all digital */
    LATB = 0x00;
    LATC = CS_ADC | CS_DAC;      /* both chip-selects HIGH (chips ignored), clock LOW */
    LATD = 0x00;
    TRISB = 0xFE;                /* RB0 (heartbeat) is an output                 */
    TRISC = 0xE4;                /* RC0, RC1, RC3, RC4 outputs; RC2 (MISO) input */
    TRISD = 0x00;                /* port D: all outputs (the bar graph)          */
}

void main(void)
{
    unsigned char ticks = 0;
    unsigned int  reading, code;
    unsigned int  wave = 0;               /* the triangle wave, 0..4095 */
    unsigned char rising = 1;

    setup();

    if (adcRead(7) > 16)   fault(1);
    if (adcRead(6) < 1007) fault(2);

    while (1)
    {
        reading = adcRead(0);
        LATD = bar(reading);

        code = (unsigned int)((reading * 5000UL) / 1024UL);   /* reading -> millivolts */
        if (code > 4095) code = 4095;                         /* the DAC cannot go higher */
        dacWrite(0, code);                                    /* A follows the knob       */

        if (rising)                                           /* B: triangle wave         */
        {
            wave += 41;
            if (wave >= 4095) { wave = 4095; rising = 0; }
        }
        else
        {
            if (wave <= 41) { wave = 0; rising = 1; }
            else wave -= 41;
        }
        dacWrite(1, wave);

        ticks++;
        if (ticks >= 50) { ticks = 0; LATB ^= HEARTBEAT; }

        __delay_ms(10);
    }
}
