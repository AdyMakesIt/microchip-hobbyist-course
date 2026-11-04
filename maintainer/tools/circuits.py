#!/usr/bin/env python3
"""Circuit definitions for the course. ONE description per month: schematic chains + breadboard holes."""
from mhc_draw import Circuit, Board

# ---------------------------------------------------------------------------------
# MONTH 1 - PIC16F18857 electronic dice
# ---------------------------------------------------------------------------------
M1_BUILDS = {1: "PIC Build 1 - Blink an LED", 2: "PIC Build 2 - Add the button", 3: "PIC Build 3 - The dice (seven LEDs)"}
AVR1_BUILDS = {1: "AVR Build 1 - Blink an LED", 2: "AVR Build 2 - Add the button", 3: "AVR Build 3 - The dice (seven LEDs)"}

def month1():
    c = Circuit("Month 1")
    c.ic("J1", "PICkit 3 ICSP", 5, "skinny",
         {1: "MCLR", 2: "VDD", 3: "VSS", 4: "PGD", 5: "PGC"}, at=(20, 60),
         sides={1: "R", 2: "R", 3: "R", 4: "R", 5: "R"}, connector=True)
    c.ic("U1", "PIC16F18857-I/SP", 28, "skinny",
         {1: "MCLR", 2: "RA0", 8: "VSS", 11: "RC0", 12: "RC1", 13: "RC2", 14: "RC3", 15: "RC4", 16: "RC5",
          17: "RC6", 19: "VSS", 20: "VDD", 27: "RB6/PGC", 28: "RB7/PGD"}, at=(330, 40),
         sides={1: "L", 2: "L", 8: "L", 19: "L", 20: "L", 27: "L", 28: "L",
                11: "R", 12: "R", 13: "R", 14: "R", 15: "R", 16: "R", 17: "R"})
    # --- build 1
    c.chain(("U1", 20), ["+5V"], 1)
    c.chain(("U1", 8), ["GND"], 1)
    c.chain(("U1", 19), ["GND"], 1)
    c.chain(("U1", 1), ["NET:MCLR"], 1)
    c.chain(("NET", "MCLR"), ["R:R1:10k", "+5V"], 1)
    c.chain(("NET", "+5V"), ["C:C1:100nF", "GND"], 1)
    c.chain(("U1", 28), ["NET:PGD"], 1)
    c.chain(("U1", 27), ["NET:PGC"], 1)
    c.chain(("J1", 1), ["NET:MCLR"], 1)
    c.chain(("J1", 2), ["+5V"], 1)
    c.chain(("J1", 3), ["GND"], 1)
    c.chain(("J1", 4), ["NET:PGD"], 1)
    c.chain(("J1", 5), ["NET:PGC"], 1)
    leds = [(11, "RC0", "D1", "R2", 1, "top left"), (12, "RC1", "D2", "R3", 3, "middle left"),
            (13, "RC2", "D3", "R4", 3, "bottom left"), (14, "RC3", "D4", "R5", 3, "centre"),
            (15, "RC4", "D5", "R6", 3, "top right"), (16, "RC5", "D6", "R7", 3, "middle right"),
            (17, "RC6", "D7", "R8", 3, "bottom right")]
    for pin, nm, d, r, b, pos in leds:
        c.chain(("U1", pin), [f"R:{r}:680R", f"LED:{d}:red", "GND"], b)
    # --- build 2
    c.chain(("U1", 2), ["SW:SW1:ROLL", "GND"], 2)

    b = Board(c)
    b.ic("U1", 8, 1)
    # rails: the supply feeds the LEFT end of the TOP rails; bridge to the bottom rails
    b.wire("TP2", "BP2", 1, "+5V"); b.wire("TN1", "BN1", 1, "GND")
    # power pins
    b.wire("16b", "TP16", 1, "+5V")          # pin 20 VDD
    b.wire("17b", "TN17", 1, "GND")          # pin 19 VSS
    b.wire("15h", "BN15", 1, "GND")          # pin 8 VSS
    b.two("C1", "16c", "17c", 1)             # decoupling across VDD/VSS
    # reset + programmer
    b.two("R1", "8g", "BP8", 1)              # MCLR pull-up
    b.lead("J1", 1, "8h", 1, "MCLR")
    b.lead("J1", 2, "TP5", 1, "VDD")
    b.lead("J1", 3, "TN5", 1, "VSS")
    b.lead("J1", 4, "8c", 1, "PGD")
    b.lead("J1", 5, "9c", 1, "PGC")
    # LED units: wire to (col,a); resistor (col,d)->(col,g); LED (col,h)->bottom GND rail
    pinhole = {11: "18h", 12: "19h", 13: "20h", 14: "21h", 15: "21b", 16: "20b", 17: "19b"}
    for i, (pin, nm, d, r, bld, pos) in enumerate(leds):
        uc = 25 + i
        b.wire(pinhole[pin], f"{uc}a", bld, nm)
        b.two(r, f"{uc}d", f"{uc}g", bld)
        b.two(d, f"{uc}h", f"BN{uc}", bld)
    # button
    b.switch("SW1", 3, 2)
    b.wire("3a", "TN3", 2, "GND")
    b.wire("5g", "9g", 2, "RA0")
    return c, b


