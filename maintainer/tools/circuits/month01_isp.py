#!/usr/bin/env python3
"""Circuit definitions for Month 1 ISP: schematic chains + breadboard holes."""
from mhc_draw import Circuit, Board

# ---------------------------------------------------------------------------------
# MONTH 1, PART B (optional) - ATmega328P as an AVR programmer
# ---------------------------------------------------------------------------------
ISP1_BUILDS = {1: "Build B1 - The minimum ATmega328P board", 2: "Build B2 - Turn it into a programmer",
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
