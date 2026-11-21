#!/usr/bin/env python3
"""Circuit definitions for Month 1 AVR: schematic chains + breadboard holes."""
from mhc_draw import Circuit, Board

# ---------------------------------------------------------------------------------
# MONTH 1, AVR TRACK - ATmega328P electronic dice (programmed through an ISP programmer)
# ---------------------------------------------------------------------------------
AVR1_BUILDS = {1: "AVR Build 1 - Blink an LED", 2: "AVR Build 2 - Add the button", 3: "AVR Build 3 - The dice (seven LEDs)"}

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
    b.wire("TP63", "BP63", 1, "+5V"); b.wire("TN62", "BN62", 1, "GND")
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
