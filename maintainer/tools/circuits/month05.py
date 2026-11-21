#!/usr/bin/env python3
"""Circuit definitions for Month 5: schematic chains + breadboard holes."""
from mhc_draw import Circuit, Board
from ._helpers import _picks, _unit, _rail_bridges

# ---------------------------------------------------------------------------------
# MONTH 5 - a 16-bit chip at 3.3 V (PIC24FJ64GA002 + 24LC512)
# ---------------------------------------------------------------------------------
M05_BUILDS = {1: "Build 1 - Blink at 3.3 V", 2: "Build 2 - Say hello to the EEPROM", 3: "Build 3 - Memory that survives power-off"}

def month05():
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
