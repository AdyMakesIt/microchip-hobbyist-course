#!/usr/bin/env python3
"""
course_data.py - the ONE place that defines the course plan and the parts.

make_purchasing.py reads this (and the circuit descriptions for Months 1-5) and writes:
  start-here/course-overview.md, start-here/purchasing-plan.md, start-here/parts-catalogue.md and the CSV files.

Edit this file to change the plan; then run:  python3 maintainer/tools/make_purchasing.py
Months 1-5 take their lab-stock quantities from the verified circuits; Months 6-24 use the estimates below.
"""

# ----------------------------------------------------------------------------------------------
# CHIPS (free samples).  base = part name used for the manufacturer's product page.
# ----------------------------------------------------------------------------------------------
def chip(pn, base, pkg, supply, what):
    return dict(kind="chip", pn=pn, base=base, pkg=pkg, supply=supply, what=what)

CHIPS = {
    # ---- months 1 to 5
    "atmega328p":   chip("ATmega328P-PU", "ATmega328P", "PDIP-28", "1.8–5.5 V", "classic 8-bit AVR (the chip in an Arduino Uno): 32 KB flash, 10-bit ADC, UART, SPI, I2C"),
    "pic16f18857":  chip("PIC16F18857-I/SP", "PIC16F18857", "SPDIP-28", "2.3–5.5 V", "8-bit PIC16 with many built-in peripherals: the course's PIC16 all-rounder"),
    "pic18f47k42":  chip("PIC18F47K42-I/P", "PIC18F47K42", "PDIP-40", "1.8–5.5 V", "8-bit PIC18, 64 MHz, 128 KB flash, 12-bit ADC: the course's PIC18 all-rounder"),
    "mcp23017":     chip("MCP23017-E/SP", "MCP23017", "SPDIP-28", "1.8–5.5 V", "16-bit I2C I/O expander"),
    "mcp3008":      chip("MCP3008-I/P", "MCP3008", "PDIP-16", "2.7–5.5 V", "8-channel 10-bit SPI analogue-to-digital converter"),
    "mcp4822":      chip("MCP4822-E/P", "MCP4822", "PDIP-8", "2.7–5.5 V", "2-channel 12-bit SPI digital-to-analogue converter"),
    "pic16f18446":  chip("PIC16F18446-I/P", "PIC16F18446", "PDIP-20", "1.8–5.5 V", "20-pin PIC16, a smaller cousin of the PIC16F18857"),
    "mcp7940n":     chip("MCP7940N-I/P", "MCP7940N", "PDIP-8", "1.8–5.5 V", "I2C real-time clock with battery input; needs a 32.768 kHz crystal"),
    "pic24fj64ga002": chip("PIC24FJ64GA002-I/SP", "PIC24FJ64GA002", "SPDIP-28", "2.0–3.6 V", "16-bit PIC24F microcontroller (3.3 V only)"),
    "24lc512":      chip("24LC512-I/P", "24LC512", "PDIP-8", "2.5–5.5 V", "512 Kbit (64 KB) I2C EEPROM"),
    # ---- months 6 to 24
    "25lc1024":     chip("25LC1024-I/P", "25LC1024", "PDIP-8", "2.5–5.5 V", "1 Mbit (128 KB) SPI EEPROM"),
    "23lc1024":     chip("23LC1024-I/P", "23LC1024", "PDIP-8", "2.5–5.5 V", "1 Mbit (128 KB) SPI SRAM"),
    "mcp23s17":     chip("MCP23S17-E/SP", "MCP23S17", "SPDIP-28", "1.8–5.5 V", "16-bit SPI I/O expander"),
    "mcp23008":     chip("MCP23008-E/P", "MCP23008", "PDIP-18", "1.8–5.5 V", "8-bit I2C I/O expander"),
    "mcp2221a":     chip("MCP2221A-I/P", "MCP2221A", "PDIP-14", "3.0–5.5 V", "USB to UART / I2C / GPIO bridge"),
    "pic16f1454":   chip("PIC16F1454-I/P", "PIC16F1454", "PDIP-14", "2.3–5.5 V", "8-bit PIC with full-speed USB built in"),
    "mcp9700a":     chip("MCP9700A-E/TO", "MCP9700A", "TO-92", "2.3–5.5 V", "analogue temperature sensor: 10 mV per °C, 500 mV at 0 °C"),
    "tc74":         chip("TC74A0-5.0VAT", "TC74", "TO-220-5", "4.5–5.5 V", "digital I2C temperature sensor"),
    "mcp6004":      chip("MCP6004-I/P", "MCP6004", "PDIP-14", "1.8–6.0 V", "quad rail-to-rail op-amp"),
    "mcp6542":      chip("MCP6542-I/P", "MCP6542", "PDIP-8", "1.6–5.5 V", "dual comparator"),
    "mcp4151":      chip("MCP4151-103E/P", "MCP4151", "PDIP-8", "1.8–5.5 V", "10 kΩ 8-bit digital potentiometer (SPI)"),
    "mcp6s21":      chip("MCP6S21-I/P", "MCP6S21", "PDIP-8", "2.5–5.5 V", "programmable-gain amplifier (SPI)"),
    "mcp1702":      chip("MCP1702-3302E/TO", "MCP1702", "TO-92", "in up to 13.2 V", "low-dropout 3.3 V voltage regulator (250 mA)"),
    "mcp100":       chip("MCP100-xxx/TO (about 4.5 V threshold)", "MCP100", "TO-92", "1.0–5.5 V", "voltage supervisor: holds a chip in reset until the supply is healthy"),
    "dspic33ev":    chip("dsPIC33EV128GM002-I/SP", "dsPIC33EV128GM002", "SPDIP-28", "4.5–5.5 V", "16-bit digital signal controller (5 V) with motor-control PWM"),
    "mcp3551":      chip("MCP3551-E/P", "MCP3551", "PDIP-8", "2.7–5.5 V", "22-bit delta-sigma ADC for precise measurements"),
    "mcp4922":      chip("MCP4922-E/P", "MCP4922", "PDIP-14", "2.7–5.5 V", "dual 12-bit DAC with external reference inputs"),
    "mcp1525":      chip("MCP1525-I/TO", "MCP1525", "TO-92", "2.7–5.5 V", "2.5 V precision voltage reference"),
    "pic32mx170":   chip("PIC32MX170F256B-I/SP", "PIC32MX170F256B", "SPDIP-28", "2.3–3.6 V", "32-bit MIPS microcontroller (3.3 V)"),
    "mcp79410":     chip("MCP79410-I/P", "MCP79410", "PDIP-8", "1.8–5.5 V", "I2C real-time clock with EEPROM and a unique ID"),
    "11lc010":      chip("11LC010-I/TO", "11LC010", "TO-92", "2.5–5.5 V", "1 Kbit single-wire (UNI/O) EEPROM"),
    "93lc66b":      chip("93LC66B-I/P", "93LC66B", "PDIP-8", "2.5–5.5 V", "4 Kbit Microwire EEPROM"),
    "attiny85":     chip("ATtiny85-20PU", "ATtiny85", "PDIP-8", "2.7–5.5 V", "tiny 8-pin AVR"),
    "pic12f1840":   chip("PIC12F1840-I/P", "PIC12F1840", "PDIP-8", "1.8–5.5 V", "tiny 8-pin PIC"),
    "atmega1284p":  chip("ATmega1284P-PU", "ATmega1284P", "PDIP-40", "1.8–5.5 V", "large classic AVR: 128 KB flash, 16 KB RAM"),
    "avr128db28":   chip("AVR128DB28-I/SP", "AVR128DB28", "SPDIP-28", "1.8–5.5 V", "modern AVR with event system and UPDI programming (optional month)"),
    "mcp3202":      chip("MCP3202-CI/P", "MCP3202", "PDIP-8", "2.7–5.5 V", "2-channel 12-bit SPI ADC"),
    "24aa02e48":    chip("24AA02E48-I/P", "24AA02E48", "PDIP-8", "1.7–5.5 V", "I2C EEPROM with a factory-programmed unique MAC address"),
    "mcp2515":      chip("MCP2515-I/P", "MCP2515", "PDIP-18", "2.7–5.5 V", "CAN bus controller (SPI)"),
    "mcp2562":      chip("MCP2562-E/P", "MCP2562", "PDIP-8", "4.5–5.5 V", "CAN bus transceiver"),
    "mcp1407":      chip("MCP1407-E/P", "MCP1407", "PDIP-8", "4.5–18 V", "6 A MOSFET gate driver"),
    "mcp6022":      chip("MCP6022-I/P", "MCP6022", "PDIP-8", "2.5–5.5 V", "dual 10 MHz rail-to-rail op-amp"),
    "tc7660":       chip("TC7660EPA", "TC7660", "PDIP-8", "1.5–10 V", "charge-pump voltage inverter: makes a negative supply"),
    "mcp6s22":      chip("MCP6S22-I/P", "MCP6S22", "PDIP-8", "2.5–5.5 V", "dual programmable-gain amplifier (SPI)"),
    "mcp1700":      chip("MCP1700-3302E/TO", "MCP1700", "TO-92", "2.3–6.0 V", "ultra-low-quiescent-current 3.3 V regulator"),
    "tc54":         chip("TC54VN3002EZB (about 3.0 V)", "TC54", "TO-92", "0.7–10 V", "voltage detector: a battery-low warning"),
    # ---- capstone shortlist (Month 24: choose two)
    "mcp23s08":     chip("MCP23S08-E/P", "MCP23S08", "PDIP-18", "1.8–5.5 V", "8-bit SPI I/O expander"),
    "mcp4261":      chip("MCP4261-103E/P", "MCP4261", "PDIP-14", "1.8–5.5 V", "dual 10 kΩ digital potentiometer (SPI)"),
    "mcp3208":      chip("MCP3208-CI/P", "MCP3208", "PDIP-16", "2.7–5.5 V", "8-channel 12-bit SPI ADC"),
    "mcp9701a":     chip("MCP9701A-E/TO", "MCP9701A", "TO-92", "3.1–5.5 V", "analogue temperature sensor with a steeper slope than the MCP9700A"),
    "attiny84a":    chip("ATtiny84A-PU", "ATtiny84A", "PDIP-14", "1.7–5.5 V", "14-pin AVR with more pins than the ATtiny85"),
    "mcp2200":      chip("MCP2200-I/P", "MCP2200", "PDIP-20", "3.0–5.5 V", "USB to UART bridge"),
}
CAPSTONE_SHORTLIST = ["mcp23s08", "mcp4261", "mcp3208", "mcp9701a", "attiny84a", "mcp2200"]