# ---------------------------------------------------------------------------------
# MONTH 1, AVR TRACK - ATmega328P electronic dice (programmed through an ISP programmer)
# ---------------------------------------------------------------------------------
def month1_avr():
    c = Circuit("Month 1 AVR")
    c.ic("J1", "ISP programmer", 5, "skinny", {1: "MISO", 2: "SCK", 3: "MOSI", 4: "RESET", 5: "GND"}, at=(20, 60),
         sides={1: "R", 2: "R", 3: "R", 4: "R", 5: "R"}, connector=True, named_only=True)
    names = {1: "RESET", 2: "PD0", 3: "PD1", 4: "PD2", 5: "PD3", 6: "PD4", 7: "VCC", 8: "GND", 11: "PD5", 12: "PD6",
             17: "MOSI (PB3)", 18: "MISO (PB4)", 19: "SCK (PB5)", 20: "AVCC", 22: "GND", 23: "PC0"}
    c.ic("U1", "ATmega328P-PU", 28, "skinny", names, at=(330, 40),
         sides={p: "L" for p in (1, 7, 8, 17, 18, 19, 20, 22, 23)} | {p: "R" for p in (2, 3, 4, 5, 6, 11, 12)})
    for p in (7, 20): c.chain(("U1", p), ["+5V"], 1)
    for p in (8, 22): c.chain(("U1", p), ["GND"], 1)
    c.chain(("NET", "+5V"), ["C:C1:100nF", "GND"], 1)
    c.chain(("U1", 1), ["NET:RESET"], 1)
    c.chain(("NET", "RESET"), ["R:R1:10k", "+5V"], 1)
    c.chain(("J1", 4), ["NET:RESET"], 1)
    for jp, up, nm in ((1, 18, "MISO"), (2, 19, "SCK"), (3, 17, "MOSI")):
        c.chain(("J1", jp), [f"NET:{nm}"], 1); c.chain(("U1", up), [f"NET:{nm}"], 1)
    c.chain(("J1", 5), ["GND"], 1)
    leds = [(2, "D1", "R2", 1), (3, "D2", "R3", 3), (4, "D3", "R4", 3), (5, "D4", "R5", 3), (6, "D5", "R6", 3),
            (11, "D6", "R7", 3), (12, "D7", "R8", 3)]
    for pin, d, r, bld in leds:
        c.chain(("U1", pin), [f"R:{r}:680R", f"LED:{d}:red", "GND"], bld)
    c.chain(("U1", 23), ["SW:SW1:ROLL", "GND"], 2)

    b = Board(c)
    b.ic("U1", 8, 1)
    b.wire("TP2", "BP2", 1, "+5V"); b.wire("TN1", "BN1", 1, "GND")
    b.wire("14j", "BP14", 1, "+5V"); b.wire("15j", "BN15", 1, "GND"); b.two("C1", "14i", "15i", 1)
    b.wire("16b", "TP16", 1, "+5V"); b.wire("14b", "TN14", 1, "GND")
    b.two("R1", "8i", "BP8", 1)
    b.lead("J1", 4, "8j", 1, "RESET"); b.lead("J1", 1, "18c", 1, "MISO"); b.lead("J1", 2, "17c", 1, "SCK")
    b.lead("J1", 3, "19c", 1, "MOSI"); b.lead("J1", 5, "TN6", 1, "GND")
    pinhole = {2: "9h", 3: "10h", 4: "11h", 5: "12h", 6: "13h", 11: "18h", 12: "19h"}
    for i, (pin, d, r, bld) in enumerate(leds):
        uc = 25 + i
        b.wire(pinhole[pin], f"{uc}a", bld, f"PD{i}")
        b.two(r, f"{uc}d", f"{uc}g", bld)
        b.two(d, f"{uc}h", f"BN{uc}", bld)
    b.switch("SW1", 3, 2); b.wire("3a", "TN3", 2, "GND"); b.wire("5g", "13b", 2, "PC0")
    return c, b

# ---------------------------------------------------------------------------------
# helpers shared by months 3-5
# ---------------------------------------------------------------------------------
def _unit(b, src_hole, uc, r, d, build, label):
    """An LED unit: wire from a chip pin to (uc,a); resistor across the centre channel; LED to the bottom GND rail."""
    b.wire(src_hole, f"{uc}a", build, label)
    b.two(r, f"{uc}d", f"{uc}g", build)
    b.two(d, f"{uc}h", f"BN{uc}", build)

def _picks(c, conn_at=(20, 60)):
    c.ic("J1", "PICkit 3 ICSP", 5, "skinny", {1: "MCLR", 2: "VDD", 3: "VSS", 4: "PGD", 5: "PGC"}, at=conn_at,
         sides={1: "R", 2: "R", 3: "R", 4: "R", 5: "R"}, connector=True)

def _rail_bridges(b, build, left=True, right=True):
    if left:
        b.wire("TP2", "BP2", build, "+5V"); b.wire("TN1", "BN1", build, "GND")
    if right:
        for r in ("TP", "BP", "TN", "BN"):
            b.wire(f"{r}31", f"{r}32", build, "+5V" if r in ("TP", "BP") else "GND")

# ---------------------------------------------------------------------------------
# MONTH 3 - analogue in, analogue out (PIC18F47K42 + MCP3008 + MCP4822, SPI by hand)
# ---------------------------------------------------------------------------------
M3_BUILDS = {1: "Build 1 - Read a knob (ADC bar graph)", 2: "Build 2 - Add the DAC", 3: "Build 3 - Loop the DAC back into the ADC"}

