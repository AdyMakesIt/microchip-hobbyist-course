#!/usr/bin/env python3
"""Circuit definitions for Month 1 PIC: schematic chains + breadboard holes."""
from mhc_draw import Circuit, Board

# ---------------------------------------------------------------------------------
# MONTH 1 - PIC16F18857 electronic dice
# ---------------------------------------------------------------------------------
PIC1_BUILDS = {1: "PIC Build 1 - Blink an LED", 2: "PIC Build 2 - Add the button", 3: "PIC Build 3 - The dice (seven LEDs)"}

def month1_pic():
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