# ----------------------------------------------------------------------------------------------
# LAB STOCK (general parts bought once and reused).  commodity=True: usually sold in cheap assortments.
# ----------------------------------------------------------------------------------------------
def stock(name, spec, search, commodity, order=0, unit="pcs"):
    return dict(kind="stock", name=name, spec=spec, search=search, commodity=commodity, order=order, unit=unit)

STOCK = {
    "led":      stock("LED, 5 mm, red", "forward voltage about 2 V, 20 mA maximum; we run them at about 4 mA", "5mm red LED assortment 100", True, 1),
    "r100":     stock("Resistor 100 Ω", "1/4 W metal film, E12 series", "resistor kit 1/4W E12 assortment", True, 2),
    "r330":     stock("Resistor 330 Ω", "LED resistor at 3.3 V", "resistor kit 1/4W E12 assortment", True, 3),
    "r680":     stock("Resistor 680 Ω", "LED resistor at 5 V", "resistor kit 1/4W E12 assortment", True, 4),
    "r1k":      stock("Resistor 1 kΩ", "", "resistor kit 1/4W E12 assortment", True, 5),
    "r4k7":     stock("Resistor 4.7 kΩ", "I2C pull-ups", "resistor kit 1/4W E12 assortment", True, 6),
    "r10k":     stock("Resistor 10 kΩ", "reset and button pull-ups", "resistor kit 1/4W E12 assortment", True, 7),
    "r100k":    stock("Resistor 100 kΩ", "", "resistor kit 1/4W E12 assortment", True, 8),
    "r120":     stock("Resistor 120 Ω", "CAN bus terminator", "resistor kit 1/4W E12 assortment", True, 9),
    "rsense":   stock("Resistor 0.1 Ω, 1 W", "current-sense resistor", "0.1 ohm 1W resistor", False, 10),
    "c10p":     stock("Capacitor 10 pF, ceramic", "crystal load capacitor", "ceramic capacitor assortment kit", True, 11),
    "c22p":     stock("Capacitor 22 pF, ceramic", "crystal load capacitor", "ceramic capacitor assortment kit", True, 12),
    "c100n":    stock("Capacitor 100 nF, ceramic", "decoupling: one next to every chip", "ceramic capacitor assortment kit 100nF", True, 13),
    "c1u":      stock("Capacitor 1 µF, ceramic", "reference and regulator capacitor", "ceramic capacitor assortment kit 1uF", True, 14),
    "c10u":     stock("Capacitor 10 µF, ceramic", "low-ESR core-regulator capacitor", "10uF ceramic capacitor", True, 15),
    "c100u":    stock("Capacitor 100 µF, electrolytic", "audio and supply smoothing", "electrolytic capacitor assortment kit", True, 16),
    "btn":      stock("Push button, 6 mm", "4-leg tact switch", "6x6mm tactile push button switch", True, 17),
    "pot10k":   stock("Potentiometer 10 kΩ, linear", "rotary or trimmer, 3 legs", "10K potentiometer B10K", True, 18),
    "piezo":    stock("Piezo disc, passive", "no oscillator inside", "passive piezo buzzer disc", True, 19),
    "ldr":      stock("LDR (light-dependent resistor)", "a few kΩ in light, hundreds of kΩ in the dark", "LDR photoresistor 5mm", False, 20),
    "speaker":  stock("Speaker, 8 Ω, small", "0.25 to 0.5 W", "8 ohm 0.5W small speaker", False, 21),
    "xtal32k":  stock("Crystal, 32.768 kHz watch type", "6 pF to 9 pF load, 2 legs", "32.768kHz crystal 6pF", False, 22),
    "xtal16m":  stock("Crystal, 16 MHz, HC-49", "", "16MHz crystal HC-49", False, 23),
    "xtal8m":   stock("Crystal, 8 MHz, HC-49", "", "8MHz crystal HC-49", False, 24),
    "mosfet":   stock("MOSFET, N-channel, logic-level", "switches loads from a 3.3 V or 5 V pin (for example IRLZ44N or IRLB8721 type)", "IRLZ44N logic level MOSFET", False, 25),
    "diode":    stock("Diode, 1N5819 or 1N4007", "motor flyback protection", "1N5819 Schottky diode", False, 26),
    "motor":    stock("DC motor, small (3 to 6 V)", "toy motor", "small DC motor 3V 6V", False, 27),
    "servo":    stock("Hobby servo, SG90 type", "", "SG90 micro servo", False, 28),
    "usbbrk":   stock("USB socket breakout board", "micro-USB or USB-B with 0.1 inch pins", "micro USB breakout board 2.54mm", False, 29),
    "keypad":   stock("Keypad, 4×4 membrane (optional)", "8 pins", "4x4 matrix membrane keypad", False, 30),
    "cr2032":   stock("CR2032 cell and holder", "backup battery for the clock chip", "CR2032 battery holder", False, 31),
    "bb2":      stock("Second breadboard", "830 points", "830 point breadboard", True, 32),
    "wires":    stock("Jumper wires, male-to-male", "assorted lengths", "jumper wire kit male to male 65pcs", True, 33),
    "dupont":   stock("Dupont leads, female-to-male", "programmer leads", "dupont wire female to male 20cm", True, 34),
}

