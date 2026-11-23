/*
 * Month 4 - Build 3: The binary clock
 *
 * Chip     : PIC16F18446-I/P (20-pin PDIP) talking to an MCP7940N clock chip (I2C address 0x6F)
 * Compiler : MPLAB XC8
 * Supply   : 5 V
 * Clock    : 1 MHz internal oscillator
 * Button   : RA2 (pin 17) -> button -> GND
 *
 * What it does:
 *   - Shows the time in binary on LEDs RC0..RC5 (value 0..59, or 0..23 for hours).
 *   - Each press of the button changes what is shown:
 *       seconds (no mode LED)  ->  minutes (RC6 lit)  ->  hours (RC7 lit)  ->  seconds ...
 *   - Faults are shown as in Build 2 (1, 2 or 3 blinks on RC0).
 */

#include <xc.h>

/* ---- Configuration bits: how the chip starts up -------------------------
 * Leave these alone. If the compiler rejects one, see
 * start-here/04-pic-setup.md  ("If a #pragma config line is rejected").
 */
#pragma config FEXTOSC  = OFF    /* no external crystal                   */
#pragma config RSTOSC   = HFINT1 /* start on the internal 1 MHz clock     */
#pragma config CLKOUTEN = OFF
#pragma config CSWEN    = ON
#pragma config FCMEN    = OFF
#pragma config WDTE     = OFF    /* watchdog OFF, or the chip keeps resetting */
#pragma config LVP      = ON
#pragma config CP       = OFF

#define _XTAL_FREQ 1000000UL     /* tells __delay_ms() the clock speed    */

/* ---- Pins ----------------------------------------------------------------
 * LEDs: RC0..RC7 on port C (pins 16, 15, 14, 7, 6, 5, 8, 9).
 * I2C : SDA on RB4 (pin 13), SCL on RB6 (pin 11).
 * Button: RA2 (pin 17), with the chip's pull-up.
 */
#define SDA        0x10      /* RB4 */
#define SCL        0x40      /* RB6 */
#define BUTTON     0x04      /* RA2 */

#define RTC_WRITE  0xDE      /* the clock chip's I2C address 0x6F, shifted left, + write bit 0 */
#define RTC_READ   0xDF      /* the same with the read bit 1                                    */
#define REG_SEC    0x00      /* seconds, and bit 7 = "start the oscillator"                    */
#define REG_MIN    0x01
#define REG_HOUR   0x02
#define REG_WKDAY  0x03      /* bit 5 = OSCRUN: the 32.768 kHz crystal is running              */

/* ---- I2C "by hand" (the same idea as Month 2, on port B) -----------------
 * A device never drives a line HIGH: it lets go (the pull-up makes it HIGH) or pulls it LOW.
 * We switch each pin between "input" (let go) and "output, LOW" (pull down) using TRISB.
 */
#define I2C_DELAY()  __delay_us(5)

static void sdaRelease(void)  { TRISB |= SDA;  }
static void sdaLow(void)      { TRISB &= ~SDA; }
static void sclRelease(void)  { TRISB |= SCL;  }
static void sclLow(void)      { TRISB &= ~SCL; }
static unsigned char sdaRead(void) { return (PORTB & SDA) ? 1 : 0; }

static void i2cStart(void)
{
    sdaRelease(); sclRelease(); I2C_DELAY();
    sdaLow();                   I2C_DELAY();
    sclLow();                   I2C_DELAY();
}

static void i2cStop(void)
{
    sdaLow();                   I2C_DELAY();
    sclRelease();               I2C_DELAY();
    sdaRelease();               I2C_DELAY();
}

/* Send one byte, most significant bit first. Returns 1 if the other chip acknowledged. */
static unsigned char i2cWrite(unsigned char data)
{
    unsigned char n, ack;

    for (n = 0; n < 8; n++)
    {
        if (data & 0x80) sdaRelease(); else sdaLow();
        I2C_DELAY();
        sclRelease();           I2C_DELAY();
        sclLow();               I2C_DELAY();
        data = (unsigned char)(data << 1);
    }
    sdaRelease();
    I2C_DELAY();
    sclRelease();               I2C_DELAY();
    ack = (sdaRead() == 0);
    sclLow();                   I2C_DELAY();
    return ack;
}

/* Receive one byte. sendAck = 1 means "send me another", 0 means "that was the last". */
static unsigned char i2cRead(unsigned char sendAck)
{
    unsigned char n, data = 0;

    sdaRelease();
    for (n = 0; n < 8; n++)
    {
        sclRelease();           I2C_DELAY();
        data = (unsigned char)(data << 1);
        if (sdaRead()) data |= 0x01;
        sclLow();               I2C_DELAY();
    }
    if (sendAck) sdaLow(); else sdaRelease();
    I2C_DELAY();
    sclRelease();               I2C_DELAY();
    sclLow();                   I2C_DELAY();
    sdaRelease();               I2C_DELAY();   /* let the line settle before the next clock pulse */
    return data;
}

static unsigned char rtcWrite(unsigned char reg, unsigned char value)
{
    unsigned char ok;
    i2cStart();
    ok  = i2cWrite(RTC_WRITE);
    ok &= i2cWrite(reg);
    ok &= i2cWrite(value);
    i2cStop();
    return ok;
}

