# Bench validation sheet: Month 1, PIC track (PIC16F18857)

**Tools:** MPLAB X v6.20, XC8, PICkit 3, multimeter

Date: ____________   Photo of the breadboard taken: [ ]

Work through the builds **in order**. Tick what happened, and write down any message you saw (compiler, programmer, avrdude) exactly as it appeared.

## Month 1 · PIC Build 1 – Blink an LED

Page: `build-pic-1-blink.md`

**Before power (meter checks):**

- [ ] **No short:** set the meter to continuity (beep) or ohms. Between the **+5 V** rail and the **GND** rail it must **not** beep and should read thousands of ohms or more (it may creep upwards as C1 charges).
- [ ] **Chip pins:** pin **20** to the +5 V rail beeps; pins **8** and **19** to the GND rail beep.
- [ ] **Reset pull-up:** pin **1** to the +5 V rail reads about **10 kΩ**.
- [ ] **Check 4:** meter on DC volts, red probe on pin **20**, black on pin **19**: you should read **4.8 V to 5.2 V**.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] The LED is on for half a second, off for half a second, repeating.
- [ ] Ten blinks take about ten seconds on a stopwatch (speed is right).
- [ ] Unplugging and re-plugging the power starts the blinking again by itself (the program is stored in the chip).

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Month 1 · PIC Build 2 – Add the button

Page: `build-pic-2-button.md`

**Before power (meter checks):**

- [ ] With power off and the button **not** pressed: pin 2 to GND must **not** beep.
- [ ] Press and hold the button: pin 2 to GND **beeps**.
- [ ] +5 V rail to GND rail: still no short.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] LED off when you are not touching the button.
- [ ] LED on while the button is held, off again when released.
- [ ] A very quick tap still lights it briefly.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Month 1 · PIC Build 3 – The dice

Page: `build-pic-3-dice.md`

**Before power (meter checks):**

- [ ] No short between the +5 V and GND rails.
- [ ] Look along the LED row: every long leg is on the **resistor** side (the picture marks it with a red **+**).
- [ ] Power on: nothing should light yet (the previous build's program may still be running; that is fine).

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] On power-up the centre LED flashes three times, then shows a **1**.
- [ ] Pressing the button runs the animation and settles on a face, about 2 seconds later.
- [ ] Holding the button does not roll again until you release and press again.
- [ ] After 20 rolls you have seen every number at least once.
- [ ] Each face looks right: 2 is opposite corners, 4 is four corners, 6 is two columns of three.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Assumptions to confirm this month

These were written from datasheets and published examples, not from a real build. Tick each when you have confirmed it, or note what differs.

|  #  | Assumption                                                                                                                                                                                                                          | Confirmed? |
| :-: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------: |
|  1  | The **PICkit 3 supports** the PIC18F47K42, PIC16F18446 and PIC24FJ64GA002 in MPLAB X v6.20                                                                                                                                          |    [ ]     |
|  2  | Pin numbers for the PIC18F47K42 (40-pin PDIP), MCP23017, MCP3008, 24LC512, ATmega328P and PIC24FJ64GA002 (28-pin SPDIP) were taken from recalled datasheet tables; the PIC16F18857 pins are bench-proven for RC0 and the power pins |    [ ]     |
|  5  | Whole-register names (`ANSELx`, `TRISx`, `LATx`, `PORTx`, `WPUA`, `OSCFRQ`, `CLKDIV`, `AD1PCFG`) exist for each device                                                                                                              |    [ ]     |

## Summary

Overall: [ ] all builds passed   [ ] some failed.   Biggest problem: ______________________________