# the tools bought once (shown in the purchasing plan's first round)
TOOLS = [
    ("Solderless breadboard, 830 points", "the full-size kind with 63 columns", "830 point breadboard", 1),
    ("Breadboard power supply, MB102 style", "5 V / 3.3 V jumper selection", "MB102 breadboard power supply module", 1),
    ("Multimeter", "continuity beep and DC volts", "digital multimeter", 1),
    ("PICkit 3 programmer (original or clone)", "for the PIC chips", "PICkit 3 programmer", 1),
    ("AVR programmer: USBasp, or an Arduino Uno R3", "for the AVR chips", "USBasp programmer", 1),
]

# ----------------------------------------------------------------------------------------------
# THE PLAN.  samples = the TWO new chips ordered (three of each) that month.
#   uses  = other chips from earlier months that the month also uses (so the reader can see the whole bill of chips)
#   stock = lab-stock quantities for Months 6 to 24 (estimates); Months 1 to 5 are computed from the circuits.
# ----------------------------------------------------------------------------------------------
def month(n, title, theme, host, samples, learn, builds, projects, stock=None, buy="", status="planned", uses=()):
    return dict(n=n, title=title, theme=theme, host=host, samples=list(samples), learn=learn, builds=list(builds),
                projects=list(projects), stock=stock or {}, buy=buy, status=status, uses=list(uses))