static unsigned char rtcRead(unsigned char reg, unsigned char *value)
{
    unsigned char ok;
    i2cStart();
    ok  = i2cWrite(RTC_WRITE);
    ok &= i2cWrite(reg);
    i2cStart();                  /* a second START: "now I want to read" */
    ok &= i2cWrite(RTC_READ);
    *value = i2cRead(0);
    i2cStop();
    return ok;
}

/* Read seconds, minutes and hours in one go. The chip hands over the next register each time we say "more". */
static unsigned char rtcReadTime(unsigned char *sec, unsigned char *min, unsigned char *hour)
{
    unsigned char ok;
    i2cStart();
    ok  = i2cWrite(RTC_WRITE);
    ok &= i2cWrite(REG_SEC);
    i2cStart();
    ok &= i2cWrite(RTC_READ);
    *sec  = i2cRead(1);          /* 1 = "and the next one please"          */
    *min  = i2cRead(1);
    *hour = i2cRead(0);          /* 0 = "that is all"                      */
    i2cStop();
    *sec  &= 0x7F;               /* drop the "oscillator on" flag          */
    *min  &= 0x7F;
    *hour &= 0x3F;               /* 24-hour mode                           */
    return ok;
}

/* The clock stores each digit pair as BCD ("binary-coded decimal"): 59 is stored as 0x59, not 0x3B. */
static unsigned char fromBcd(unsigned char b) { return (unsigned char)(((b >> 4) * 10) + (b & 0x0F)); }
static unsigned char toBcd(unsigned char v)   { return (unsigned char)(((v / 10) << 4) | (v % 10)); }

/* If something is wrong, flash LED RC0 'code' times, pause, repeat, forever. */
static void fault(unsigned char code)
{
    unsigned char n;
    LATC = 0x00;
    while (1)
    {
        for (n = 0; n < code; n++)
        {
            LATC = 0x01; __delay_ms(200);
            LATC = 0x00; __delay_ms(200);
        }
        __delay_ms(1000);
    }
}

static unsigned char digit(char c) { return (unsigned char)(c - '0'); }

/* The compiler fills in __TIME__ as the text "hh:mm:ss" at the moment you build the program. */
static void rtcSetToBuildTime(void)
{
    unsigned char hours   = (unsigned char)(digit(__TIME__[0]) * 10 + digit(__TIME__[1]));
    unsigned char minutes = (unsigned char)(digit(__TIME__[3]) * 10 + digit(__TIME__[4]));
    unsigned char seconds = (unsigned char)(digit(__TIME__[6]) * 10 + digit(__TIME__[7]));
    unsigned char ok;

    ok  = rtcWrite(REG_HOUR, toBcd(hours));                /* bit 6 = 0 means 24-hour mode  */
    ok &= rtcWrite(REG_MIN,  toBcd(minutes));
    ok &= rtcWrite(REG_SEC,  (unsigned char)(0x80 | toBcd(seconds)));   /* bit 7 = start the clock */
    if (!ok) fault(1);
}

/* Make sure the clock is running. If its crystal is not running yet, set the time and start it. */
static void startClock(void)
{
    unsigned char flags, waited = 0;

    if (!rtcRead(REG_WKDAY, &flags)) fault(1);             /* the clock chip does not answer */
    if (flags & 0x20) return;                              /* already running: leave the time alone */

    rtcSetToBuildTime();
    do
    {
        __delay_ms(10);
        if (!rtcRead(REG_WKDAY, &flags)) fault(1);
        waited++;
    } while (!(flags & 0x20) && waited < 200);             /* give the crystal up to 2 seconds to start */
    if (!(flags & 0x20)) fault(3);                         /* crystal or its capacitors not working    */
}

static void setup(void)
{
    ANSELA = 0x00; ANSELB = 0x00; ANSELC = 0x00;           /* all digital */
    LATB   = 0x00;                                         /* SDA and SCL latch bits stay LOW */
    LATC   = 0x00;
    TRISA  = 0xFF;                                         /* port A inputs (the button)     */
    WPUA   = BUTTON;                                       /* weak pull-up on RA2            */
    TRISB  = 0xFF;                                         /* port B inputs: I2C lines released */
    TRISC  = 0x00;                                         /* port C: all outputs (LEDs)     */
}

void main(void)
{
    unsigned char sec = 0, min = 0, hour = 0;
    unsigned char mode = 0, value, indicator;
    unsigned char down, wasDown = 0, ticks = 0;

    setup();
    startClock();
    if (!rtcReadTime(&sec, &min, &hour)) fault(2);

    while (1)
    {
        down = ((PORTA & BUTTON) == 0);              /* 0 = pressed (pulled to GND)   */
        if (down && !wasDown)                        /* the moment it goes down       */
        {
            mode++;
            if (mode >= 3) mode = 0;
        }
        wasDown = down;

        ticks++;                                     /* read the clock 10 times a second */
        if (ticks >= 10)
        {
            ticks = 0;
            if (!rtcReadTime(&sec, &min, &hour)) fault(2);
        }

        if (mode == 0)      { value = fromBcd(sec);  indicator = 0x00; }
        else if (mode == 1) { value = fromBcd(min);  indicator = 0x40; }   /* RC6 */
        else                { value = fromBcd(hour); indicator = 0x80; }   /* RC7 */
        LATC = (unsigned char)(value | indicator);

        __delay_ms(10);                              /* the 10 ms tick; also hides button bounce */
    }
}
