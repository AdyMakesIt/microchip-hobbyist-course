# Bench validation sheet: Month 3 (MCP3008 + MCP4822)

**Tools:** MPLAB X v6.20, XC8, PICkit 3, multimeter

Date: ____________   Photo of the breadboard taken: [ ]

Work through the builds **in order**. Tick what happened, and write down any message you saw (compiler, programmer, avrdude) exactly as it appeared.

## Month 3 · Build 1 – Read a knob

Page: `build-1-adc-bar-graph.md`

**Before power (meter checks):**

- [ ] +5 V rail to GND rail: no short.
- [ ] All four PIC power pins (11, 12, 31, 32) as in Month 2.
- [ ] MCP3008: pins **15** and **16** to +5 V; pins **9** and **14** to GND. Pin **7** (CH6) to +5 V, pin **8** (CH7) to GND.
- [ ] Knob: the two outer legs read about the knob's value (for example 10 kΩ) between them, and the middle leg reads between 0 and that value as you turn it.
- [ ] Power on: MCP3008 pin 16 to pin 9 reads about **5 V**; the knob's middle leg sweeps 0 to 5 V as you turn it.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] The bar graph is **empty** with the knob fully one way and **all 8 LEDs lit** fully the other way (or the reverse, depending on which end is which).
- [ ] Turning the knob smoothly makes the bar grow and shrink one LED at a time.
- [ ] The heartbeat LED (RB0) blinks about once a second.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Month 3 · Build 2 – Add the DAC

Page: `build-2-dac.md`

**Before power (meter checks):**

- [ ] +5 V to GND: no short.
- [ ] MCP4822 pin **1** to +5 V; pins **5** and **7** to GND.
- [ ] SCK, SDI and CS go to the right places: SCK ↔ MCP3008 pin 13, SDI ↔ MCP3008 pin 11 (these are the same nets), CS ↔ PIC pin 23.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] The bar graph still follows the knob.
- [ ] With the multimeter (DC volts), the voltage at **MCP4822 pin 8 (VOUTA)** matches the voltage at the knob's **middle leg**, within about 30 mV, for knob positions up to about 4 V.
- [ ] Above about 4.1 V on the knob, VOUTA stops at 4.09 V and the bar graph keeps rising.
- [ ] The LED **D10** slowly brightens and dims, about every 2 seconds (it only lights in the upper part of the wave, above about 1.9 V).
- [ ] The heartbeat LED blinks.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Month 3 · Build 3 – Loop the DAC back into the ADC

Page: `build-3-loopback.md`

**Before power (meter checks):**

- [ ] +5 V to GND: no short.
- [ ] MCP4822 pin 8 and MCP3008 pin 2 beep to each other, and to nothing else.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] The bar graph sweeps from empty up to 7 LEDs and back, about every 4 seconds.
- [ ] It rises and falls **smoothly**, one LED at a time.
- [ ] The heartbeat LED blinks once a second (no fault code).
- [ ] Pull out the loop-back wire and reset the chip: the heartbeat LED shows **3 blinks**. Put the wire back: it works again.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Assumptions to confirm this month

These were written from datasheets and published examples, not from a real build. Tick each when you have confirmed it, or note what differs.

|  #  | Assumption                                                                                                                                                                                                                                               | Confirmed? |
| :-: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------: |
|  2  | Pin numbers for the PIC18F47K42 (40-pin PDIP), MCP23017, MCP3008, 24LC512, ATmega328P and PIC24FJ64GA002 (28-pin SPDIP) were taken from recalled datasheet tables; the PIC16F18857 pins are bench-proven for RC0 and the power pins                      |    [ ]     |
|  8  | Month 3: MCP3008 pin table and the 3-byte read; the MCP4822 gain-2x setting gives 1 mV per step; the loop-back test limits (readings rise by at least 60 counts per step; 3.5 V reads 600 to 850 counts) are loose enough for a real 4.5 to 5.5 V supply |    [ ]     |

## Summary

Overall: [ ] all builds passed   [ ] some failed.   Biggest problem: ______________________________