PLAN = [
    month(1, "Electronic dice", "the real tools: AVR, then PIC", "ATmega328P, then PIC16F18857", ["atmega328p", "pic16f18857"],
          "Plain C without the Arduino IDE; outputs and inputs; a PICkit 3 and a USBasp or Uno as programmers",
          ["Blink", "Button", "The dice"], ["Add a six-celebration", "A high-roll mode"], status="built"),
    month(2, "Workshop Command Centre", "I2C and port expanders", "PIC18F47K42", ["pic18f47k42", "mcp23017"],
          "I2C by hand; fault codes; edge detection", ["Blink", "Hello expander", "LED chase", "Command centre"], ["A fourth animation", "Two-button combos"], status="built"),
    month(3, "Analogue in, analogue out", "SPI, ADC and DAC", "PIC18F47K42", ["mcp3008", "mcp4822"],
          "SPI by hand; converting voltages to numbers and back; self-tests", ["Read a knob", "Add the DAC", "Loop the DAC back"], ["Voltage divider range test"], status="built", uses=["pic18f47k42"]),
    month(4, "The binary clock", "porting a program; a real-time clock", "PIC16F18446", ["pic16f18446", "mcp7940n"],
          "Moving a program between chips of one family; BCD; a 32.768 kHz crystal", ["Blink on a new chip", "Meet the RTC", "Binary clock"], ["Keep time with a coin cell"], status="built"),
    month(5, "A 16-bit chip at 3.3 V", "PIC24, XC16 and EEPROM", "PIC24FJ64GA002", ["pic24fj64ga002", "24lc512"],
          "3.3 V supplies; a 16-bit core; EEPROM pages and ACK polling", ["Blink at 3.3 V", "EEPROM hello", "Boot counter"], ["Press-and-hold to reset the counter"], status="built"),
    month(6, "SPI memory", "hardware SPI with pin mapping", "PIC24FJ64GA002", ["25lc1024", "23lc1024"],
          "The PIC24's built-in SPI and peripheral pin select; EEPROM versus SRAM speed", ["Hardware SPI hello", "Write and verify the EEPROM", "SRAM as a fast buffer"],
          ["Memory tester", "Tape recorder: record button presses and replay them", "Stream ADC readings into memory"],
          {"led": 9, "r330": 9, "r10k": 2, "c100n": 4, "c10u": 1, "btn": 2, "wires": 40, "dupont": 5}, uses=["pic24fj64ga002"]),
    month(7, "Hardware SPI and I2C on AVR", "expanders on a classic AVR", "ATmega328P", ["mcp23s17", "mcp23008"],
          "The ATmega328P's SPI and TWI hardware; comparing SPI and I2C", ["TWI hello (MCP23008)", "SPI hello (MCP23S17)", "Both: 16 LEDs"],
          ["16-LED bar graph", "Keypad scanner", "A memory-game"],
          {"led": 16, "r680": 16, "r10k": 2, "r4k7": 2, "c100n": 4, "btn": 2, "keypad": 1, "wires": 45, "dupont": 5}, uses=["atmega328p"]),
    month(8, "USB two ways", "a USB bridge and native USB", "PC + PIC16F1454, PIC18F47K42", ["mcp2221a", "pic16f1454"],
          "A USB-to-serial bridge; a PIC with USB built in; the first use of Microchip's code generator (MCC) for a large library",
          ["USB serial echo (MCP2221A)", "A PC command console", "A native USB device (PIC16F1454)"],
          ["Serial dashboard of ADC readings", "Set the clock chip from a PC", "A USB HID button box"],
          {"led": 4, "r680": 4, "r10k": 1, "c100n": 3, "c1u": 2, "btn": 1, "usbbrk": 1, "wires": 30, "dupont": 5}, uses=["pic18f47k42"]),
    month(9, "Sensing the world", "analogue and digital temperature sensors", "ATmega328P", ["mcp9700a", "tc74"],
          "ADC accuracy; analogue versus digital sensors; logging to the EEPROM",
          ["Thermometer on a bar graph", "Read the I2C sensor and compare", "Log temperatures to memory"],
          ["Min/max thermometer", "Frost alarm", "A calibration table"],
          {"led": 8, "r680": 8, "r10k": 2, "r4k7": 2, "c100n": 3, "c1u": 2, "btn": 1, "wires": 40, "dupont": 5}, uses=["atmega328p", "24lc512"]),
    month(10, "Op-amps and comparators", "conditioning analogue signals", "PIC16F18857", ["mcp6004", "mcp6542"],
          "Buffers, gain, hysteresis and filters", ["Buffer and amplify", "Light switch with an LDR and hysteresis", "PWM into a filter"],
          ["Night-light", "A clap switch", "A PWM digital-to-analogue converter"],
          {"ldr": 1, "pot10k": 1, "r1k": 4, "r10k": 4, "r100k": 2, "c100n": 4, "c10u": 1, "led": 4, "r680": 4, "wires": 40, "dupont": 5}, uses=["pic16f18857"]),
    month(11, "Programmable analogue", "digital pots and programmable gain", "PIC18F47K42", ["mcp4151", "mcp6s21"],
          "Letting software set analogue values over SPI", ["Digital volume control", "Gain switching", "Auto-ranging meter"],
          ["Digital volume control", "Programmable LED dimmer", "Auto-gain light meter"],
          {"speaker": 1, "pot10k": 1, "r100": 1, "c100n": 4, "c10u": 1, "btn": 3, "led": 8, "r680": 8, "wires": 40, "dupont": 5}, uses=["pic18f47k42"]),
    month(12, "Power and reset", "building your own supply", "PIC18F47K42", ["mcp1702", "mcp100"],
          "Regulators, dropout, supervisors and brown-out", ["Build a 3.3 V supply", "Watch a supervisor reset", "Power the Month 5 board"],
          ["Brown-out demonstration", "Power-on sequencer"],
          {"c1u": 2, "pot10k": 1, "c100n": 3, "r10k": 2, "led": 3, "r680": 3, "btn": 1, "wires": 35, "dupont": 5}, uses=["pic18f47k42", "pic24fj64ga002"]),
    month(13, "dsPIC33: a signal controller", "a new family and precision measurement", "dsPIC33EV", ["dspic33ev", "mcp3551"],
          "A fast 16-bit core, timers and PWM; measuring tiny voltages precisely", ["Blink and clock set-up", "Timers and PWM", "Precision ADC over SPI"],
          ["LED fade with hardware PWM", "Tone generator", "Frequency counter", "A strain-gauge-style bridge reader"],
          {"led": 9, "r680": 9, "r10k": 2, "c100n": 3, "c10u": 1, "btn": 2, "pot10k": 1, "wires": 40, "dupont": 5}),
    month(14, "Waveforms with a real reference", "DAC output with an external reference", "dsPIC33EV", ["mcp4922", "mcp1525"],
          "Waveform tables; PWM through a filter; the effect of a precise reference", ["PWM and an RC filter", "Sine, triangle, saw from a table", "Two-knob generator"],
          ["Function generator", "Tone sequencer", "Siren"],
          {"speaker": 1, "c100u": 1, "r100": 1, "r1k": 2, "c100n": 4, "pot10k": 2, "led": 4, "r680": 4, "wires": 40, "dupont": 5}, uses=["dspic33ev", "mcp6004"]),
    month(15, "PIC32: a 32-bit chip", "a new family, a second clock chip", "PIC32MX (3.3 V)", ["pic32mx170", "mcp79410"],
          "XC32; a fast 32-bit core; a clock chip with EEPROM and a unique ID", ["Blink and clock", "Port the Month 4 clock", "Port the Month 5 EEPROM counter"],
          ["Speed comparison across families", "Terminal clock"],
          {"led": 9, "r330": 9, "r10k": 2, "c100n": 4, "c10u": 2, "btn": 2, "xtal32k": 1, "c10p": 2, "r4k7": 2, "wires": 40, "dupont": 5}),
    month(16, "Other serial buses", "one-wire and Microwire EEPROMs; portable drivers", "any of your chips", ["11lc010", "93lc66b"],
          "Bit-banging unusual protocols; separating a hardware layer from a device layer", ["One-wire (UNI/O) EEPROM", "Microwire EEPROM", "A portable driver on four families"],
          ["A portable library for your chips", "A benchmark table"],
          {"led": 4, "r680": 4, "r4k7": 2, "r10k": 3, "c100n": 3, "btn": 2, "wires": 35, "dupont": 5}, uses=["atmega328p", "pic18f47k42", "pic24fj64ga002", "pic32mx170"]),
    month(17, "Tiny chips: AVR and PIC", "eight-pin microcontrollers", "ATtiny85, PIC12F1840", ["attiny85", "pic12f1840"],
          "How little a program can use; comparing a tiny AVR with a tiny PIC", ["Blink on five pins", "Analogue read and PWM", "Charlieplexing: six LEDs from three pins"],
          ["A tiny dice", "A knob-controlled LED", "A one-chip light sensor"],
          {"led": 6, "r680": 6, "r10k": 2, "c100n": 2, "btn": 1, "pot10k": 1, "ldr": 1, "wires": 30, "dupont": 5}),
    month(18, "Bigger and newer AVRs", "a large classic AVR and a modern one", "ATmega1284P, AVR128DB28", ["atmega1284p", "avr128db28"],
          "A 128 KB AVR with more peripherals; the modern AVR's event system (optional month, needs a UPDI programmer)", ["Large-AVR blink and timers", "Modern AVR blink (UPDI)", "Event system and configurable logic"],
          ["An LED driven by hardware only", "A frequency meter"],
          {"led": 9, "r680": 9, "c100n": 3, "btn": 2, "r10k": 2, "r1k": 1, "wires": 40, "dupont": 5}),
    month(19, "Data logger", "putting several chips together", "any of your chips", ["mcp3202", "24aa02e48"],
          "A multi-chip project: clock, memory, sensors, a precise ADC and a node ID", ["Log one reading a minute", "Read the log back over serial", "Sleep between readings"],
          ["Greenhouse logger", "Fridge monitor", "Plant-watering log"],
          {"cr2032": 1, "xtal32k": 1, "c10p": 2, "r4k7": 2, "c100n": 3, "led": 4, "r680": 4, "btn": 2, "wires": 40, "dupont": 5}, uses=["mcp7940n", "24lc512", "mcp9700a", "tc74"]),
    month(20, "CAN bus: two nodes", "a real network", "PIC18F47K42 + ATmega328P", ["mcp2515", "mcp2562"],
          "CAN messages between two different chip families", ["One node transmitting", "Two nodes: button to LED", "A small status protocol"],
          ["Remote sensor", "Two-player reaction game", "A bus-error demonstration"],
          {"xtal8m": 2, "c22p": 4, "r120": 2, "c100n": 6, "led": 6, "r680": 6, "btn": 2, "r10k": 4, "bb2": 1, "wires": 60, "dupont": 5}, uses=["pic18f47k42", "atmega328p", "24aa02e48"]),
    month(21, "Motors and power switching", "driving real loads", "dsPIC33EV or PIC16F18857", ["mcp1407", "mcp6022"],
          "MOSFET switching, PWM speed control, flyback protection and current sensing", ["Switch a lamp", "Motor speed with a knob", "Servo and current limit"],
          ["Fan controller", "Servo gauge for the data logger", "Motor stall detector"],
          {"mosfet": 2, "diode": 2, "motor": 1, "servo": 1, "rsense": 1, "r10k": 2, "r100": 2, "c100n": 3, "c100u": 1, "led": 2, "r680": 2, "pot10k": 1, "btn": 2, "wires": 40, "dupont": 5}, uses=["dspic33ev"]),
    month(22, "Sound and signals", "audio with a negative supply and stereo gain", "dsPIC33EV", ["tc7660", "mcp6s22"],
          "A negative rail for an audio op-amp; stereo programmable gain; a simple synthesizer", ["A tone and a chord", "A melody player", "A simple synth"],
          ["Theremin-style instrument", "Drum machine", "Sound-level meter"],
          {"speaker": 1, "c100u": 1, "c10u": 2, "r1k": 3, "r10k": 3, "pot10k": 2, "c100n": 4, "led": 2, "r680": 2, "btn": 3, "r100": 1, "wires": 40, "dupont": 5}, uses=["dspic33ev", "mcp4922", "mcp6004"]),
    month(23, "Low power", "running for months on a battery", "PIC or AVR", ["mcp1700", "tc54"],
          "Sleep modes, wake-up sources, an ultra-low-power regulator and a battery-low detector", ["Sleep and wake on a button", "Wake on the clock alarm", "Battery-low warning"],
          ["Coin-cell blinker", "A sleeping logger", "A battery-voltage gauge"],
          {"cr2032": 1, "r1k": 1, "c100n": 2, "led": 2, "r680": 2, "btn": 1, "r10k": 1, "wires": 30, "dupont": 5}, uses=["mcp7940n"]),
    month(24, "Capstone", "design and build your own", "your choice", [],
          "Combine at least three chips from earlier months; order two chips of your choice from the shortlist", ["Plan and wire", "Program", "Test and document"],
          ["Weather station", "CAN-linked sensor network", "Synthesizer", "Motor-driven gauge"],
          {"wires": 50, "dupont": 5}, buy="two chips of your choice (see the shortlist)"),
]

PHASES = [
    ("Foundations", 1, 5, "the real tools, the three buses (I2C, SPI) and the first memory chip"),
    ("Buses, memory and analogue", 6, 12, "hardware peripherals and the analogue world"),
    ("New families", 13, 18, "dsPIC33, PIC32, tiny chips and modern AVR, with peripherals you already know"),
    ("Projects", 19, 24, "multi-chip projects, a network, power and sound, and a capstone"),
]

LEARN_LINKS = {
    "microchip": "https://www.microchip.com/en-us/product/{base}",
}

def product_link(base):
    return LEARN_LINKS["microchip"].format(base=base)

def search_links(terms):
    from urllib.parse import quote_plus
    q = quote_plus(terms)
    return {"AliExpress": f"https://www.aliexpress.com/wholesale?SearchText={q}",
            "eBay": f"https://www.ebay.co.uk/sch/i.html?_nkw={q}",
            "Amazon": f"https://www.amazon.co.uk/s?k={q}"}

def octopart_link(pn):
    from urllib.parse import quote_plus
    return f"https://octopart.com/search?q={quote_plus(pn.split(' ')[0])}"
