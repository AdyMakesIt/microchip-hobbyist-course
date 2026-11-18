# Course overview: the 24 months

A high-level plan of what you will build each month, which chips you will use and what else you need.
**Months 1 to 5 are complete.** Months 6 to 24 are a **plan and may change** as the course develops.

Every month uses **two new free-sample chips** (three of each), plus parts from your **lab stock**. The [purchasing plan](purchasing-plan.md) shows what to order and when, and the [parts catalogue](parts-catalogue.md) has the specifications and links.

## The path

| Phase                      | Months | What it covers                                                               |
| -------------------------- | :----: | ---------------------------------------------------------------------------- |
| Foundations                |  1–5   | the real tools, the three buses (I2C, SPI) and the first memory chip         |
| Buses, memory and analogue |  6–12  | hardware peripherals and the analogue world                                  |
| New families               | 13–18  | dsPIC33, PIC32, tiny chips and modern AVR, with peripherals you already know |
| Projects                   | 19–24  | multi-chip projects, a network, power and sound, and a capstone              |

## Month by month

| Month | Project                                                                  | New chips (free samples)            | Main chip                    | What you learn                                                                                                         | Extra parts to buy                                   |
| :---: | ------------------------------------------------------------------------ | ----------------------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
|   1   | [Electronic dice](../month-01-electronic-dice/README.md)                 | ATmega328P-PU, PIC16F18857-I/SP     | ATmega328P, then PIC16F18857 | Plain C without the Arduino IDE; outputs and inputs; a PICkit 3 and a USBasp or Uno as programmers                     | Crystal                                              |
|   2   | [Workshop Command Centre](../month-02-workshop-command-centre/README.md) | PIC18F47K42-I/P, MCP23017-E/SP      | PIC18F47K42                  | I2C by hand; fault codes; edge detection                                                                               | –                                                    |
|   3   | [Analogue in, analogue out](../month-03-analogue-in-out/README.md)       | MCP3008-I/P, MCP4822-E/P            | PIC18F47K42                  | SPI by hand; converting voltages to numbers and back; self-tests                                                       | –                                                    |
|   4   | [The binary clock](../month-04-binary-clock/README.md)                   | PIC16F18446-I/P, MCP7940N-I/P       | PIC16F18446                  | Moving a program between chips of one family; BCD; a 32.768 kHz crystal                                                | Crystal                                              |
|   5   | [A 16-bit chip at 3.3 V](../month-05-sixteen-bit-and-memory/README.md)   | PIC24FJ64GA002-I/SP, 24LC512-I/P    | PIC24FJ64GA002               | 3.3 V supplies; a 16-bit core; EEPROM pages and ACK polling                                                            | –                                                    |
|   6   | SPI memory                                                               | 25LC1024-I/P, 23LC1024-I/P          | PIC24FJ64GA002               | The PIC24's built-in SPI and peripheral pin select; EEPROM versus SRAM speed                                           | –                                                    |
|   7   | Hardware SPI and I2C on AVR                                              | MCP23S17-E/SP, MCP23008-E/P         | ATmega328P                   | The ATmega328P's SPI and TWI hardware; comparing SPI and I2C                                                           | Keypad                                               |
|   8   | USB two ways                                                             | MCP2221A-I/P, PIC16F1454-I/P        | PC + PIC16F1454, PIC18F47K42 | A USB-to-serial bridge; a PIC with USB built in; the first use of Microchip's code generator (MCC) for a large library | USB socket breakout board                            |
|   9   | Sensing the world                                                        | MCP9700A-E/TO, TC74A0-5.0VAT        | ATmega328P                   | ADC accuracy; analogue versus digital sensors; logging to the EEPROM                                                   | –                                                    |
|  10   | Op-amps and comparators                                                  | MCP6004-I/P, MCP6542-I/P            | PIC16F18857                  | Buffers, gain, hysteresis and filters                                                                                  | LDR (light-dependent resistor)                       |
|  11   | Programmable analogue                                                    | MCP4151-103E/P, MCP6S21-I/P         | PIC18F47K42                  | Letting software set analogue values over SPI                                                                          | Speaker                                              |
|  12   | Power and reset                                                          | MCP1702-3302E/TO, MCP100-xxx/TO     | PIC18F47K42                  | Regulators, dropout, supervisors and brown-out                                                                         | –                                                    |
|  13   | dsPIC33: a signal controller                                             | dsPIC33EV128GM002-I/SP, MCP3551-E/P | dsPIC33EV                    | A fast 16-bit core, timers and PWM; measuring tiny voltages precisely                                                  | –                                                    |
|  14   | Waveforms with a real reference                                          | MCP4922-E/P, MCP1525-I/TO           | dsPIC33EV                    | Waveform tables; PWM through a filter; the effect of a precise reference                                               | –                                                    |
|  15   | PIC32: a 32-bit chip                                                     | PIC32MX170F256B-I/SP, MCP79410-I/P  | PIC32MX (3.3 V)              | XC32; a fast 32-bit core; a clock chip with EEPROM and a unique ID                                                     | –                                                    |
|  16   | Other serial buses                                                       | 11LC010-I/TO, 93LC66B-I/P           | any of your chips            | Bit-banging unusual protocols; separating a hardware layer from a device layer                                         | –                                                    |
|  17   | Tiny chips: AVR and PIC                                                  | ATtiny85-20PU, PIC12F1840-I/P       | ATtiny85, PIC12F1840         | How little a program can use; comparing a tiny AVR with a tiny PIC                                                     | –                                                    |
|  18   | Bigger and newer AVRs                                                    | ATmega1284P-PU, AVR128DB28-I/SP     | ATmega1284P, AVR128DB28      | A 128 KB AVR with more peripherals; the modern AVR's event system (optional month, needs a UPDI programmer)            | –                                                    |
|  19   | Data logger                                                              | MCP3202-CI/P, 24AA02E48-I/P         | any of your chips            | A multi-chip project: clock, memory, sensors, a precise ADC and a node ID                                              | CR2032 cell and holder                               |
|  20   | CAN bus: two nodes                                                       | MCP2515-I/P, MCP2562-E/P            | PIC18F47K42 + ATmega328P     | CAN messages between two different chip families                                                                       | Crystal                                              |
|  21   | Motors and power switching                                               | MCP1407-E/P, MCP6022-I/P            | dsPIC33EV or PIC16F18857     | MOSFET switching, PWM speed control, flyback protection and current sensing                                            | Resistor 0.1 Ω, MOSFET, Diode, DC motor, Hobby servo |
|  22   | Sound and signals                                                        | TC7660EPA, MCP6S22-I/P              | dsPIC33EV                    | A negative rail for an audio op-amp; stereo programmable gain; a simple synthesizer                                    | –                                                    |
|  23   | Low power                                                                | MCP1700-3302E/TO, TC54VN3002EZB     | PIC or AVR                   | Sleep modes, wake-up sources, an ultra-low-power regulator and a battery-low detector                                  | –                                                    |
|  24   | Capstone                                                                 | two of your choice                  | your choice                  | Combine at least three chips from earlier months; order two chips of your choice from the shortlist                    | –                                                    |

