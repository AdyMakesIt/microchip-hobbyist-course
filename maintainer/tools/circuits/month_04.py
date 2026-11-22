#!/usr/bin/env python3
"""Circuit definitions for Month 4: schematic chains + breadboard holes."""
from mhc_draw import Circuit, Board
from ._helpers import _picks, _unit, _rail_bridges

# ---------------------------------------------------------------------------------
# MONTH 4 - a clock that keeps time (PIC16F18446 + MCP7940N)
# ---------------------------------------------------------------------------------
MONTH_04_BUILDS = {1: "Build 1 - Blink on a new chip", 2: "Build 2 - Meet the real-time clock", 3: "Build 3 - The binary clock"}

def month_04():
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