def month3():
    c = Circuit("Month 3")
    _picks(c)
    n1 = {1: "MCLR", 11: "VDD", 12: "VSS", 15: "RC0 (SCK)", 16: "RC1 (MOSI)", 17: "RC2 (MISO)", 18: "RC3 (CS ADC)",
          19: "RD0", 20: "RD1", 21: "RD2", 22: "RD3", 23: "RC4 (CS DAC)", 27: "RD4", 28: "RD5", 29: "RD6", 30: "RD7",
          31: "VSS", 32: "VDD", 33: "RB0 (heartbeat)", 39: "RB6/PGC", 40: "RB7/PGD"}
    c.ic("U1", "PIC18F47K42-I/P", 40, "wide", n1, at=(330, 40),
         sides={p: "L" for p in (1, 11, 12, 15, 16, 17, 18, 23, 31, 32, 39, 40)} | {p: "R" for p in (19, 20, 21, 22, 27, 28, 29, 30, 33)})
    n2 = {1: "CH0", 2: "CH1", 7: "CH6", 8: "CH7", 9: "DGND", 10: "CS", 11: "DIN", 12: "DOUT", 13: "CLK", 14: "AGND", 15: "VREF", 16: "VDD"}
    c.ic("U2", "MCP3008-I/P", 16, "skinny", n2, at=(330, 700),
         sides={p: "L" for p in (9, 10, 11, 12, 13, 14, 15, 16)} | {p: "R" for p in (1, 2, 7, 8)})
    n3 = {1: "VDD", 2: "CS", 3: "SCK", 4: "SDI", 5: "LDAC", 6: "VOUTB", 7: "VSS", 8: "VOUTA"}
    c.ic("U3", "MCP4822-E/P", 8, "skinny", n3, at=(330, 1180),
         sides={p: "L" for p in (1, 2, 3, 4, 5, 7)} | {p: "R" for p in (6, 8)})
    # ---- build 1: knob -> ADC -> 8-LED bar graph
    for p in (11, 32): c.chain(("U1", p), ["+5V"], 1)
    for p in (12, 31): c.chain(("U1", p), ["GND"], 1)
    c.chain(("U1", 1), ["NET:MCLR"], 1); c.chain(("NET", "MCLR"), ["R:R1:10k", "+5V"], 1)
    c.chain(("NET", "+5V"), ["C:C1:100nF", "GND"], 1); c.chain(("NET", "+5V"), ["C:C2:100nF", "GND"], 1)
    c.chain(("U1", 40), ["NET:PGD"], 1); c.chain(("U1", 39), ["NET:PGC"], 1)
    c.chain(("J1", 1), ["NET:MCLR"], 1); c.chain(("J1", 2), ["+5V"], 1); c.chain(("J1", 3), ["GND"], 1)
    c.chain(("J1", 4), ["NET:PGD"], 1); c.chain(("J1", 5), ["NET:PGC"], 1)
    c.chain(("U1", 33), ["R:R2:680R", "LED:D1:red", "GND"], 1)
    for i, p in enumerate((19, 20, 21, 22, 27, 28, 29, 30)):
        c.chain(("U1", p), [f"R:R{3+i}:680R", f"LED:D{2+i}:red", "GND"], 1)
    c.chain(("U1", 15), ["NET:SCK"], 1); c.chain(("U1", 16), ["NET:MOSI"], 1)
    c.chain(("U1", 17), ["NET:MISO"], 1); c.chain(("U1", 18), ["NET:CS_ADC"], 1)
    for p in (15, 16): c.chain(("U2", p), ["+5V"], 1)
    for p in (9, 14): c.chain(("U2", p), ["GND"], 1)
    c.chain(("NET", "+5V"), ["C:C3:100nF", "GND"], 1)
    c.chain(("U2", 13), ["NET:SCK"], 1); c.chain(("U2", 11), ["NET:MOSI"], 1)
    c.chain(("U2", 12), ["NET:MISO"], 1); c.chain(("U2", 10), ["NET:CS_ADC"], 1)
    c.chain(("U2", 7), ["+5V"], 1); c.chain(("U2", 8), ["GND"], 1)          # CH6 to 5 V, CH7 to GND: known values for the self-test
    c.chain(("NET", "+5V"), ["POT:RV1:10k", "GND"], 1); c.chain(("NET", "AIN0"), ["WIPER:RV1"], 1)
    c.chain(("U2", 1), ["NET:AIN0"], 1)
    # ---- build 2: the DAC
    c.chain(("U1", 23), ["NET:CS_DAC"], 2)
    c.chain(("U3", 1), ["+5V"], 2); c.chain(("U3", 7), ["GND"], 2); c.chain(("U3", 5), ["GND"], 2)
    c.chain(("NET", "+5V"), ["C:C4:100nF", "GND"], 2)
    c.chain(("U3", 2), ["NET:CS_DAC"], 2); c.chain(("U3", 3), ["NET:SCK"], 2); c.chain(("U3", 4), ["NET:MOSI"], 2)
    c.chain(("U3", 6), ["R:R11:1k", "LED:D10:red", "GND"], 2)
    c.chain(("U3", 8), ["NET:DACA"], 2)
    # ---- build 3: loop DAC A into ADC channel 1
    c.chain(("U2", 2), ["NET:DACA"], 3)

    b = Board(c)
    b.ic("U1", 3, 1); b.ic("U2", 26, 1); b.ic("U3", 36, 2)
    _rail_bridges(b, 1)
    b.wire("13j", "BP13", 1, "+5V"); b.wire("14j", "BN14", 1, "GND"); b.two("C1", "13i", "14i", 1)
    b.wire("11a", "TP11", 1, "+5V"); b.wire("12a", "TN12", 1, "GND"); b.two("C2", "11b", "12b", 1)
    b.two("R1", "3i", "BP3", 1); b.lead("J1", 1, "3j", 1, "MCLR")
    b.lead("J1", 2, "TP6", 1, "VDD"); b.lead("J1", 3, "TN6", 1, "VSS"); b.lead("J1", 4, "3c", 1, "PGD"); b.lead("J1", 5, "4c", 1, "PGC")
    _unit(b, "10b", 51, "R2", "D1", 1, "RB0")
    for i, ph in enumerate(("21i", "22i", "22b", "21b", "16b", "15b", "14b", "13b")):
        _unit(b, ph, 42 + i, f"R{3+i}", f"D{2+i}", 1, f"RD{i}")
    # SPI wires (build 1: to the ADC)
    b.wire("17i", "29c", 1, "SCK"); b.wire("18i", "31c", 1, "MOSI"); b.wire("30b", "19i", 1, "MISO"); b.wire("32b", "20i", 1, "CS")
    b.wire("26b", "TP26", 1, "+5V"); b.wire("27b", "TP27", 1, "+5V"); b.wire("28b", "TN28", 1, "GND"); b.wire("33b", "TN33", 1, "GND")
    b.two("C3", "26c", "28c", 1)
    b.wire("32g", "BP32", 1, "+5V"); b.wire("33g", "BN33", 1, "GND")
    b.pot("RV1", "55c", "56c", "57c", 1); b.wire("55a", "TP55", 1, "+5V"); b.wire("57a", "TN57", 1, "GND"); b.wire("56b", "26h", 1, "AIN0")
    # build 2: the DAC
    b.wire("36h", "BP36", 2, "+5V"); b.two("C4", "36i", "BN36", 2); b.wire("37b", "TN37", 2, "GND"); b.wire("39b", "TN39", 2, "GND")
    b.wire("37h", "20c", 2, "CS DAC"); b.wire("38i", "29d", 2, "SCK"); b.wire("39g", "31d", 2, "MOSI")
    _unit(b, "38b", 53, "R11", "D10", 2, "VOUTB")
    # build 3: loopback
    b.wire("36b", "27h", 3, "DAC A")
    return c, b