## Details of each month

### Month 1: Electronic dice (complete)

**Subject:** the real tools: AVR, then PIC.  **Main chip:** ATmega328P, then PIC16F18857.

**New chips:** [ATmega328P-PU](https://www.microchip.com/en-us/product/ATmega328P) (classic 8-bit AVR (the chip in an Arduino Uno): 32 KB flash, 10-bit ADC, UART, SPI, I2C); [PIC16F18857-I/SP](https://www.microchip.com/en-us/product/PIC16F18857) (8-bit PIC16 with many built-in peripherals: the course's PIC16 all-rounder).

**Builds:** 1. Blink; 2. Button; 3. The dice.

**Project ideas:** Add a six-celebration; A high-roll mode.

### Month 2: Workshop Command Centre (complete)

**Subject:** I2C and port expanders.  **Main chip:** PIC18F47K42.

**New chips:** [PIC18F47K42-I/P](https://www.microchip.com/en-us/product/PIC18F47K42) (8-bit PIC18, 64 MHz, 128 KB flash, 12-bit ADC: the course's PIC18 all-rounder); [MCP23017-E/SP](https://www.microchip.com/en-us/product/MCP23017) (16-bit I2C I/O expander).

**Builds:** 1. Blink; 2. Hello expander; 3. LED chase; 4. Command centre.

**Project ideas:** A fourth animation; Two-button combos.

### Month 3: Analogue in, analogue out (complete)

**Subject:** SPI, ADC and DAC.  **Main chip:** PIC18F47K42.

**New chips:** [MCP3008-I/P](https://www.microchip.com/en-us/product/MCP3008) (8-channel 10-bit SPI analogue-to-digital converter); [MCP4822-E/P](https://www.microchip.com/en-us/product/MCP4822) (2-channel 12-bit SPI digital-to-analogue converter).

**Also uses:** PIC18F47K42-I/P (from earlier months).

**Builds:** 1. Read a knob; 2. Add the DAC; 3. Loop the DAC back.

**Project ideas:** Voltage divider range test.

### Month 4: The binary clock (complete)

**Subject:** porting a program; a real-time clock.  **Main chip:** PIC16F18446.

**New chips:** [PIC16F18446-I/P](https://www.microchip.com/en-us/product/PIC16F18446) (20-pin PIC16, a smaller cousin of the PIC16F18857); [MCP7940N-I/P](https://www.microchip.com/en-us/product/MCP7940N) (I2C real-time clock with battery input; needs a 32.768 kHz crystal).

**Builds:** 1. Blink on a new chip; 2. Meet the RTC; 3. Binary clock.

**Project ideas:** Keep time with a coin cell.

### Month 5: A 16-bit chip at 3.3 V (complete)

**Subject:** PIC24, XC16 and EEPROM.  **Main chip:** PIC24FJ64GA002.

**New chips:** [PIC24FJ64GA002-I/SP](https://www.microchip.com/en-us/product/PIC24FJ64GA002) (16-bit PIC24F microcontroller (3.3 V only)); [24LC512-I/P](https://www.microchip.com/en-us/product/24LC512) (512 Kbit (64 KB) I2C EEPROM).

**Builds:** 1. Blink at 3.3 V; 2. EEPROM hello; 3. Boot counter.

**Project ideas:** Press-and-hold to reset the counter.

### Month 6: SPI memory (planned)

**Subject:** hardware SPI with pin mapping.  **Main chip:** PIC24FJ64GA002.

**New chips:** [25LC1024-I/P](https://www.microchip.com/en-us/product/25LC1024) (1 Mbit (128 KB) SPI EEPROM); [23LC1024-I/P](https://www.microchip.com/en-us/product/23LC1024) (1 Mbit (128 KB) SPI SRAM).

**Also uses:** PIC24FJ64GA002-I/SP (from earlier months).

**Builds:** 1. Hardware SPI hello; 2. Write and verify the EEPROM; 3. SRAM as a fast buffer.

**Project ideas:** Memory tester; Tape recorder: record button presses and replay them; Stream ADC readings into memory.

### Month 7: Hardware SPI and I2C on AVR (planned)

**Subject:** expanders on a classic AVR.  **Main chip:** ATmega328P.

**New chips:** [MCP23S17-E/SP](https://www.microchip.com/en-us/product/MCP23S17) (16-bit SPI I/O expander); [MCP23008-E/P](https://www.microchip.com/en-us/product/MCP23008) (8-bit I2C I/O expander).

**Also uses:** ATmega328P-PU (from earlier months).

**Builds:** 1. TWI hello (MCP23008); 2. SPI hello (MCP23S17); 3. Both: 16 LEDs.

**Project ideas:** 16-LED bar graph; Keypad scanner; A memory-game.

### Month 8: USB two ways (planned)

**Subject:** a USB bridge and native USB.  **Main chip:** PC + PIC16F1454, PIC18F47K42.

**New chips:** [MCP2221A-I/P](https://www.microchip.com/en-us/product/MCP2221A) (USB to UART / I2C / GPIO bridge); [PIC16F1454-I/P](https://www.microchip.com/en-us/product/PIC16F1454) (8-bit PIC with full-speed USB built in).

**Also uses:** PIC18F47K42-I/P (from earlier months).

**Builds:** 1. USB serial echo (MCP2221A); 2. A PC command console; 3. A native USB device (PIC16F1454).

**Project ideas:** Serial dashboard of ADC readings; Set the clock chip from a PC; A USB HID button box.

### Month 9: Sensing the world (planned)

**Subject:** analogue and digital temperature sensors.  **Main chip:** ATmega328P.

**New chips:** [MCP9700A-E/TO](https://www.microchip.com/en-us/product/MCP9700A) (analogue temperature sensor: 10 mV per °C, 500 mV at 0 °C); [TC74A0-5.0VAT](https://www.microchip.com/en-us/product/TC74) (digital I2C temperature sensor).

**Also uses:** ATmega328P-PU, 24LC512-I/P (from earlier months).

**Builds:** 1. Thermometer on a bar graph; 2. Read the I2C sensor and compare; 3. Log temperatures to memory.

**Project ideas:** Min/max thermometer; Frost alarm; A calibration table.

### Month 10: Op-amps and comparators (planned)

**Subject:** conditioning analogue signals.  **Main chip:** PIC16F18857.

**New chips:** [MCP6004-I/P](https://www.microchip.com/en-us/product/MCP6004) (quad rail-to-rail op-amp); [MCP6542-I/P](https://www.microchip.com/en-us/product/MCP6542) (dual comparator).

**Also uses:** PIC16F18857-I/SP (from earlier months).

**Builds:** 1. Buffer and amplify; 2. Light switch with an LDR and hysteresis; 3. PWM into a filter.

**Project ideas:** Night-light; A clap switch; A PWM digital-to-analogue converter.

### Month 11: Programmable analogue (planned)

**Subject:** digital pots and programmable gain.  **Main chip:** PIC18F47K42.

**New chips:** [MCP4151-103E/P](https://www.microchip.com/en-us/product/MCP4151) (10 kΩ 8-bit digital potentiometer (SPI)); [MCP6S21-I/P](https://www.microchip.com/en-us/product/MCP6S21) (programmable-gain amplifier (SPI)).

**Also uses:** PIC18F47K42-I/P (from earlier months).

**Builds:** 1. Digital volume control; 2. Gain switching; 3. Auto-ranging meter.

**Project ideas:** Digital volume control; Programmable LED dimmer; Auto-gain light meter.

### Month 12: Power and reset (planned)

**Subject:** building your own supply.  **Main chip:** PIC18F47K42.

**New chips:** [MCP1702-3302E/TO](https://www.microchip.com/en-us/product/MCP1702) (low-dropout 3.3 V voltage regulator (250 mA)); [MCP100-xxx/TO (about 4.5 V threshold)](https://www.microchip.com/en-us/product/MCP100) (voltage supervisor: holds a chip in reset until the supply is healthy).

**Also uses:** PIC18F47K42-I/P, PIC24FJ64GA002-I/SP (from earlier months).

**Builds:** 1. Build a 3.3 V supply; 2. Watch a supervisor reset; 3. Power the Month 5 board.

**Project ideas:** Brown-out demonstration; Power-on sequencer.

### Month 13: dsPIC33: a signal controller (planned)

**Subject:** a new family and precision measurement.  **Main chip:** dsPIC33EV.

**New chips:** [dsPIC33EV128GM002-I/SP](https://www.microchip.com/en-us/product/dsPIC33EV128GM002) (16-bit digital signal controller (5 V) with motor-control PWM); [MCP3551-E/P](https://www.microchip.com/en-us/product/MCP3551) (22-bit delta-sigma ADC for precise measurements).

**Builds:** 1. Blink and clock set-up; 2. Timers and PWM; 3. Precision ADC over SPI.

**Project ideas:** LED fade with hardware PWM; Tone generator; Frequency counter; A strain-gauge-style bridge reader.

### Month 14: Waveforms with a real reference (planned)

**Subject:** DAC output with an external reference.  **Main chip:** dsPIC33EV.

**New chips:** [MCP4922-E/P](https://www.microchip.com/en-us/product/MCP4922) (dual 12-bit DAC with external reference inputs); [MCP1525-I/TO](https://www.microchip.com/en-us/product/MCP1525) (2.5 V precision voltage reference).

**Also uses:** dsPIC33EV128GM002-I/SP, MCP6004-I/P (from earlier months).

**Builds:** 1. PWM and an RC filter; 2. Sine, triangle, saw from a table; 3. Two-knob generator.

**Project ideas:** Function generator; Tone sequencer; Siren.

### Month 15: PIC32: a 32-bit chip (planned)

**Subject:** a new family, a second clock chip.  **Main chip:** PIC32MX (3.3 V).

**New chips:** [PIC32MX170F256B-I/SP](https://www.microchip.com/en-us/product/PIC32MX170F256B) (32-bit MIPS microcontroller (3.3 V)); [MCP79410-I/P](https://www.microchip.com/en-us/product/MCP79410) (I2C real-time clock with EEPROM and a unique ID).

**Builds:** 1. Blink and clock; 2. Port the Month 4 clock; 3. Port the Month 5 EEPROM counter.

**Project ideas:** Speed comparison across families; Terminal clock.

### Month 16: Other serial buses (planned)

**Subject:** one-wire and Microwire EEPROMs; portable drivers.  **Main chip:** any of your chips.

**New chips:** [11LC010-I/TO](https://www.microchip.com/en-us/product/11LC010) (1 Kbit single-wire (UNI/O) EEPROM); [93LC66B-I/P](https://www.microchip.com/en-us/product/93LC66B) (4 Kbit Microwire EEPROM).

**Also uses:** ATmega328P-PU, PIC18F47K42-I/P, PIC24FJ64GA002-I/SP, PIC32MX170F256B-I/SP (from earlier months).

**Builds:** 1. One-wire (UNI/O) EEPROM; 2. Microwire EEPROM; 3. A portable driver on four families.

**Project ideas:** A portable library for your chips; A benchmark table.

### Month 17: Tiny chips: AVR and PIC (planned)

**Subject:** eight-pin microcontrollers.  **Main chip:** ATtiny85, PIC12F1840.

**New chips:** [ATtiny85-20PU](https://www.microchip.com/en-us/product/ATtiny85) (tiny 8-pin AVR); [PIC12F1840-I/P](https://www.microchip.com/en-us/product/PIC12F1840) (tiny 8-pin PIC).

**Builds:** 1. Blink on five pins; 2. Analogue read and PWM; 3. Charlieplexing: six LEDs from three pins.

**Project ideas:** A tiny dice; A knob-controlled LED; A one-chip light sensor.

### Month 18: Bigger and newer AVRs (planned)

**Subject:** a large classic AVR and a modern one.  **Main chip:** ATmega1284P, AVR128DB28.

**New chips:** [ATmega1284P-PU](https://www.microchip.com/en-us/product/ATmega1284P) (large classic AVR: 128 KB flash, 16 KB RAM); [AVR128DB28-I/SP](https://www.microchip.com/en-us/product/AVR128DB28) (modern AVR with event system and UPDI programming (optional month)).

**Builds:** 1. Large-AVR blink and timers; 2. Modern AVR blink (UPDI); 3. Event system and configurable logic.

**Project ideas:** An LED driven by hardware only; A frequency meter.

### Month 19: Data logger (planned)

**Subject:** putting several chips together.  **Main chip:** any of your chips.

**New chips:** [MCP3202-CI/P](https://www.microchip.com/en-us/product/MCP3202) (2-channel 12-bit SPI ADC); [24AA02E48-I/P](https://www.microchip.com/en-us/product/24AA02E48) (I2C EEPROM with a factory-programmed unique MAC address).

**Also uses:** MCP7940N-I/P, 24LC512-I/P, MCP9700A-E/TO, TC74A0-5.0VAT (from earlier months).

**Builds:** 1. Log one reading a minute; 2. Read the log back over serial; 3. Sleep between readings.

**Project ideas:** Greenhouse logger; Fridge monitor; Plant-watering log.

### Month 20: CAN bus: two nodes (planned)

**Subject:** a real network.  **Main chip:** PIC18F47K42 + ATmega328P.

**New chips:** [MCP2515-I/P](https://www.microchip.com/en-us/product/MCP2515) (CAN bus controller (SPI)); [MCP2562-E/P](https://www.microchip.com/en-us/product/MCP2562) (CAN bus transceiver).

**Also uses:** PIC18F47K42-I/P, ATmega328P-PU, 24AA02E48-I/P (from earlier months).

**Builds:** 1. One node transmitting; 2. Two nodes: button to LED; 3. A small status protocol.

**Project ideas:** Remote sensor; Two-player reaction game; A bus-error demonstration.

### Month 21: Motors and power switching (planned)

**Subject:** driving real loads.  **Main chip:** dsPIC33EV or PIC16F18857.

**New chips:** [MCP1407-E/P](https://www.microchip.com/en-us/product/MCP1407) (6 A MOSFET gate driver); [MCP6022-I/P](https://www.microchip.com/en-us/product/MCP6022) (dual 10 MHz rail-to-rail op-amp).

**Also uses:** dsPIC33EV128GM002-I/SP (from earlier months).

**Builds:** 1. Switch a lamp; 2. Motor speed with a knob; 3. Servo and current limit.

**Project ideas:** Fan controller; Servo gauge for the data logger; Motor stall detector.

### Month 22: Sound and signals (planned)

**Subject:** audio with a negative supply and stereo gain.  **Main chip:** dsPIC33EV.

**New chips:** [TC7660EPA](https://www.microchip.com/en-us/product/TC7660) (charge-pump voltage inverter: makes a negative supply); [MCP6S22-I/P](https://www.microchip.com/en-us/product/MCP6S22) (dual programmable-gain amplifier (SPI)).

**Also uses:** dsPIC33EV128GM002-I/SP, MCP4922-E/P, MCP6004-I/P (from earlier months).

**Builds:** 1. A tone and a chord; 2. A melody player; 3. A simple synth.

**Project ideas:** Theremin-style instrument; Drum machine; Sound-level meter.

### Month 23: Low power (planned)

**Subject:** running for months on a battery.  **Main chip:** PIC or AVR.

**New chips:** [MCP1700-3302E/TO](https://www.microchip.com/en-us/product/MCP1700) (ultra-low-quiescent-current 3.3 V regulator); [TC54VN3002EZB (about 3.0 V)](https://www.microchip.com/en-us/product/TC54) (voltage detector: a battery-low warning).

**Also uses:** MCP7940N-I/P (from earlier months).

**Builds:** 1. Sleep and wake on a button; 2. Wake on the clock alarm; 3. Battery-low warning.

**Project ideas:** Coin-cell blinker; A sleeping logger; A battery-voltage gauge.

### Month 24: Capstone (planned)

**Subject:** design and build your own.  **Main chip:** your choice.

**New chips:** two of your choice from the shortlist: [MCP23S08-E/P](https://www.microchip.com/en-us/product/MCP23S08), [MCP4261-103E/P](https://www.microchip.com/en-us/product/MCP4261), [MCP3208-CI/P](https://www.microchip.com/en-us/product/MCP3208), [MCP9701A-E/TO](https://www.microchip.com/en-us/product/MCP9701A), [ATtiny84A-PU](https://www.microchip.com/en-us/product/ATtiny84A), [MCP2200-I/P](https://www.microchip.com/en-us/product/MCP2200).

**Builds:** 1. Plan and wire; 2. Program; 3. Test and document.

**Project ideas:** Weather station; CAN-linked sensor network; Synthesizer; Motor-driven gauge.
