# Month 1 · Part B – Build your own AVR programmer (optional)

[← Month 1](../README.md)

**Time:** two or three evenings  **Do it after:** Month 1 Build 3 passes (or at any later time)  **Supply:** 5 V
**Everything for Part B is in this folder:** pages, pictures and code.

You will turn one ATmega328P chip into a small **programmer** that can load programs into other AVR chips, and then use it to program a second ATmega328P.
Along the way you learn how an AVR chip is built into a minimal working board: crystal, reset, bootloader, fuses and the
**ISP** (in-system programming) connection.

## What it can and cannot program

| It can program                                                                                                            | It cannot program                                                      |
| ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| ATmega328P and other AVR chips that use the **ISP** interface (MOSI, MISO, SCK, RESET), such as the ATtiny85 and ATtiny84 | **PIC chips**: use the PICkit 3 for those                              |
|                                                                                                                           | newer AVR chips that use **UPDI** (the "AVR Dx" and "AVR Ex" families) |

**Why build one?** A USBasp (used below to start the process) can also program AVR chips directly, and is the quicker everyday tool.
Part B is about **understanding** how a chip is programmed, and ending up with a working programmer you built yourself.
Skip it if you only want to get on with the PIC projects.

## The three builds

| #   | Build                                                     | You add                                  | You prove                                           |
| :-: | --------------------------------------------------------- | ---------------------------------------- | --------------------------------------------------- |
| B1  | [The minimum ATmega328P board](build-b1-minimum-board.md) | the chip, crystal, reset, serial lead    | the chip runs and accepts a program over USB-serial |
| B2  | [Turn it into a programmer](build-b2-programmer.md)       | two status LEDs                          | the chip is running the programmer software         |
| B3  | [Program a second chip](build-b3-program-a-chip.md)       | a second ATmega328P board and four wires | your programmer really programs another chip        |

**Status:** the wiring in the pictures is machine-checked against the schematics. The programs are Arduino's standard examples plus a ten-line blink sketch.
Nothing here has been run on a real bench yet. Please report what you find.

## What you need

### Free sample chips

Two of the **three ATmega328P-PU** chips ordered in Month 1: one becomes the programmer, one is the target. The third is a spare.

### Extra items (not free)

| Item                            | What to look for                                                                                   | Rough cost |
| ------------------------------- | -------------------------------------------------------------------------------------------------- | ---------: |
| **A way to start a blank chip** | a **USBasp** programmer (about £2–5), *or* any Arduino board you already own, used as a programmer |       £2–5 |
| **USB-to-serial (TTL) adapter** | CH340, CP2102 or FT232 type, with a **5 V** setting or jumper                                      |       £2–5 |
| Crystals                        | **16 MHz**, HC-49 type, 2 needed                                                                   |       £1–2 |
| Electrolytic capacitor          | 10 µF, one (used only if programming reports "not in sync")                                        |    pennies |

### Parts used (counted automatically from the three circuits)

<!-- bom -->
| Part                                                                       | Value            | Qty used | Buy at least |
| -------------------------------------------------------------------------- | ---------------- | -------: | -----------: |
| Resistor                                                                   | 10 kΩ            |        2 |            3 |
| Resistor                                                                   | 680 Ω            |        4 |            5 |
| Ceramic capacitor                                                          | 100nF            |        4 |            5 |
| Ceramic capacitor                                                          | 22pF             |        4 |            5 |
| Crystal, HC-49                                                             | 16MHz            |        2 |            3 |
| LED, 5 mm                                                                  | red              |        4 |            5 |
| Jumper wires, solid or male-to-male                                        | assorted lengths |       22 |           28 |
| Female-to-male Dupont leads (USB-serial adapter / USBasp ISP → breadboard) |                  |        9 |           10 |
<!-- /bom -->

### Software

**Arduino IDE** (version 2 or later), free from arduino.cc. This is separate from MPLAB X. You need no extra add-ons: the standard Arduino AVR boards are included.

## Safety rules for this part

1. **One power source.** The breadboard supply powers everything. **Do not connect the USB-serial adapter's VCC (power) lead** and do not connect the USBasp's VCC lead.
2. Set the USB-serial adapter to **5 V** signalling.
3. Power off before changing wiring.
4. Never connect the programmer's output pins to a 3.3 V chip without checking: this course only uses 5 V parts here.

## Arduino IDE settings at a glance

| Task                                             | Board       | Programmer         | Port                   | Then                                                               |
| ------------------------------------------------ | ----------- | ------------------ | ---------------------- | ------------------------------------------------------------------ |
| Burn bootloader with a USBasp (B1)               | Arduino Uno | USBasp             | (none needed)          | Tools → Burn Bootloader                                            |
| Upload a sketch to the programmer board (B1, B2) | Arduino Uno | (any)              | the USB-serial adapter | Sketch → Upload                                                    |
| Program the target (B3)                          | Arduino Uno | **Arduino as ISP** | the USB-serial adapter | Tools → Burn Bootloader, then Sketch → **Upload Using Programmer** |

(The board is called "Arduino Uno" because an ATmega328P with a 16 MHz crystal is exactly what an Uno contains.)

## Folder contents

```text
avr-programmer/
  README.md                         this page
  build-b1-minimum-board.md
  build-b2-programmer.md
  build-b3-program-a-chip.md
  images/                           schematic + breadboard picture for every build
  code/blink-d9/blink-d9.ino        the blink sketch (ArduinoISP comes with the Arduino IDE)
```
