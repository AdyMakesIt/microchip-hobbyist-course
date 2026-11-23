# Microchip Hobbyist Course

Learn to build with Microchip's **PIC** and **AVR** microcontrollers on a breadboard, one small project a month,
using **free chip samples** with a **low-cost PICkit 3 programmer** and a **USB/ASP programmer**. No soldering. No degree needed.

> **Status: Months 1 to 5 are complete.** Their programs are tested in simulation and their wiring is machine-checked,
> but they still need their first **bench test** on real hardware (see [the verification log](maintainer/VERIFICATION_LOG.md)).
> Months 6 to 24 are in preparation.

## Start here

1. [How the course works](start-here/01-how-the-course-works.md) (5 min)
2. [Course overview](start-here/course-overview.md): what you will build in each of the 24 months
3. [Ordering and budget](start-here/02-ordering-and-budget.md): how ordering works
4. [Purchasing plan](start-here/purchasing-plan.md): what to order each month, and what to buy ahead
5. [Parts catalogue](start-here/parts-catalogue.md): specifications and links for every part
6. [AVR software and programmer setup](start-here/03-avr-setup.md) (ATmega328P, VS Code + PlatformIO)
7. [PIC software and programmer setup](start-here/04-pic-setup.md) (MPLAB X v6.20, XC8, PICkit 3)
8. [Electronics and breadboard basics](start-here/05-electronics-and-breadboard-basics.md)
9. [Troubleshooting](start-here/06-troubleshooting.md)
10. [Taking a project further](start-here/07-taking-a-project-further.md): KiCad and PCBs

