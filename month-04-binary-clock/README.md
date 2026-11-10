# Month 4 – The Binary Clock (PIC16F18446 and MCP7940N)

**Time:** three or four evenings  **Chips:** PIC16F18446 and MCP7940N, both free samples  **Supply:** 5 V
**Everything for this month is in this folder:** pages, pictures and code.

This month has two ideas.

1. **Moving a program to a different chip in the same family.** You met the PIC16F18857 in Month 1. The PIC16F18446 is a smaller cousin (20 pins instead of 28). Build 1 moves the Month 1 blink program across and shows exactly what changes and what does not.
2. **A real-time clock.** The MCP7940N keeps the time (seconds, minutes, hours) using a tiny 32.768 kHz watch crystal. The PIC asks it the time over I2C and shows it in **binary** on eight LEDs.

## The three builds

Do them in order. Each ends with a **pass check**.

| #   | Build                                            | You add                                    | You prove                                            |
| :-: | ------------------------------------------------ | ------------------------------------------ | ---------------------------------------------------- |
|  1  | [Blink on a new chip](build-1-blink.md)          | the PIC16F18446, programmer leads, one LED | you can move a program to another chip of the family |
|  2  | [Meet the real-time clock](build-2-rtc-hello.md) | the MCP7940N, its crystal, five more LEDs  | the clock keeps time and the PIC can read it         |
|  3  | [The binary clock](build-3-binary-clock.md)      | two mode LEDs and a button                 | the finished clock                                   |

**Status:** the logic of all three programs, including the I2C conversation with a simulated clock chip (oscillator start, BCD times, minute and midnight rollover),
has been tested (see [`../maintainer/VERIFICATION_LOG.md`](../maintainer/VERIFICATION_LOG.md)). The wiring pictures are machine-checked against the schematics.
Nothing here has been run on a real bench yet. If something does not work, that is useful information, so please report it.

## What you need

### Free samples (order these in month 4)

| Part                              | Order | Used for            |
| --------------------------------- | ----: | ------------------- |
| **PIC16F18446-I/P** (20-pin PDIP) |     3 | the main chip       |
| **MCP7940N-I/P** (8-pin PDIP)     |     3 | the real-time clock |

### Parts used (counted automatically from the circuit)

<!-- bom -->
| Part                                                     | Value            | Qty used | Buy at least |
| -------------------------------------------------------- | ---------------- | -------: | -----------: |
| Resistor                                                 | 10 kΩ            |        1 |            2 |
| Resistor                                                 | 4.7 kΩ           |        2 |            3 |
| Resistor                                                 | 680 Ω            |        8 |           10 |
| Ceramic capacitor                                        | 100nF            |        2 |            3 |
| Ceramic capacitor                                        | 10pF             |        2 |            3 |
| Crystal                                                  | 32.768kHz        |        1 |            2 |
| LED, 5 mm                                                | red              |        8 |           10 |
| Push button (4-leg tact switch)                          | 6 mm             |        1 |            2 |
| Jumper wires, solid or male-to-male                      | assorted lengths |       23 |           29 |
| Female-to-male Dupont leads (PICkit 3 ICSP → breadboard) |                  |        5 |            6 |
<!-- /bom -->

**The crystal and its two capacitors matter.** The MCP7940N needs a **32.768 kHz "watch" crystal** (the little cylinder kind, two legs) and, according to its datasheet,
**two external load capacitors** on its crystal pins. Choose a crystal rated for a **6 pF or 9 pF** load. The ceramic capacitors in this circuit are **10 pF**; the clock will still run if
yours differ a little, but it may gain or lose a few seconds a day. Accuracy is not important for this month.

### Optional

A **CR2032 coin cell with a holder**, for keeping the time while the board is off. See "Try this" in Build 3.

## Before you start

* You need the PIC setup and the programmer leads from Month 1 ([PIC setup](../start-here/04-pic-setup.md)). The 20-pin chip is *skinny*, like the Month 1 chip.
* Build 1 compares your Month 1 program with this month's. Keep your Month 1 files handy.

## Ready-made projects and hardware files

* **Working projects:** [`projects/`](projects/README.md) holds complete, ready-to-open projects for the builds (MPLAB X).
* **Hardware files:** [`hardware/`](hardware/README.md) holds the KiCad schematic location, a **parts list** and a **connection list** you can use to design a PCB. See [Taking a project further](../start-here/07-taking-a-project-further.md).

## Folder contents

```text
month-04-binary-clock/
  README.md                          this page
  build-1-blink.md ... build-3-binary-clock.md
  images/                            schematic + breadboard picture for every build
  projects/              ready-to-open projects (see projects/README.md)
  hardware/              KiCad schematic, parts list and connection list
  code/
    build-1-blink/main.c             one complete file per build
    build-2-rtc-hello/main.c
    build-3-binary-clock/main.c
```
