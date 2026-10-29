# Month 2 – Workshop Command Centre (PIC18F47K42 + MCP23017)

**Time:** three or four evenings  **Chips:** PIC18F47K42 (40-pin) and MCP23017 (28-pin), both free samples  **Supply:** 5 V
**Everything for this month is in this folder:** pages, pictures and code.

You will build a small control panel: eight LEDs and two buttons driven through an **I2C port expander**,
with a beeper for feedback. The new idea this month is **I2C**: two wires that let one chip talk to many others.
You will write the I2C routines yourself (about 60 readable lines), so you can see exactly what happens on the wires.

> **Why no MCC this month?** Microchip's code generator (MCC) is powerful, but its generated function names change
> between versions, and one wrong click leaves you with code that does not compile and no clue why. For the first
> months you will write short, plain C that you can read from top to bottom. MCC comes back later, when you
> already understand what it is generating for you.

## The four builds

Do them in order. Each ends with a **pass check**.

| #   | Build                                                  | You add                                          | You prove                                    |
| :-: | ------------------------------------------------------ | ------------------------------------------------ | -------------------------------------------- |
|  1  | [Blink (minimum circuit)](build-1-blink.md)            | the chip, power, programmer leads, heartbeat LED | chip, programmer and software work           |
|  2  | [Say hello to the MCP23017](build-2-hello-expander.md) | the expander, two I2C wires, one LED             | I2C works; you can write and read a register |
|  3  | [Eight LEDs and a button](build-3-led-chase.md)        | seven more LEDs, button 1                        | writing and reading through the expander     |
|  4  | [Workshop Command Centre](build-4-command-centre.md)   | button 2, piezo                                  | the finished project                         |

**Status:** the logic of all four programs, including the I2C protocol and its timing, has been tested against a
simulated MCP23017 (see [`../maintainer/VERIFICATION_LOG.md`](../maintainer/VERIFICATION_LOG.md)). The wiring pictures have been machine-checked
against the schematics. Nothing here has been run on a real bench *in this new format* yet. If something does not work,
that is useful information, so please report it.

## What you need

### Free samples (order these in month 2)

| Part                              | Order | Used for      |
| --------------------------------- | ----: | ------------- |
| **PIC18F47K42-I/P** (40-pin PDIP) |     3 | the main chip |
| **MCP23017-E/SP** (28-pin SPDIP)  |     3 | the expander  |

Ask for the **P** (PDIP) package of the PIC18F47K42 and the **SP** (skinny) package of the MCP23017: they fit a breadboard.

### Parts used (counted automatically from the circuit)

<!-- bom -->
| Part                                                     | Value            | Qty used | Buy at least |
| -------------------------------------------------------- | ---------------- | -------: | -----------: |
| Resistor                                                 | 10 kΩ            |        2 |            3 |
| Resistor                                                 | 100 Ω            |        1 |            2 |
| Resistor                                                 | 4.7 kΩ           |        2 |            3 |
| Resistor                                                 | 680 Ω            |        9 |           11 |
| Ceramic capacitor                                        | 100nF            |        3 |            4 |
| LED, 5 mm                                                | red              |        9 |           11 |
| Push button (4-leg tact switch)                          | 6 mm             |        2 |            3 |
| Piezo disc (passive)                                     |                  |        1 |            2 |
| Jumper wires, solid or male-to-male                      | assorted lengths |       31 |           37 |
| Female-to-male Dupont leads (PICkit 3 ICSP → breadboard) |                  |        5 |            6 |
<!-- /bom -->

### Tools

Everything from Month 1 (breadboard, 5 V supply, PICkit 3, multimeter, MPLAB X + XC8 set up). Nothing else.

## Two things that are different from Month 1

1. **The PIC18F47K42 is a wide chip (600 mil).** It does *not* sit in the centre channel of a breadboard the way the 28-pin chips do.
   Its two rows of pins are 0.6" apart, so they go in rows **d** and **h**, with the body covering rows e, f and g. The pictures show this.
2. **It needs two power pins and two ground pins** (pins 11 and 32 are VDD, pins 12 and 31 are VSS). All four must be connected.

## Folder contents

```text
month-02-workshop-command-centre/
  README.md                        this page
  build-1-blink.md ... build-4-command-centre.md
  images/                          schematic + breadboard picture for every build (SVG and PNG)
  code/
    build-1-blink/main.c           one complete file per build
    build-2-hello-expander/main.c
    build-3-led-chase/main.c
    build-4-command-centre/main.c
```