## The months
<!-- months -->
| N   | Title                                                                 | Theme                                            | Host                         | Samples                 | Learn                                                                                                                  | Projects                                                                                             | Status  |
| --- | --------------------------------------------------------------------- | ------------------------------------------------ | ---------------------------- | ----------------------- | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------- |
| 1   | [Electronic dice](month-01-electronic-dice/README.md)                 | the real tools: AVR, then PIC                    | ATMEGA328P, THEN PIC16F18857 | ATMEGA328P, PIC16F18857 | Plain C without the Arduino IDE; outputs and inputs; a PICkit 3 and a USBasp or Uno as programmers                     | Add a six-celebration, A high-roll mode                                                              | built   |
| 2   | [Workshop Command Centre](month-02-workshop-command-centre/README.md) | I2C and port expanders                           | PIC18F47K42                  | PIC18F47K42, MCP23017   | I2C by hand; fault codes; edge detection                                                                               | A fourth animation, Two-button combos                                                                | built   |
| 3   | [Analogue in, analogue out](month-03-analogue-in-out/README.md)       | SPI, ADC and DAC                                 | PIC18F47K42                  | MCP3008, MCP4822        | SPI by hand; converting voltages to numbers and back; self-tests                                                       | Voltage divider range test                                                                           | built   |
| 4   | [The binary clock](month-04-binary-clock/README.md)                   | porting a program; a real-time clock             | PIC16F18446                  | PIC16F18446, MCP7940N   | Moving a program between chips of one family; BCD; a 32.768 kHz crystal                                                | Keep time with a coin cell                                                                           | built   |
| 5   | [A 16-bit chip at 3.3 V](month-05-sixteen-bit-and-memory/README.md)   | PIC24, XC16 and EEPROM                           | PIC24FJ64GA002               | PIC24FJ64GA002, 24LC512 | 3.3 V supplies; a 16-bit core; EEPROM pages and ACK polling                                                            | Press-and-hold to reset the counter                                                                  | built   |
| 6   | SPI memory                                                            | hardware SPI with pin mapping                    | PIC24FJ64GA002               | 25LC1024, 23LC1024      | The PIC24's built-in SPI and peripheral pin select; EEPROM versus SRAM speed                                           | Memory tester, Tape recorder: record button presses and replay them, Stream ADC readings into memory | planned |
| 7   | Hardware SPI and I2C on AVR                                           | expanders on a classic AVR                       | ATMEGA328P                   | MCP23S17, MCP23008      | The ATmega328P's SPI and TWI hardware; comparing SPI and I2C                                                           | 16-LED bar graph, Keypad scanner, A memory-game                                                      | planned |
| 8   | USB two ways                                                          | a USB bridge and native USB                      | PC + PIC16F1454, PIC18F47K42 | MCP2221A, PIC16F1454    | A USB-to-serial bridge; a PIC with USB built in; the first use of Microchip's code generator (MCC) for a large library | Serial dashboard of ADC readings, Set the clock chip from a PC, A USB HID button box                 | planned |
| 9   | Sensing the world                                                     | analogue and digital temperature sensors         | ATMEGA328P                   | MCP9700A, TC74          | ADC accuracy; analogue versus digital sensors; logging to the EEPROM                                                   | Min/max thermometer, Frost alarm, A calibration table                                                | planned |
| 10  | Op-amps and comparators                                               | conditioning analogue signals                    | PIC16F18857                  | MCP6004, MCP6542        | Buffers, gain, hysteresis and filters                                                                                  | Night-light, A clap switch, A PWM digital-to-analogue converter                                      | planned |
| 11  | Programmable analogue                                                 | digital pots and programmable gain               | PIC18F47K42                  | MCP4151, MCP6S21        | Letting software set analogue values over SPI                                                                          | Digital volume control, Programmable LED dimmer, Auto-gain light meter                               | planned |
| 12  | Power and reset                                                       | building your own supply                         | PIC18F47K42                  | MCP1702, MCP100         | Regulators, dropout, supervisors and brown-out                                                                         | Brown-out demonstration, Power-on sequencer                                                          | planned |
| 13  | dsPIC33: a signal controller                                          | a new family and precision measurement           | DSPIC33EV                    | DSPIC33EV, MCP3551      | A fast 16-bit core, timers and PWM; measuring tiny voltages precisely                                                  | LED fade with hardware PWM, Tone generator, Frequency counter, A strain-gauge-style bridge reader    | planned |
| 14  | Waveforms with a real reference                                       | DAC output with an external reference            | DSPIC33EV                    | MCP4922, MCP1525        | Waveform tables; PWM through a filter; the effect of a precise reference                                               | Function generator, Tone sequencer, Siren                                                            | planned |
| 15  | PIC32: a 32-bit chip                                                  | a new family, a second clock chip                | PIC32MX (3.3 V)              | PIC32MX170, MCP79410    | XC32; a fast 32-bit core; a clock chip with EEPROM and a unique ID                                                     | Speed comparison across families, Terminal clock                                                     | planned |
| 16  | Other serial buses                                                    | one-wire and Microwire EEPROMs; portable drivers | ANY OF YOUR CHIPS            | 11LC010, 93LC66B        | Bit-banging unusual protocols; separating a hardware layer from a device layer                                         | A portable library for your chips, A benchmark table                                                 | planned |
| 17  | Tiny chips: AVR and PIC                                               | eight-pin microcontrollers                       | ATTINY85, PIC12F1840         | ATTINY85, PIC12F1840    | How little a program can use; comparing a tiny AVR with a tiny PIC                                                     | A tiny dice, A knob-controlled LED, A one-chip light sensor                                          | planned |
| 18  | Bigger and newer AVRs                                                 | a large classic AVR and a modern one             | ATMEGA1284P, AVR128DB28      | ATMEGA1284P, AVR128DB28 | A 128 KB AVR with more peripherals; the modern AVR's event system (optional month, needs a UPDI programmer)            | An LED driven by hardware only, A frequency meter                                                    | planned |
| 19  | Data logger                                                           | putting several chips together                   | ANY OF YOUR CHIPS            | MCP3202, 24AA02E48      | A multi-chip project: clock, memory, sensors, a precise ADC and a node ID                                              | Greenhouse logger, Fridge monitor, Plant-watering log                                                | planned |
| 20  | CAN bus: two nodes                                                    | a real network                                   | PIC18F47K42 + ATMEGA328P     | MCP2515, MCP2562        | CAN messages between two different chip families                                                                       | Remote sensor, Two-player reaction game, A bus-error demonstration                                   | planned |
| 21  | Motors and power switching                                            | driving real loads                               | DSPIC33EV OR PIC16F18857     | MCP1407, MCP6022        | MOSFET switching, PWM speed control, flyback protection and current sensing                                            | Fan controller, Servo gauge for the data logger, Motor stall detector                                | planned |
| 22  | Sound and signals                                                     | audio with a negative supply and stereo gain     | DSPIC33EV                    | TC7660, MCP6S22         | A negative rail for an audio op-amp; stereo programmable gain; a simple synthesizer                                    | Theremin-style instrument, Drum machine, Sound-level meter                                           | planned |
| 23  | Low power                                                             | running for months on a battery                  | PIC OR AVR                   | MCP1700, TC54           | Sleep modes, wake-up sources, an ultra-low-power regulator and a battery-low detector                                  | Coin-cell blinker, A sleeping logger, A battery-voltage gauge                                        | planned |
| 24  | Capstone                                                              | design and build your own                        | YOUR CHOICE                  | —                       | Combine at least three chips from earlier months; order two chips of your choice from the shortlist                    | Weather station, CAN-linked sensor network, Synthesizer, Motor-driven gauge                          | planned |
<!-- /months -->

## How is the course structured

* **One folder per month** with the pages, pictures and code together.
* **One short page per build**, each ending in a pass check.
* **Plain-C programs** you can read from top to bottom. No generated code in the early months.
* **Every circuit is drawn from one description** and the breadboard layout is **machine-checked** against the schematic.
* **Hole-by-hole assembly tables** instead of "wire it like the picture".
* **Fault codes** on the heartbeat LED, so a failure tells you *what* failed.
* **Honest status labels** on every page.

## Repository layout

```text
README.md                          this page
start-here/                        introduction, overview, ordering and purchasing, setup, basics, troubleshooting
month-01-electronic-dice/          pages + images + code, all together
month-02-workshop-command-centre/  pages + images + code, all together
month-03-analogue-in-out/          (and months 4 and 5, the same layout)
maintainer/                        tests, diagram tools, GitHub guide, verification log
```

## For maintainers and contributors

See [maintainer/README.md](maintainer/README.md).

## Licence

Not yet chosen. See the note in [maintainer/GITHUB_GUIDE.md](maintainer/GITHUB_GUIDE.md#licence).