# ---------------------------------------------------------------------------------
# MONTH 4 - a clock that keeps time (PIC16F18446 + MCP7940N)
# ---------------------------------------------------------------------------------
M4_BUILDS = {1: "Build 1 - Blink on a new chip", 2: "Build 2 - Meet the real-time clock", 3: "Build 3 - The binary clock"}

def month4():
    c = Circuit("Month 4")
    _picks(c)
    n1 = {1: "VDD", 4: "RA3 (MCLR)", 20: "VSS", 19: "RA0 (PGD)", 18: "RA1 (PGC)", 17: "RA2 (button)", 16: "RC0", 15: "RC1",
          14: "RC2", 7: "RC3", 6: "RC4", 5: "RC5", 8: "RC6", 9: "RC7", 13: "RB4 (SDA)", 11: "RB6 (SCL)"}
    c.ic("U1", "PIC16F18446-I/P", 20, "skinny", n1, at=(330, 40),
         sides={p: "L" for p in (1, 4, 11, 13, 17, 18, 19, 20)} | {p: "R" for p in (16, 15, 14, 7, 6, 5, 8, 9)})
    n2 = {1: "X1", 2: "X2", 3: "VBAT", 4: "VSS", 5: "SDA", 6: "SCL", 7: "MFP", 8: "VCC"}
    c.ic("U2", "MCP7940N-I/P", 8, "skinny", n2, at=(330, 640), sides={p: "L" for p in (1, 2, 3, 4, 5, 6, 8)})
    # ---- build 1
    c.chain(("U1", 1), ["+5V"], 1); c.chain(("U1", 20), ["GND"], 1)
    c.chain(("NET", "+5V"), ["C:C1:100nF", "GND"], 1)
    c.chain(("U1", 4), ["NET:MCLR"], 1); c.chain(("NET", "MCLR"), ["R:R1:10k", "+5V"], 1)
    c.chain(("U1", 19), ["NET:PGD"], 1); c.chain(("U1", 18), ["NET:PGC"], 1)
    c.chain(("J1", 1), ["NET:MCLR"], 1); c.chain(("J1", 2), ["+5V"], 1); c.chain(("J1", 3), ["GND"], 1)
    c.chain(("J1", 4), ["NET:PGD"], 1); c.chain(("J1", 5), ["NET:PGC"], 1)
    c.chain(("U1", 16), ["R:R2:680R", "LED:D1:red", "GND"], 1)
    # ---- build 2: the clock chip and LEDs RC1..RC5
    c.chain(("U2", 8), ["+5V"], 2); c.chain(("U2", 4), ["GND"], 2); c.chain(("U2", 3), ["GND"], 2)
    c.chain(("NET", "+5V"), ["C:C2:100nF", "GND"], 2)
    c.chain(("U2", 1), ["NET:X1"], 2); c.chain(("U2", 2), ["NET:X2"], 2)
    c.chain(("NET", "X1"), ["XTAL:Y1:32.768kHz", "NET:X2"], 2)
    c.chain(("NET", "X1"), ["C:C3:10pF", "GND"], 2); c.chain(("NET", "X2"), ["C:C4:10pF", "GND"], 2)
    c.chain(("U2", 6), ["NET:SCL"], 2); c.chain(("U2", 5), ["NET:SDA"], 2)
    c.chain(("NET", "SCL"), ["R:R3:4k7", "+5V"], 2); c.chain(("NET", "SDA"), ["R:R4:4k7", "+5V"], 2)
    c.chain(("U1", 11), ["NET:SCL"], 2); c.chain(("U1", 13), ["NET:SDA"], 2)
    for i, p in enumerate((15, 14, 7, 6, 5)):
        c.chain(("U1", p), [f"R:R{5+i}:680R", f"LED:D{2+i}:red", "GND"], 2)
    # ---- build 3: mode LEDs and the button
    c.chain(("U1", 8), ["R:R10:680R", "LED:D7:red", "GND"], 3)
    c.chain(("U1", 9), ["R:R11:680R", "LED:D8:red", "GND"], 3)
    c.chain(("U1", 17), ["SW:SW1:MODE", "GND"], 3)

    b = Board(c)
    b.ic("U1", 8, 1); b.ic("U2", 22, 2)
    _rail_bridges(b, 1, right=False); _rail_bridges(b, 2, left=False)
    b.wire("8j", "BP8", 1, "+5V"); b.wire("8a", "TN8", 1, "GND"); b.two("C1", "8g", "8d", 1)
    b.two("R1", "11i", "BP11", 1); b.lead("J1", 1, "11j", 1, "MCLR")
    b.lead("J1", 2, "TP5", 1, "VDD"); b.lead("J1", 3, "TN5", 1, "VSS"); b.lead("J1", 4, "9b", 1, "PGD"); b.lead("J1", 5, "10b", 1, "PGC")
    _unit(b, "12b", 28, "R2", "D1", 1, "RC0")
    # build 2
    b.wire("22b", "TP22", 2, "+5V"); b.wire("25h", "BN25", 2, "GND"); b.wire("24h", "BN24", 2, "GND"); b.two("C2", "22c", "TN22", 2)
    b.two("Y1", "22h", "23h", 2); b.two("C3", "22i", "BN22", 2); b.two("C4", "23i", "BN23", 2)
    b.wire("17b", "24b", 2, "SCL"); b.wire("15c", "25c", 2, "SDA"); b.two("R3", "24d", "TP24", 2); b.two("R4", "25d", "TP25", 2)
    for i, (ph, r, d) in enumerate((("13b", "R5", "D2"), ("14b", "R6", "D3"), ("14h", "R7", "D4"), ("13h", "R8", "D5"), ("12h", "R9", "D6"))):
        _unit(b, ph, 29 + i, r, d, 2, f"RC{i+1}")
    # build 3
    _unit(b, "15h", 34, "R10", "D7", 3, "RC6"); _unit(b, "16h", 35, "R11", "D8", 3, "RC7")
    b.switch("SW1", 3, 3); b.wire("3a", "TN3", 3, "GND"); b.wire("5g", "11b", 3, "RA2")
    return c, b

