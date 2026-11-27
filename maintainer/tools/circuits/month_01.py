#!/usr/bin/env python3
"""Circuit definitions for Month 1: schematic chains + breadboard holes."""
from mhc_draw import Circuit, Board

# ---------------------------------------------------------------------------------
# MONTH 1, AVR TRACK - ATmega328P electronic dice (programmed through an ISP programmer)
# ---------------------------------------------------------------------------------
MONTH_01_AVR_BUILDS = {1: "AVR Build 1 - Blink an LED", 2: "AVR Build 2 - Add the button", 3: "AVR Build 3 - The dice (seven LEDs)"}

def month_01_avr():
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
    c.chain(("NET", "+5V"), ["C:C2:100nF", "GND"], 1)          # AVCC decoupling (added after bench feedback)
    c.chain(("U1", 1), ["NET:RESET"], 1)
    c.chain(("NET", "RESET"), ["R:R1:10k", "+5V"], 1)
    c.chain(("J1", 4), ["NET:RESET"], 1)
    for jp, up, nm in ((1, 18, "MISO"), (2, 19, "SCK"), (3, 17, "MOSI")):
        c.chain(("J1", jp), [f"NET:{nm}"], 1); c.chain(("U1", up), [f"NET:{nm}"], 1)
    c.chain(("J1", 5), ["GND"], 1)

    # Build 1 blinks D4 (centre LED); Build 3 adds the rest of the dice LEDs.
    leds = [
        (2,  "D1", "R2", 3, "9g",  "PD0"),
        (3,  "D2", "R3", 3, "10g", "PD1"),
        (4,  "D3", "R4", 3, "11g", "PD2"),
        (5,  "D4", "R5", 1, "12g", "PD3"),
        (6,  "D5", "R6", 3, "13g", "PD4"),
        (11, "D6", "R7", 3, "18g", "PD5"),
        (12, "D7", "R8", 3, "19g", "PD6"),
    ]
    for pin, d, r, bld, _src, _net in leds:
        c.chain(("U1", pin), [f"R:{r}:680R", f"LED:{d}:red", "GND"], bld)
    c.chain(("U1", 23), ["SW:SW1:ROLL", "GND"], 2)

    b = Board(c)
    b.ic("U1", 8, 1)
    # MB102 power supply at left end of rails (column 1) - powers all builds
    b.mb102(build=1, col=1, voltage="5 V")
    # power pins - chip power from rails (no rail bridging wires needed; MB102 feeds left end)
    b.wire("14h", "BP14", 1, "+5V"); b.wire("15h", "BN15", 1, "GND"); b.two("C1", "14g", "15g", 1)
    b.wire("16b", "TP16", 1, "+5V"); b.wire("14b", "TN14", 1, "GND"); b.two("C2", "16d", "14d", 1)
    b.two("R1", "8i", "BP8", 1)
    b.lead("J1", 4, "8h", 1, "RESET"); b.lead("J1", 1, "18c", 1, "MISO"); b.lead("J1", 2, "17c", 1, "SCK")
    b.lead("J1", 3, "19c", 1, "MOSI"); b.lead("J1", 5, "TN6", 1, "GND")

    # D1 (Build 3, PD0): cols 25-26 (top)
    b.wire("9g", "25e", 3, "PD0")
    b.two("R2", "25d", "26b", 3)
    b.two("D1", "26a", "TN26", 3)

    # D2 (Build 3, PD1): cols 27-28 (top)
    b.wire("10g", "35e", 3, "PD1")
    b.two("R3", "35d", "34b", 3)
    b.two("D2", "34a", "TN34", 3)

    # D3 (Build 3, PD2): cols 29-30 (top)
    b.wire("11g", "27d", 3, "PD2")
    b.two("R4", "27e", "28f", 3)
    b.two("D3", "28g", "BN28", 3)

    # D4 (Build 1 centre blink LED, PD3): cols 31-32 (top)
    b.wire("12g", "29d", 1, "PD3")
    b.two("R5", "29e", "30f", 1)
    b.two("D4", "30g", "BN30", 1)

    # D5 (Build 3, PD4): cols 33-34 (top)
    b.wire("13g", "31d", 3, "PD4")
    b.two("R6", "31e", "32f", 3)
    b.two("D5", "32g", "BN32", 3)

    # D6 (Build 3, PD5): cols 35-36 (bottom)
    b.wire("18g", "25f", 3, "PD5")
    b.two("R7", "25g", "26i", 3)
    b.two("D6", "26j", "BN26", 3)

    # D7 (Build 3, PD6): cols 37-38 (bottom)
    b.wire("19g", "35f", 3, "PD6")
    b.two("R8", "35g", "34i", 3)
    b.two("D7", "34j", "BN34", 3)

    b.switch("SW1", 22, 2, flip=True); b.wire("22d", "13b", 2, "PC0"); b.wire("24g", "BN24", 2, "GND")
    return c, b

# ---------------------------------------------------------------------------------
# MONTH 1 - PIC Track PIC16F18857 electronic dice
# ---------------------------------------------------------------------------------
MONTH_01_PIC_BUILDS = {1: "PIC Build 1 - Blink an LED", 2: "PIC Build 2 - Add the button", 3: "PIC Build 3 - The dice (seven LEDs)"}

def month_01_pic():
    c = Circuit("Month 1 PIC")
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
    b.mb102(build=1, col=1, voltage="5 V")
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
# MONTH 1, PART B (optional) - ATmega328P as an AVR programmer
# ---------------------------------------------------------------------------------
MONTH_01_ISP_BUILDS = {1: "Build B1 - The minimum ATmega328P board", 2: "Build B2 - Turn it into a programmer",
              3: "Build B3 - Program a second chip"}

def month_01_isp():
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
    b.mb102(build=1, col=1, voltage="5 V")
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
