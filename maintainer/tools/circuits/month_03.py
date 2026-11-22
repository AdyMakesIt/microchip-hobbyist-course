#!/usr/bin/env python3
"""Circuit definitions for Month 3: schematic chains + breadboard holes."""
from mhc_draw import Circuit, Board
from ._helpers import _picks, _unit, _rail_bridges

# ---------------------------------------------------------------------------------
# MONTH 3 - analogue in, analogue out (PIC18F47K42 + MCP3008 + MCP4822, SPI by hand)
# ---------------------------------------------------------------------------------
MONTH_03_BUILDS = {1: "Build 1 - Read a knob (ADC bar graph)", 2: "Build 2 - Add the DAC", 3: "Build 3 - Loop the DAC back into the ADC"}

def month_03():
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
