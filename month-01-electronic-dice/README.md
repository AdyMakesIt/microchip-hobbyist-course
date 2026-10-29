# Month 1 – Electronic Dice (PIC16F18857)

**Time:** two or three evenings  **Chip:** PIC16F18857 (28-pin, free sample)  **Supply:** 5 V
**Everything for this month is in this folder:** pages, pictures and code.

You will build a pocket dice: press a button and seven LEDs "roll" and settle on a number from 1 to 6.
Along the way you learn the things every later month relies on: powering a microcontroller correctly,
programming it, switching an output, reading an input, and reading a circuit diagram.

## The three builds

Do them in order. Each build ends with a **pass check**. Do not move on until it passes.

| #   | Build                               | You add                                    | You prove                                          |
| :-: | ----------------------------------- | ------------------------------------------ | -------------------------------------------------- |
|  1  | [Blink an LED](build-1-blink.md)    | the chip, power, programmer leads, one LED | the chip, the programmer and the software all work |
|  2  | [Add the button](build-2-button.md) | one push button                            | you can read an input                              |
|  3  | [The dice](build-3-dice.md)         | six more LEDs                              | the finished project                               |

**Part B (optional):** once the dice work, you can use a second kind of chip, the **ATmega328P**, to build your own AVR programmer. See [Part B](avr-programmer/README.md).

**Status:** the logic of all three programs has been tested in simulation (see
[`../maintainer/VERIFICATION_LOG.md`](../maintainer/VERIFICATION_LOG.md)). The wiring on the
breadboard pictures has been machine-checked against the schematics. Nothing here has been built on
a real bench *in this new format* yet. If something does not work, that is useful information, so
please report it.

## What you need

### Free samples (order these in month 1)

| Part                                | Order | Used for                                                                          |
| ----------------------------------- | ----: | --------------------------------------------------------------------------------- |
| **PIC16F18857-I/SP** (28-pin SPDIP) |     3 | this month                                                                        |
| ATmega328P-PU (28-pin DIP)          |     3 | optional [Part B](avr-programmer/README.md): an AVR programmer you build yourself |

Order three of each: spares are useful when a chip gets damaged.

### Parts used (counted automatically from the circuit)

<!-- bom -->
| Part                                                     | Value            | Qty used | Buy at least |
| -------------------------------------------------------- | ---------------- | -------: | -----------: |
| Resistor                                                 | 10 kΩ            |        1 |            2 |
| Resistor                                                 | 680 Ω            |        7 |            9 |
| Ceramic capacitor                                        | 100nF            |        1 |            2 |
| LED, 5 mm                                                | red              |        7 |            9 |
| Push button (4-leg tact switch)                          | 6 mm             |        1 |            2 |
| Jumper wires, solid or male-to-male                      | assorted lengths |       14 |           20 |
| Female-to-male Dupont leads (PICkit 3 ICSP → breadboard) |                  |        5 |            6 |
<!-- /bom -->

### Tools

* Solderless breadboard (830 points) and a 5 V breadboard power supply (MB102 style, or any clean 5 V USB supply)
* **PICkit 3** (original or clone) and its USB cable
* Multimeter
* A computer with MPLAB X and XC8 installed: see [Software & programmer setup](../start-here/03-software-setup.md)

## Before you start

1. Read [How the course works](../start-here/01-how-the-course-works.md) (5 minutes).
2. Do [Software & programmer setup](../start-here/03-software-setup.md) once.
3. Skim [Electronics & breadboard basics](../start-here/04-electronics-and-breadboard-basics.md) if you have not used a breadboard before.

## Folder contents

```text
month-01-electronic-dice/
  README.md              this page
  build-1-blink.md       one page per build
  build-2-button.md
  build-3-dice.md
  images/                schematic + breadboard picture for every build (SVG and PNG)
  avr-programmer/        optional Part B: build an AVR programmer (its own pages, pictures, code)
  code/
    build-1-blink/main.c  one file per build; each build's file is complete on its own
    build-2-button/main.c
    build-3-dice/main.c
```
