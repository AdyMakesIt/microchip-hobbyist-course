# Bench validation sheet: Month 4 (PIC16F18446 + MCP7940N)

**Tools:** MPLAB X v6.20, XC8, PICkit 3

Date: ____________   Photo of the breadboard taken: [ ]

Work through the builds **in order**. Tick what happened, and write down any message you saw (compiler, programmer, avrdude) exactly as it appeared.

## Month 4 · Build 1 – Blink on a new chip

Page: `month-04-binary-clock/build-1-blink.md`

**Before power (meter checks):**

- [ ] +5 V rail to GND rail: no short.
- [ ] Pin **1** (VDD) beeps to the +5 V rail; pin **20** (VSS) beeps to the GND rail.
- [ ] Pin **4** (MCLR) to the +5 V rail reads about **10 kΩ**.
- [ ] Power on: pin 1 to pin 20 reads **4.8–5.2 V**.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] The LED on RC0 blinks: half a second on, half a second off.
- [ ] Ten blinks take about ten seconds.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Month 4 · Build 2 – Meet the real-time clock

Page: `month-04-binary-clock/build-2-rtc-hello.md`

**Before power (meter checks):**

- [ ] +5 V to GND: no short.
- [ ] MCP7940N pin **8** to +5 V; pin **4** and pin **3** to GND.
- [ ] SCL: pin 6 of the clock to **PIC pin 11**; SDA: pin 5 to **PIC pin 13**. They must **not** beep to each other.
- [ ] Power on: clock pin 8 to pin 4 reads about **5 V**.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] The six LEDs RC0 to RC5 count **in binary**, one step per second. RC0 (the "1" LED) flips every second; RC1 (the "2" LED) every 2 seconds, and so on.
- [ ] After 59 the LEDs go back to all-off, and the count starts again.
- [ ] Unplug and re-plug the power: the count restarts from the build time (no battery yet).

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Month 4 · Build 3 – The binary clock

Page: `month-04-binary-clock/build-3-binary-clock.md`

**Before power (meter checks):**

- [ ] +5 V to GND: no short.
- [ ] Pin 17 to GND does **not** beep until you press the button, then it does.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] With no mode LED lit, the six LEDs count the **seconds** in binary.
- [ ] Press once: **RC6** lights and the LEDs show the **minutes**.
- [ ] Press again: **RC7** lights and the LEDs show the **hours** (0 to 23).
- [ ] Press again: back to seconds.
- [ ] Compare with a real clock: the seconds step once per second, and the minutes change when the seconds wrap. The time is the program's build time plus the time since you powered up.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Assumptions to confirm this month

These were written from datasheets and published examples, not from a real build. Tick each when you have confirmed it, or note what differs.

|  #  | Assumption                                                                                                                                                                 | Confirmed? |
| :-: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------: |
|  1  | The **PICkit 3 supports** the PIC18F47K42, PIC16F18446 and PIC24FJ64GA002 in MPLAB X v6.20                                                                                 |    [ ]     |
|  9  | Month 4: the MCP7940N register bits (`ST`, `OSCRUN`, `VBATEN`), I2C address 0x6F, crystal load capacitors of about 10 pF, and VBAT tied to ground when there is no battery |    [ ]     |
| 11  | `__TIME__` is supported by XC8 and returns "hh:mm:ss"                                                                                                                      |    [ ]     |

## Summary

Overall: [ ] all builds passed   [ ] some failed.   Biggest problem: ______________________________