# ---------------------------------------------------------------------------------
# MONTH 5 - a 16-bit chip at 3.3 V (PIC24FJ64GA002 + 24LC512)
# ---------------------------------------------------------------------------------
M5_BUILDS = {1: "Build 1 - Blink at 3.3 V", 2: "Build 2 - Say hello to the EEPROM", 3: "Build 3 - Memory that survives power-off"}

def month5():
    c = Circuit("Month 5"); c.supply_label = "+3.3 V"
    _picks(c)
    n1 = {1: "MCLR", 2: "RA0 (heartbeat)", 3: "RA1 (button)", 4: "RB0 (PGED1)", 5: "RB1 (PGEC1)", 6: "RB2", 7: "RB3", 8: "VSS",
          13: "VDD", 17: "RB8 (SCL)", 18: "RB9 (SDA)", 19: "VSS", 20: "VCAP", 21: "RB10", 22: "RB11", 23: "RB12", 24: "RB13",
          25: "RB14", 26: "RB15", 27: "AVSS", 28: "AVDD"}
    c.ic("U1", "PIC24FJ64GA002-I/SP", 28, "skinny", n1, at=(330, 40),
         sides={p: "L" for p in (1, 3, 4, 5, 8, 13, 17, 18, 19, 20, 27, 28)} | {p: "R" for p in (2, 6, 7, 21, 22, 23, 24, 25, 26)})
    n2 = {1: "A0", 2: "A1", 3: "A2", 4: "VSS", 5: "SDA", 6: "SCL", 7: "WP", 8: "VCC"}
    c.ic("U2", "24LC512-I/P", 8, "skinny", n2, at=(330, 760), sides={p: "L" for p in (1, 2, 3, 4, 5, 6, 7, 8)})
    # ---- build 1
    for p in (13, 28): c.chain(("U1", p), ["+5V"], 1)
    for p in (8, 19, 27): c.chain(("U1", p), ["GND"], 1)
    c.chain(("U1", 20), ["C:C2:10uF", "GND"], 1)
    c.chain(("NET", "+5V"), ["C:C1:100nF", "GND"], 1)
    c.chain(("U1", 1), ["NET:MCLR"], 1); c.chain(("NET", "MCLR"), ["R:R1:10k", "+5V"], 1)
    c.chain(("U1", 4), ["NET:PGD"], 1); c.chain(("U1", 5), ["NET:PGC"], 1)
    c.chain(("J1", 1), ["NET:MCLR"], 1); c.chain(("J1", 2), ["+5V"], 1); c.chain(("J1", 3), ["GND"], 1)
    c.chain(("J1", 4), ["NET:PGD"], 1); c.chain(("J1", 5), ["NET:PGC"], 1)
    c.chain(("U1", 2), ["R:R2:330R", "LED:D1:red", "GND"], 1)
    # ---- build 2: EEPROM + 8 LEDs
    for p in (1, 2, 3, 4, 7): c.chain(("U2", p), ["GND"], 2)
    c.chain(("U2", 8), ["+5V"], 2); c.chain(("NET", "+5V"), ["C:C3:100nF", "GND"], 2)
    c.chain(("U2", 5), ["NET:SDA"], 2); c.chain(("U2", 6), ["NET:SCL"], 2)
    c.chain(("NET", "SCL"), ["R:R3:4k7", "+5V"], 2); c.chain(("NET", "SDA"), ["R:R4:4k7", "+5V"], 2)
    c.chain(("U1", 17), ["NET:SCL"], 2); c.chain(("U1", 18), ["NET:SDA"], 2)
    for i, p in enumerate((6, 7, 21, 22, 23, 24, 25, 26)):
        c.chain(("U1", p), [f"R:R{5+i}:330R", f"LED:D{2+i}:red", "GND"], 2)
    # ---- build 3: button
    c.chain(("U1", 3), ["NET:BTN"], 3); c.chain(("NET", "BTN"), ["R:R13:10k", "+5V"], 3); c.chain(("NET", "BTN"), ["SW:SW1:ADD", "GND"], 3)

    b = Board(c)
    b.ic("U1", 8, 1); b.ic("U2", 41, 2)
    _rail_bridges(b, 1)
    b.wire("20j", "BP20", 1, "+5V"); b.two("C1", "20i", "BN20", 1); b.wire("15j", "BN15", 1, "GND")
    b.wire("17b", "TN17", 1, "GND"); b.two("C2", "16b", "TN16", 1)
    b.wire("8b", "TP8", 1, "+5V"); b.wire("9b", "TN9", 1, "GND")
    b.two("R1", "8i", "BP8", 1); b.lead("J1", 1, "8j", 1, "MCLR")
    b.lead("J1", 2, "TP5", 1, "VDD"); b.lead("J1", 3, "TN5", 1, "VSS"); b.lead("J1", 4, "11j", 1, "PGD"); b.lead("J1", 5, "12j", 1, "PGC")
    _unit(b, "9h", 39, "R2", "D1", 1, "RA0")
    # build 2
    for i, ph in enumerate(("13h", "14h", "15b", "14b", "13b", "12b", "11b", "10b")):
        _unit(b, ph, 30 + i, f"R{5+i}", f"D{2+i}", 2, f"LED{i}")
    for col in (41, 42, 43): b.wire(f"{col}h", f"BN{col}", 2, "GND")
    b.wire("44h", "BN44", 2, "GND"); b.wire("42b", "TN42", 2, "GND"); b.wire("41b", "TP41", 2, "+5V"); b.two("C3", "41c", "TN41", 2)
    b.wire("19b", "43b", 2, "SCL"); b.wire("18c", "44c", 2, "SDA"); b.two("R3", "43c", "TP43", 2); b.two("R4", "44d", "TP44", 2)
    # build 3
    b.switch("SW1", 3, 3); b.wire("3a", "TN3", 3, "GND"); b.wire("5g", "10h", 3, "RA1"); b.two("R13", "10i", "BP10", 3)
    return c, b

