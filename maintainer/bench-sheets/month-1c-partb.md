# Bench validation sheet: Month 1, Part B (optional AVR programmer)

**Tools:** Arduino IDE, USBasp or Uno, USB-serial adapter

Date: ____________   Photo of the breadboard taken: [ ]

Work through the builds **in order**. Tick what happened, and write down any message you saw (compiler, programmer, avrdude) exactly as it appeared.

## Month 1 · Part B · Build B1 – The minimum ATmega328P board

Page: `month-01-electronic-dice/avr-programmer/build-b1-minimum-board.md`

**Before power (meter checks):**

- [ ] +5 V rail to GND rail: no beep (no short).
- [ ] Pins **7** and **20** each beep to the +5 V rail; pins **8** and **22** each beep to the GND rail.
- [ ] Pin **1** (RESET) to the +5 V rail reads about **10 kΩ**.
- [ ] Power on: pin 7 to pin 8 reads **4.8–5.2 V**.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] "Burn Bootloader" ended with **Done burning bootloader.**
- [ ] The upload ended with **Done uploading.**
- [ ] The D9 LED blinks: half a second on, half a second off.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Month 1 · Part B · Build B2 – Turn it into a programmer

Page: `month-01-electronic-dice/avr-programmer/build-b2-programmer.md`

**Before power (meter checks):**

- [ ] +5 V to GND: no short.
- [ ] Long leg of D2 and D3 towards the resistors.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] The upload finished with **Done uploading.**
- [ ] **D1** (heartbeat) pulses slowly: it fades up and down, not an on/off blink.
- [ ] **D2** (error) and **D3** (programming) are **off**.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Month 1 · Part B · Build B3 – Program a second chip

Page: `month-01-electronic-dice/avr-programmer/build-b3-program-a-chip.md`

**Before power (meter checks):**

- [ ] +5 V to GND: no short.
- [ ] Target pins **7** and **20** beep to +5 V; pins **8** and **22** beep to GND.
- [ ] The four ISP wires go pin-to-pin (programmer pin 17 to target pin 17 and so on). They are **not** crossed over.
- [ ] Target pin 1 to +5 V reads about **10 kΩ**.

**Programming:**

- [ ] Built with no errors
- [ ] Programmed
- [ ] Program runs

**Pass checks:**

- [ ] "Burn Bootloader" ended with **Done burning bootloader.**
- [ ] **D3** flickered during programming, and **D2** (error) never lit.
- [ ] The **target's LED (D4)** blinks: half a second on, half a second off.
- [ ] The target keeps blinking after you **unplug the four ISP wires**: it is now a chip programmed by a programmer you built.

| Result                               | Notes / exact messages |
| ------------------------------------ | ---------------------- |
| [ ] passed   [ ] partly   [ ] failed |                        |

## Assumptions to confirm this month

These were written from datasheets and published examples, not from a real build. Tick each when you have confirmed it, or note what differs.

|  #  | Assumption                                                                                              | Confirmed? |
| :-: | ------------------------------------------------------------------------------------------------------- | :--------: |
|  7  | Part B: Arduino IDE menu names and messages match the IDE version you install; the ATmega328P pin table |    [ ]     |

## Summary

Overall: [ ] all builds passed   [ ] some failed.   Biggest problem: ______________________________
