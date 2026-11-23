# Bench validation sheet: Month 5 (PIC24FJ64GA002 + 24LC512, 3.3 V)

**Tools:** MPLAB X v6.20, XC16, PICkit 3, multimeter

Date: ____________   Photo of the breadboard taken: [ ]

Work through the builds **in order**. Tick what happened, and write down any message you saw (compiler, programmer, avrdude) exactly as it appeared.

## Month 5 · Build 1 – Blink at 3.3 V

Page: `month-05-build-1-blink.md`

**Before power (meter checks):**

- [ ] 3.3 V rail to GND rail: no short.
- [ ] Pins **13** and **28** beep to the 3.3 V rail; pins **8, 19** and **27** beep to the GND rail.
- [ ] The **VCAP** capacitor really is between pin 20 and ground, and not between pin 20 and the 3.3 V rail.
- [ ] Pin **1** (MCLR) to the 3.3 V rail reads about **10 kΩ**.
- [ ] Power on: pin 13 to pin 8 reads **3.2–3.4 V**.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] The LED on RA0 blinks: half a second on, half a second off.
- [ ] Ten blinks take about ten seconds.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Month 5 · Build 2 – Say hello to the EEPROM

Page: `month-05-build-2-eeprom-hello.md`

**Before power (meter checks):**

- [ ] 3.3 V rail to GND rail: no short.
- [ ] 24LC512 pin **8** to 3.3 V; pins **1, 2, 3, 4, 7** all to ground.
- [ ] SCL: pin 6 of the EEPROM to **PIC pin 17**; SDA: pin 5 to **PIC pin 18**. They must **not** beep to each other.
- [ ] Power on: EEPROM pin 8 to pin 4 reads about **3.3 V**.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] The eight LEDs show **1010 0101** (0xA5): LED 0 lit, LED 1 off, LED 2 lit, LED 3 off, LED 4 off, LED 5 lit, LED 6 off, LED 7 lit.
- [ ] The heartbeat LED (RA0) blinks about once a second.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Month 5 · Build 3 – Memory that survives power-off

Page: `month-05-build-3-boot-counter.md`

**Before power (meter checks):**

- [ ] 3.3 V to GND: no short.
- [ ] Pin 3 to ground does **not** beep until you press the button, then it does.
- [ ] Pin 3 to the 3.3 V rail reads about **10 kΩ**.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] First start: the LEDs show **1**: LED 0 lit. (On a brand-new chip.)
- [ ] Press the button: the number goes up by one each press. A long press counts once.
- [ ] **Switch the power off, then on again:** the number is still there, plus one.
- [ ] After 256 counts the LEDs wrap to all-off, but the real counter keeps going in the EEPROM's second byte.
- [ ] The heartbeat LED blinks.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Assumptions to confirm this month

These were written from datasheets and published examples, not from a real build. Tick each when you have confirmed it, or note what differs.

|  #  | Assumption                                                                                                                                                                                                                                      | Confirmed? |
| :-: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------: |
|  1  | The **PICkit 3 supports** the PIC18F47K42, PIC16F18446 and PIC24FJ64GA002 in MPLAB X v6.20                                                                                                                                                      |    [ ]     |
|  2  | Pin numbers for the PIC18F47K42 (40-pin PDIP), MCP23017, MCP3008, 24LC512, ATmega328P and PIC24FJ64GA002 (28-pin SPDIP) were taken from recalled datasheet tables; the PIC16F18857 pins are bench-proven for RC0 and the power pins             |    [ ]     |
| 10  | Month 5: the PIC24's VCAP capacitor value and type, the 3.3 V supply range (do not exceed about 3.6 V), the I2C pins RB8/RB9 being usable as plain I/O, and the 24LC512 (address 0x50, 128-byte page, 5 ms write cycle, about a million writes) |    [ ]     |

## Summary

Overall: [ ] all builds passed   [ ] some failed.   Biggest problem: ______________________________