# ---------------------------------------------------------------------------------
# MONTH 2 - PIC18F47K42 + MCP23017 workshop command centre
# ---------------------------------------------------------------------------------
M2_BUILDS = {1: "Build 1 - Blink (minimum circuit)", 2: "Build 2 - Say hello to the MCP23017",
             3: "Build 3 - Eight LEDs and a button", 4: "Build 4 - Workshop Command Centre"}

def month2():
    c = Circuit("Month 2")
    c.ic("J1", "PICkit 3 ICSP", 5, "skinny", {1: "MCLR", 2: "VDD", 3: "VSS", 4: "PGD", 5: "PGC"}, at=(20, 60),
         sides={1: "R", 2: "R", 3: "R", 4: "R", 5: "R"}, connector=True)
    c.ic("U1", "PIC18F47K42-I/P", 40, "wide",
         {1: "MCLR", 11: "VDD", 12: "VSS", 18: "RC3 (SCL)", 19: "RD0 (LED)", 22: "RD3 (piezo)", 23: "RC4 (SDA)",
          31: "VSS", 32: "VDD", 39: "RB6/PGC", 40: "RB7/PGD"}, at=(330, 40),
         sides={1: "L", 11: "L", 12: "L", 31: "L", 32: "L", 39: "L", 40: "L", 18: "R", 19: "R", 22: "R", 23: "R"})
    gpa = {21: "GPA0", 22: "GPA1", 23: "GPA2", 24: "GPA3", 25: "GPA4", 26: "GPA5", 27: "GPA6", 28: "GPA7"}
    pins2 = {1: "GPB0", 2: "GPB1", 9: "VDD", 10: "VSS", 12: "SCL", 13: "SDA", 15: "A0", 16: "A1", 17: "A2", 18: "RESET"}
    pins2.update(gpa)
    sides2 = {p: "L" for p in (1, 2, 9, 10, 12, 13, 15, 16, 17, 18)}
    sides2.update({p: "R" for p in gpa})
    c.ic("U2", "MCP23017-E/SP", 28, "skinny", pins2, at=(330, 400), sides=sides2)
    # ---- build 1
    for p in (11, 32): c.chain(("U1", p), ["+5V"], 1)
    for p in (12, 31): c.chain(("U1", p), ["GND"], 1)
    c.chain(("U1", 1), ["NET:MCLR"], 1)
    c.chain(("NET", "MCLR"), ["R:R1:10k", "+5V"], 1)
    c.chain(("NET", "+5V"), ["C:C1:100nF", "GND"], 1)
    c.chain(("NET", "+5V"), ["C:C2:100nF", "GND"], 1)
    c.chain(("U1", 40), ["NET:PGD"], 1); c.chain(("U1", 39), ["NET:PGC"], 1)
    c.chain(("J1", 1), ["NET:MCLR"], 1); c.chain(("J1", 2), ["+5V"], 1); c.chain(("J1", 3), ["GND"], 1)
    c.chain(("J1", 4), ["NET:PGD"], 1); c.chain(("J1", 5), ["NET:PGC"], 1)
    c.chain(("U1", 19), ["R:R2:680R", "LED:D1:red", "GND"], 1)
    # ---- build 2
    c.chain(("U1", 18), ["NET:SCL"], 2); c.chain(("U1", 23), ["NET:SDA"], 2)
    c.chain(("NET", "SCL"), ["R:R3:4k7", "+5V"], 2); c.chain(("NET", "SDA"), ["R:R4:4k7", "+5V"], 2)
    c.chain(("U2", 12), ["NET:SCL"], 2); c.chain(("U2", 13), ["NET:SDA"], 2)
    c.chain(("U2", 9), ["+5V"], 2); c.chain(("U2", 10), ["GND"], 2)
    c.chain(("NET", "+5V"), ["C:C3:100nF", "GND"], 2)
    for p in (15, 16, 17): c.chain(("U2", p), ["GND"], 2)
    c.chain(("U2", 18), ["R:R5:10k", "+5V"], 2)
    # GPA LEDs: GPA0 in build 2, the rest in build 3
    for i, p in enumerate(range(21, 29)):
        c.chain(("U2", p), [f"R:R{6+i}:680R", f"LED:D{2+i}:red", "GND"], 2 if i == 0 else 3)
    # ---- build 3 / 4
    c.chain(("U2", 1), ["SW:SW1:MODE", "GND"], 3)
    c.chain(("U2", 2), ["SW:SW2:SPEED", "GND"], 4)
    c.chain(("U1", 22), ["R:R14:100R", "PIEZO:BZ1", "GND"], 4)

    b = Board(c)
    b.ic("U1", 3, 1)                     # 40-pin: pins 1-20 bottom, 40-21 top
    b.ic("U2", 30, 2)                    # 28-pin MCP23017
    # rails (bridging)
    b.wire("TP2", "BP2", 1, "+5V"); b.wire("TN1", "BN1", 1, "GND")
    b.wire("TP31", "TP32", 1, "+5V"); b.wire("BP31", "BP32", 1, "+5V")
    b.wire("TN31", "TN32", 1, "GND"); b.wire("BN31", "BN32", 1, "GND")
    # U1 power
    b.wire("13j", "BP13", 1, "+5V"); b.wire("14j", "BN14", 1, "GND"); b.two("C1", "13i", "14i", 1)
    b.wire("11a", "TP11", 1, "+5V"); b.wire("12a", "TN12", 1, "GND"); b.two("C2", "11b", "12b", 1)
    # reset + programmer
    b.two("R1", "3i", "BP3", 1); b.lead("J1", 1, "3j", 1, "MCLR")
    b.lead("J1", 2, "TP6", 1, "VDD"); b.lead("J1", 3, "TN6", 1, "VSS")
    b.lead("J1", 4, "3c", 1, "PGD"); b.lead("J1", 5, "4c", 1, "PGC")
    # heartbeat LED unit at column 53
    b.wire("21i", "53a", 1, "RD0"); b.two("R2", "53d", "53g", 1); b.two("D1", "53h", "BN53", 1)
    # ---- build 2: MCP23017 (c0=30: pin1 col30 ... pin14 col43; top: pin28 col30 ... pin15 col43)
    b.wire("38h", "BP38", 2, "+5V"); b.wire("39h", "BN39", 2, "GND"); b.two("C3", "38g", "39g", 2)
    b.wire("20i", "41g", 2, "SCL"); b.wire("20c", "42g", 2, "SDA")
    b.two("R3", "41i", "BP41", 2); b.two("R4", "42i", "BP42", 2)
    for col in (41, 42, 43): b.wire(f"{col}b", f"TN{col}", 2, "GND")      # A2, A1, A0
    b.two("R5", "40d", "TP40", 2)                                          # RESET pull-up
    # GPA0..7 = pins 21..28 -> top strips cols 37,36,...,30 ; LED units at cols 44..51
    for i in range(8):
        pincol = 37 - i; uc = 44 + i; bld = 2 if i == 0 else 3
        b.wire(f"{pincol}b", f"{uc}a", bld, f"GPA{i}")
        b.two(f"R{6+i}", f"{uc}d", f"{uc}g", bld)
        b.two(f"D{2+i}", f"{uc}h", f"BN{uc}", bld)
    # ---- build 3: SW1 (MODE) on GPB0; build 4: SW2 (SPEED) on GPB1
    b.switch("SW1", 23, 3); b.wire("23a", "TN23", 3, "GND"); b.wire("25g", "30g", 3, "GPB0")
    b.switch("SW2", 26, 4); b.wire("26a", "TN26", 4, "GND"); b.wire("28h", "31h", 4, "GPB1")
    # ---- build 4: piezo unit at column 55
    b.wire("21c", "55a", 4, "RD3"); b.two("R14", "55d", "55g", 4); b.two("BZ1", "55h", "BN55", 4)
    return c, b

