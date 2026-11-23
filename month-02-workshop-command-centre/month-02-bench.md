# Bench validation sheet: Month 2 (PIC18F47K42 + MCP23017)

**Tools:** MPLAB X v6.20, XC8, PICkit 3

Date: ____________   Photo of the breadboard taken: [ ]

Work through the builds **in order**. Tick what happened, and write down any message you saw (compiler, programmer, avrdude) exactly as it appeared.

## Month 2 · Build 1 – Blink (minimum circuit)

Page: `month-02-build-1-blink.md`

**Before power (meter checks):**

- [ ] +5 V rail to GND rail: no beep (no short).
- [ ] Pins **11** and **32** each beep to the +5 V rail; pins **12** and **31** each beep to the GND rail.
- [ ] Pin **1** to the +5 V rail reads about **10 kΩ**.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] The LED blinks: half a second on, half a second off.
- [ ] Ten blinks take about ten seconds.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Month 2 · Build 2 – Say hello to the MCP23017

Page: `month-02-build-2-hello-expander.md`

**Before power (meter checks):**

- [ ] +5 V to GND: no short.
- [ ] MCP23017 pin **9** (VDD) beeps to +5 V; pin **10** (VSS) beeps to GND; pins **15, 16, 17** beep to GND.
- [ ] Pin **18** (RESET) to +5 V reads about **10 kΩ**.
- [ ] SCL line: MCP pin **12** to PIC pin **18** beeps. SDA line: MCP pin **13** to PIC pin **23** beeps. They must **not** beep to each other.
- [ ] Power on: MCP pin 9 to pin 10 reads about **5 V**.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] The **GPA0 LED (D2) stays lit**.
- [ ] The **heartbeat LED (D1) blinks once a second** (half a second on, half off).

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Month 2 · Build 3 – Eight LEDs and a button

Page: `month-02-build-3-led-chase.md`

**Before power (meter checks):**

- [ ] +5 V to GND: no short.
- [ ] Along the LED row, every LED's long leg is on the resistor side (the picture marks the long leg with a red **+**).
- [ ] SW1: pin 1 of the MCP23017 to GND does **not** beep until you press the button, then it does.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] At power-up all eight LEDs light for half a second, then only the first one stays on.
- [ ] Each press of SW1 moves the light one LED to the right (towards GPA7), and after the last LED it goes back to the first.
- [ ] Holding the button down moves it **once**, not repeatedly.
- [ ] The heartbeat LED keeps blinking about once a second.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Month 2 · Build 4 – Workshop Command Centre

Page: `month-02-build-4-command-centre.md`

**Before power (meter checks):**

- [ ] +5 V to GND: no short.
- [ ] Pin 2 of the MCP23017 to GND beeps only while SW2 is pressed.
- [ ] The piezo disc is wired through R14, **not** straight to the pin.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] Start-up: all LEDs flash, one beep, then a single light runs along the row (slowly).
- [ ] **MODE** (SW1): next animation: *filling bar*, then *alternating LEDs*, then back to the running light. Each press beeps.
- [ ] **SPEED** (SW2): slow, medium, fast, then back to slow. Each press beeps.
- [ ] The heartbeat LED keeps blinking.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Assumptions to confirm this month

These were written from datasheets and published examples, not from a real build. Tick each when you have confirmed it, or note what differs.

|  #  | Assumption                                                                                                                                                                                                                          | Confirmed? |
| :-: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------: |
|  1  | The **PICkit 3 supports** the PIC18F47K42, PIC16F18446 and PIC24FJ64GA002 in MPLAB X v6.20                                                                                                                                          |    [ ]     |
|  2  | Pin numbers for the PIC18F47K42 (40-pin PDIP), MCP23017, MCP3008, 24LC512, ATmega328P and PIC24FJ64GA002 (28-pin SPDIP) were taken from recalled datasheet tables; the PIC16F18857 pins are bench-proven for RC0 and the power pins |    [ ]     |
|  3  | A 600-mil 40-pin DIP straddles an 830-point breadboard with pins in rows d and h                                                                                                                                                    |    [ ]     |
|  5  | Whole-register names (`ANSELx`, `TRISx`, `LATx`, `PORTx`, `WPUA`, `OSCFRQ`, `CLKDIV`, `AD1PCFG`) exist for each device                                                                                                              |    [ ]     |

## Summary

Overall: [ ] all builds passed   [ ] some failed.   Biggest problem: ______________________________
