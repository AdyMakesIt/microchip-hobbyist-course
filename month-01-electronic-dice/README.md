# Month 1 – Electronic Dice (ATmega328P and PIC16F18857)

**Time:** four or five evenings  **Chips:** ATmega328P and PIC16F18857, both free samples  **Supply:** 5 V
**Everything for this month is in this folder:** pages, pictures and code.

You will build the same pocket dice **twice, on two different chips**: press a button and seven LEDs "roll" and settle on a number from 1 to 6.
Building one project on two chips shows you what is the same (the ideas) and what is different (the tools and register names).

* The **ATmega328P** is the chip inside an Arduino Uno. Here you program it in plain C, **without the Arduino IDE**, so you see what the IDE was doing for you.
* The **PIC16F18857** is Microchip's own 8-bit family, programmed with MPLAB X and a PICkit 3.

## Two tracks

Do the **AVR track first**: it is the gentler start, especially if you have used an Arduino. Then do the **PIC track**.

| Track   | Chip          | Builds                                                                            | Programmer                   | Software                                                      |
| ------- | ------------- | --------------------------------------------------------------------------------- | ---------------------------- | ------------------------------------------------------------- |
| **AVR** | ATmega328P-PU | [1 Blink](avr-1-blink.md) · [2 Button](avr-2-button.md) · [3 Dice](avr-3-dice.md) | USBasp **or** Arduino Uno R3 | VS Code + PlatformIO ([setup](../start-here/03-avr-setup.md)) |
| **PIC** | PIC16F18857   | [1 Blink](pic-1-blink.md) · [2 Button](pic-2-button.md) · [3 Dice](pic-3-dice.md) | PICkit 3                     | MPLAB X + XC8 ([setup](../start-here/04-pic-setup.md))        |

Each build ends with a **pass check**. Do not move on until it passes.

**The two tracks share one board layout.** The LED bank (columns 25 to 31) and the push button (column 3) are in the same place for both.
When you move from the AVR track to the PIC track you keep the LEDs, resistors and button, and replace only the chip, its power and programming leads, and the wires from the chip.

## What you need

### Free samples (order these in month 1)

| Part                                | Order | Used for      |
| ----------------------------------- | ----: | ------------- |
| **ATmega328P-PU** (28-pin PDIP)     |     3 | the AVR track |
| **PIC16F18857-I/SP** (28-pin SPDIP) |     3 | the PIC track |

Order three of each: spares are useful when a chip gets damaged.

### Parts used (counted automatically; the two tracks reuse the same parts)

<!-- bom:pic+avr -->
| Part                                                                      | Value            | Qty used | Buy at least |
| ------------------------------------------------------------------------- | ---------------- | -------: | -----------: |
| Resistor                                                                  | 10 kΩ            |        1 |            2 |
| Resistor                                                                  | 680 Ω            |        7 |            9 |
| Ceramic capacitor                                                         | 100nF            |        1 |            2 |
| LED, 5 mm                                                                 | red              |        7 |            9 |
| Push button (4-leg tact switch)                                           | 6 mm             |        1 |            2 |
| Jumper wires, solid or male-to-male                                       | assorted lengths |       15 |           21 |
| Female-to-male Dupont leads (ISP programmer / PICkit 3 ICSP → breadboard) |                  |        5 |            6 |
<!-- /bom -->

### Tools

* Solderless breadboard (830 points) and a 5 V breadboard power supply (MB102 style, or any clean 5 V USB supply)
* **For the AVR track:** a **USBasp** *or* an **Arduino Uno R3** to use as a programmer
* **For the PIC track:** a **PICkit 3** (original or clone) and its USB cable
* Multimeter
* A computer with VS Code (AVR) and MPLAB X (PIC) set up as described in the setup pages

## Before you start

1. Read [How the course works](../start-here/01-how-the-course-works.md) (5 minutes).
2. Do [AVR software and programmer setup](../start-here/03-avr-setup.md). The PIC setup can wait until you reach the PIC track.
3. Skim [Electronics and breadboard basics](../start-here/05-electronics-and-breadboard-basics.md) if you have not used a breadboard before.

## Optional: Part B, build your own AVR programmer

After both tracks, you can turn a second ATmega328P into a programmer yourself and use it to program a third. This teaches crystals, fuses, bootloaders and the ISP connection.
See [Part B](avr-programmer/README.md). Skip it if you would rather move on.

**Status:** the logic of all six programs has been tested in simulation (see
[`../maintainer/VERIFICATION_LOG.md`](../maintainer/VERIFICATION_LOG.md)). The wiring in the pictures has been machine-checked against the schematics.
Nothing here has been built on a real bench yet. If something does not work, that is useful information, so please report it.

## Folder contents

```text
month-01-electronic-dice/
  README.md                this page
  avr-1-blink.md ...       one page per AVR build
  pic-1-blink.md ...       one page per PIC build
  avr-programmer/          optional Part B: build an AVR programmer (its own pages, pictures, code)
  images/                  schematic + breadboard picture for every build (avr-N-..., pic-N-...)
  code/
    avr-1-blink/main.c     one complete file per build
    avr-2-button/main.c
    avr-3-dice/main.c
    pic-1-blink/main.c
    pic-2-button/main.c
    pic-3-dice/main.c
```