# ---------------------------------------------------------------------------------
# MONTH 1, PART B (optional) - ATmega328P as an AVR programmer
# ---------------------------------------------------------------------------------
ISP_BUILDS = {1: "Build B1 - The minimum ATmega328P board", 2: "Build B2 - Turn it into a programmer",
              3: "Build B3 - Program a second chip"}

def month1_isp():
    c = Circuit("Month 1 Part B")
    c.ic("J2", "USB-serial adapter", 4, "skinny", {1: "GND", 2: "TXD (to chip RXD)", 3: "RXD (from chip TXD)", 4: "DTR"},
         at=(20, 40), sides={1: "R", 2: "R", 3: "R", 4: "R"}, connector=True, named_only=True)
    c.ic("J3", "USBasp ISP", 6, "skinny", {1: "MISO", 3: "SCK", 4: "MOSI", 5: "RESET", 6: "GND"},
         at=(20, 330), sides={1: "R", 3: "R", 4: "R", 5: "R", 6: "R"}, connector=True)
    names = {1: "RESET", 2: "RXD (PD0)", 3: "TXD (PD1)", 7: "VCC", 8: "GND", 9: "XTAL1", 10: "XTAL2", 13: "D7 (PD7)",
             14: "D8 (PB0)", 15: "D9 (PB1)", 16: "D10 (PB2)", 17: "MOSI (PB3)", 18: "MISO (PB4)", 19: "SCK (PB5)",
             20: "AVCC", 21: "AREF", 22: "GND"}
    c.ic("U1", "ATmega328P-PU (programmer)", 28, "skinny", names, at=(470, 40),
         sides={p: "L" for p in (1, 2, 3, 7, 8, 9, 10, 20, 21, 22)} | {p: "R" for p in (13, 14, 15, 16, 17, 18, 19)})
    n2 = {1: "RESET", 7: "VCC", 8: "GND", 9: "XTAL1", 10: "XTAL2", 15: "D9 (PB1)", 17: "MOSI (PB3)", 18: "MISO (PB4)",
          19: "SCK (PB5)", 20: "AVCC", 22: "GND"}
    c.ic("U2", "ATmega328P-PU (target)", 28, "skinny", n2, at=(470, 640),
         sides={p: "L" for p in (1, 7, 8, 9, 10, 20, 22)} | {p: "R" for p in (15, 17, 18, 19)})
    # ---- build 1: the minimum board
    for p in (7, 20): c.chain(("U1", p), ["+5V"], 1)
    for p in (8, 22): c.chain(("U1", p), ["GND"], 1)
    c.chain(("U1", 21), ["C:C5:100nF", "GND"], 1)
    c.chain(("NET", "+5V"), ["C:C1:100nF", "GND"], 1)
    c.chain(("U1", 1), ["NET:RESET"], 1)
    c.chain(("NET", "RESET"), ["R:R1:10k", "+5V"], 1)
    c.chain(("U1", 9), ["NET:XTAL1"], 1); c.chain(("U1", 10), ["NET:XTAL2"], 1)
    c.chain(("NET", "XTAL1"), ["XTAL:Y1:16MHz", "NET:XTAL2"], 1)
    c.chain(("NET", "XTAL1"), ["C:C2:22pF", "GND"], 1)
    c.chain(("NET", "XTAL2"), ["C:C3:22pF", "GND"], 1)
    c.chain(("U1", 15), ["R:R2:680R", "LED:D1:red", "GND"], 1)
    c.chain(("J2", 1), ["GND"], 1)
    c.chain(("J2", 2), ["NET:TO_RXD"], 1); c.chain(("U1", 2), ["NET:TO_RXD"], 1)
    c.chain(("J2", 3), ["NET:FROM_TXD"], 1); c.chain(("U1", 3), ["NET:FROM_TXD"], 1)
    c.chain(("J2", 4), ["C:C4:100nF", "NET:RESET"], 1)
    # USBasp leads: only while burning the bootloader in build 1
    for p, nm in ((1, "MISO"), (3, "SCK"), (4, "MOSI")):
        c.chain(("J3", p), [f"NET:{nm}"], 1, until=1)
    c.chain(("J3", 5), ["NET:RESET"], 1, until=1); c.chain(("J3", 6), ["GND"], 1, until=1)
    c.chain(("U1", 17), ["NET:MOSI"], 1); c.chain(("U1", 18), ["NET:MISO"], 1); c.chain(("U1", 19), ["NET:SCK"], 1)
    # ---- build 2: programmer indicator LEDs
    c.chain(("U1", 14), ["R:R5:680R", "LED:D2:red", "GND"], 2)
    c.chain(("U1", 13), ["R:R6:680R", "LED:D3:red", "GND"], 2)
    # ---- build 3: the target chip
    c.chain(("U1", 16), ["NET:TRESET"], 3)
    for p in (7, 20): c.chain(("U2", p), ["+5V"], 3)
    for p in (8, 22): c.chain(("U2", p), ["GND"], 3)
    c.chain(("NET", "+5V"), ["C:C6:100nF", "GND"], 3)
    c.chain(("U2", 1), ["NET:TRESET"], 3)
    c.chain(("NET", "TRESET"), ["R:R3:10k", "+5V"], 3)
    c.chain(("U2", 9), ["NET:XTAL1B"], 3); c.chain(("U2", 10), ["NET:XTAL2B"], 3)
    c.chain(("NET", "XTAL1B"), ["XTAL:Y2:16MHz", "NET:XTAL2B"], 3)
    c.chain(("NET", "XTAL1B"), ["C:C7:22pF", "GND"], 3)
    c.chain(("NET", "XTAL2B"), ["C:C8:22pF", "GND"], 3)
    c.chain(("U2", 17), ["NET:MOSI"], 3); c.chain(("U2", 18), ["NET:MISO"], 3); c.chain(("U2", 19), ["NET:SCK"], 3)
    c.chain(("U2", 15), ["R:R4:680R", "LED:D4:red", "GND"], 3)

    b = Board(c)
    b.ic("U1", 5, 1)
    b.wire("TP2", "BP2", 1, "+5V"); b.wire("TN1", "BN1", 1, "GND")
    # power
    b.wire("11j", "BP11", 1, "+5V"); b.wire("12j", "BN12", 1, "GND"); b.two("C1", "11i", "12i", 1)
    b.wire("13b", "TP13", 1, "+5V"); b.wire("11b", "TN11", 1, "GND"); b.two("C5", "12a", "TN12", 1)
    # reset, DTR capacitor
    b.two("R1", "5i", "BP5", 1); b.two("C4", "3h", "5h", 1)
    b.lead("J2", 4, "3j", 1, "DTR")
    b.lead("J2", 2, "6h", 1, "TXD")
    b.lead("J2", 3, "7h", 1, "RXD")
    b.lead("J2", 1, "BN8", 1, "GND")
    # crystal
    b.two("Y1", "13h", "14h", 1); b.two("C2", "13i", "BN13", 1); b.two("C3", "14i", "BN14", 1)
    # USBasp leads (removed after build 1)
    b.lead("J3", 1, "15c", 1, "MISO", until=1); b.lead("J3", 3, "14c", 1, "SCK", until=1)
    b.lead("J3", 4, "16c", 1, "MOSI", until=1); b.lead("J3", 5, "5j", 1, "RESET", until=1)
    b.lead("J3", 6, "TN6", 1, "GND", until=1)
    # LED units: D9 heartbeat (cols 22), D8 error (23), D7 programming (24)
    b.wire("18b", "22a", 1, "D9"); b.two("R2", "22d", "22g", 1); b.two("D1", "22h", "BN22", 1)
    b.wire("18h", "23a", 2, "D8"); b.two("R5", "23d", "23g", 2); b.two("D2", "23h", "BN23", 2)
    b.wire("17h", "24a", 2, "D7"); b.two("R6", "24d", "24g", 2); b.two("D3", "24h", "BN24", 2)
    # build 3: the target
    b.ic("U2", 30, 3)
    for r in ("TP", "BP", "TN", "BN"):
        b.wire(f"{r}31", f"{r}32", 3, "+5V" if r in ("TP", "BP") else "GND")
    b.two("R3", "30i", "BP30", 3); b.wire("17c", "30g", 3, "D10 reset")
    b.wire("36j", "BP36", 3, "+5V"); b.wire("37j", "BN37", 3, "GND"); b.two("C6", "36i", "37i", 3)
    b.wire("38b", "TP38", 3, "+5V"); b.wire("36b", "TN36", 3, "GND")
    b.two("Y2", "38h", "39h", 3); b.two("C7", "38i", "BN38", 3); b.two("C8", "39i", "BN39", 3)
    b.wire("16b", "41b", 3, "MOSI"); b.wire("15b", "40b", 3, "MISO"); b.wire("14b", "39b", 3, "SCK")
    b.wire("43b", "46a", 3, "D9"); b.two("R4", "46d", "46g", 3); b.two("D4", "46h", "BN46", 3)
    return c, b

if __name__ == "__main__":
    for name, fn, nb in (("Month 1", month1, 3), ("Month 1 Part B", month1_isp, 3), ("Month 1 ATmega328P", month1_avr, 3), ("Month 2", month2, 4), ("Month 3", month3, 3), ("Month 4", month4, 3), ("Month 5", month5, 3)):
        c, b = fn()
        for n in range(1, nb + 1):
            pr = b.verify(n)
            print(f"{name} build {n}: {'OK - breadboard matches schematic' if not pr else 'PROBLEMS'}")
            for x in pr: print("   -", x)
