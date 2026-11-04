/*
 * Month 5 - Build 3: Memory that survives power-off
 *
 * Chip     : PIC24FJ64GA002-I/SP talking to a 24LC512 I2C EEPROM (address 0x50)
 * Compiler : MPLAB XC16
 * Supply   : 3.3 V
 * Clock    : internal 8 MHz oscillator
 * Button   : RA1 (pin 3) -> button -> GND (with a 10k pull-up to 3.3 V)
 *
 * What it does:
 *   - Keeps a 16-bit counter in the EEPROM (addresses 0 and 1).
 *   - Every time the board is powered up, the counter goes up by one.
 *   - Every press of the button also adds one.
 *   - The eight LEDs show the counter's low 8 bits in binary. Unplug the power, plug it in again:
 *     the number is still there, and one higher.
 *   - Fault codes on the heartbeat LED (RA0): 1 = write failed, 2 = read failed,
 *     3 = read back the wrong value, 4 = EEPROM never finished storing.
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

/* ---- Pins ----------------------------------------------------------------
 * Heartbeat LED : RA0 (pin 2)
 * Button        : RA1 (pin 3), with an external 10k pull-up to 3.3 V
 * I2C           : SCL on RB8 (pin 17), SDA on RB9 (pin 18)
 * Eight LEDs    : RB2, RB3, RB10, RB11, RB12, RB13, RB14, RB15 (bit 0 .. bit 7)
 */
#define HEARTBEAT  0x0001    /* RA0, on LATA                       */
#define BUTTON     0x0002    /* RA1, on PORTA                      */
#define SCL        0x0100    /* RB8                                */
#define SDA        0x0200    /* RB9                                */
#define LED_MASK   0xFC0C    /* the eight LED pins on port B       */

/* Show an 8-bit value on the eight LEDs. Bits 0 and 1 go to RB2 and RB3; bits 2..7 go to RB10..RB15. */
static void showLeds(unsigned char value)
{
    unsigned int bits = (unsigned int)((value & 0x03) << 2) | (unsigned int)((unsigned int)(value >> 2) << 10);
    LATB = (unsigned int)((LATB & ~LED_MASK) | bits);
}

/* ---- I2C "by hand" (the same routines as Months 2 and 4, on port B) ------ */
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
    sdaRelease();               I2C_DELAY();
    return data;
}

/* ---- The 24LC512 EEPROM (I2C address 0x50: its A0, A1, A2 pins are wired to GND) ---- */
#define EE_WRITE  0xA0
#define EE_READ   0xA1

/* Write 'count' bytes starting at a 16-bit address. All bytes must lie in the same 128-byte page.
 * Returns 1 if every byte was acknowledged. The chip then needs up to 5 ms to store them. */
static unsigned char eeWrite(unsigned int address, const unsigned char *data, unsigned char count)
{
    unsigned char ok, i;

    i2cStart();
    ok  = i2cWrite(EE_WRITE);
    ok &= i2cWrite((unsigned char)(address >> 8));       /* the address is 16 bits: high byte first */
    ok &= i2cWrite((unsigned char)(address & 0xFF));
    for (i = 0; i < count; i++) ok &= i2cWrite(data[i]);
    i2cStop();
    return ok;
}

/* While the chip is storing data it does not answer its address. "ACK polling": keep knocking until it answers. */
static unsigned char eeWaitReady(void)
{
    unsigned char tries, ack;

    for (tries = 0; tries < 50; tries++)
    {
        i2cStart();
        ack = i2cWrite(EE_WRITE);
        i2cStop();
        if (ack) return 1;
        __delay_us(200);
    }
    return 0;                                          /* still busy after about 15 ms: something is wrong */
}

/* Read 'count' bytes starting at a 16-bit address. */
static unsigned char eeRead(unsigned int address, unsigned char *data, unsigned char count)
{
    unsigned char ok, i;

    i2cStart();
    ok  = i2cWrite(EE_WRITE);
    ok &= i2cWrite((unsigned char)(address >> 8));
    ok &= i2cWrite((unsigned char)(address & 0xFF));
    i2cStart();                                        /* a second START: "now I want to read" */
    ok &= i2cWrite(EE_READ);
    for (i = 0; i < count; i++) data[i] = i2cRead((unsigned char)(i < count - 1));
    i2cStop();
    return ok;
}

/* If something is wrong, flash the heartbeat LED 'code' times, pause, repeat, forever. */
static void fault(unsigned char code)
{
    unsigned char n;

    showLeds(0x00);
    while (1)
    {
        for (n = 0; n < code; n++)
        {
            LATA |= HEARTBEAT;  __delay_ms(200);
            LATA &= ~HEARTBEAT; __delay_ms(200);
        }
        __delay_ms(1000);
    }
}

static void setup(void)
{
    CLKDIV   = 0x0000;           /* run the internal oscillator at its full 8 MHz        */
    AD1PCFG  = 0xFFFF;           /* every pin digital (a 1 means "digital" on this chip) */
    LATA     = 0x0000;
    LATB     = 0x0000;           /* SDA and SCL latch bits stay LOW                      */
    TRISA    = 0xFFFE;           /* RA0 (heartbeat) is an output, the rest inputs        */
    TRISB    = (unsigned int)~LED_MASK;   /* LED pins are outputs; the I2C pins are released inputs */
}

/* Store the counter in the EEPROM (low byte first), wait for the chip to finish, then read it back to check. */
static void saveCounter(unsigned int counter)
{
    unsigned char bytes[2], check[2];

    bytes[0] = (unsigned char)(counter & 0xFF);
    bytes[1] = (unsigned char)(counter >> 8);

    if (!eeWrite(0x0000, bytes, 2)) fault(1);          /* both bytes are in the same page, so one write is enough */
    if (!eeWaitReady())             fault(4);
    if (!eeRead(0x0000, check, 2))  fault(2);
    if (check[0] != bytes[0] || check[1] != bytes[1]) fault(3);
}

int main(void)
{
    unsigned char bytes[2];
    unsigned int  counter;
    unsigned char down, wasDown = 0, ticks = 0;

    setup();

    if (!eeRead(0x0000, bytes, 2)) fault(2);
    counter = (unsigned int)(bytes[0] | ((unsigned int)bytes[1] << 8));
    if (counter == 0xFFFF) counter = 0;                /* a brand-new EEPROM reads all 1s: start from zero */

    counter++;                                         /* one more power-up */
    saveCounter(counter);
    showLeds((unsigned char)counter);

    while (1)
    {
        down = ((PORTA & BUTTON) == 0);                /* 0 = pressed (pulled to GND)   */
        if (down && !wasDown)                          /* the moment it goes down       */
        {
            counter++;
            saveCounter(counter);
            showLeds((unsigned char)counter);
        }
        wasDown = down;

        ticks++;                                       /* heartbeat: toggle every 50 x 10 ms */
        if (ticks >= 50) { ticks = 0; LATA ^= HEARTBEAT; }

        __delay_ms(10);
    }
}
