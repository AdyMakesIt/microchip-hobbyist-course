# Month 3 – Analogue In, Analogue Out (PIC18F47K42, MCP3008, MCP4822)

**Time:** three or four evenings  **Chips:** MCP3008 (ADC) and MCP4822 (DAC), both free samples, plus the PIC18F47K42 from Month 2  **Supply:** 5 V
**Everything for this month is in this folder:** pages, pictures and code.

The real world is **analogue**: voltages that can be any value. A microcontroller is **digital**: numbers. This month you cross the border in both directions:

* an **ADC** (analogue-to-digital converter) turns a voltage into a number. You will read a knob (a potentiometer) and show its position as a bar of LEDs.
* a **DAC** (digital-to-analogue converter) turns a number into a voltage. You will make the chip output exact voltages you can measure with a multimeter.

Both chips talk over **SPI**, a four-wire bus faster and simpler than I2C. As in Month 2, you will write the SPI routine yourself (about 25 lines) so you can see every bit.

## The three builds

Do them in order. Each ends with a **pass check**.

| #   | Build                                                 | You add                                       | You prove                              |
| :-: | ----------------------------------------------------- | --------------------------------------------- | -------------------------------------- |
|  1  | [Read a knob](build-1-adc-bar-graph.md)               | the PIC, the MCP3008, a potentiometer, 8 LEDs | SPI works and the ADC measures voltage |
|  2  | [Add the DAC](build-2-dac.md)                         | the MCP4822 and an LED                        | the chip can output exact voltages     |
|  3  | [Loop the DAC back into the ADC](build-3-loopback.md) | one wire                                      | both converters check each other       |

**Status:** the logic of all three programs, including the SPI protocol and its timing, has been tested against simulated MCP3008 and MCP4822 chips
(see [`../maintainer/VERIFICATION_LOG.md`](../maintainer/VERIFICATION_LOG.md)). The wiring pictures are machine-checked against the schematics.
Nothing here has been run on a real bench yet. If something does not work, that is useful information, so please report it.

## What you need

### Free samples (order these in month 3)

| Part                          | Order | Used for                  |
| ----------------------------- | ----: | ------------------------- |
| **MCP3008-I/P** (16-pin PDIP) |     3 | the 8-channel, 10-bit ADC |
| **MCP4822-E/P** (8-pin PDIP)  |     3 | the 2-channel, 12-bit DAC |

You also need the **PIC18F47K42-I/P** from Month 2 and the same PICkit 3 programming leads.

### Parts used (counted automatically from the circuit)

<!-- bom -->
| Part                                                     | Value            | Qty used | Buy at least |
| -------------------------------------------------------- | ---------------- | -------: | -----------: |
| Resistor                                                 | 1 kΩ             |        1 |            2 |
| Resistor                                                 | 10 kΩ            |        1 |            2 |
| Resistor                                                 | 680 Ω            |        9 |           11 |
| Ceramic capacitor                                        | 100nF            |        4 |            5 |
| Potentiometer (rotary or trimmer)                        | 10 kΩ            |        1 |            2 |
| LED, 5 mm                                                | red              |       10 |           12 |
| Jumper wires, solid or male-to-male                      | assorted lengths |       40 |           46 |
| Female-to-male Dupont leads (PICkit 3 ICSP → breadboard) |                  |        5 |            6 |
<!-- /bom -->

The potentiometer should be a **10 kΩ linear** one ("B10K"): a rotary pot with three legs in a row, or a small trimmer. Any value from 5 kΩ to 100 kΩ works.

### Tools

Everything from Month 2. Nothing else.

## Before you start

1. **Take a photo of your Month 2 board**, then clear it. Month 3 uses the same PIC18F47K42 and the same programming leads, but a new layout.
2. The numbers: the ADC reads **0 to 1023** for **0 V to 5 V**, so each step is about **4.9 mV**. The DAC is set to its "2x gain" mode, so each step is exactly **1 mV**.

## Ready-made projects and hardware files

* **Working projects:** [`projects/`](projects/README.md) holds complete, ready-to-open projects for the builds (MPLAB X).
* **Hardware files:** [`hardware/`](hardware/README.md) holds the KiCad schematic location, a **parts list** and a **connection list** you can use to design a PCB. See [Taking a project further](../start-here/07-taking-a-project-further.md).

## Folder contents

```text
month-03-analogue-in-out/
  README.md                          this page
  build-1-adc-bar-graph.md ... build-3-loopback.md
  images/                            schematic + breadboard picture for every build
  projects/              ready-to-open projects (see projects/README.md)
  hardware/              KiCad schematic, parts list and connection list
  code/
    build-1-adc-bar-graph/main.c     one complete file per build
    build-2-dac/main.c
    build-3-loopback/main.c
```
