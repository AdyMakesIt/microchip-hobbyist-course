#!/usr/bin/env python3
"""Circuit definitions for Month 2: schematic chains + breadboard holes."""
from mhc_draw import Circuit, Board

# ---------------------------------------------------------------------------------
# MONTH 2 - PIC18F47K42 + MCP23017 workshop command centre
# ---------------------------------------------------------------------------------
M02_BUILDS = {1: "Build 1 - Blink (minimum circuit)", 2: "Build 2 - Say hello to the MCP23017",
             3: "Build 3 - Eight LEDs and a button", 4: "Build 4 - Workshop Command Centre"}

def month02():
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
