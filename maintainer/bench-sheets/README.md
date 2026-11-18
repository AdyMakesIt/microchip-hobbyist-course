# Bench validation kit

Printable sheets for testing the course on real hardware. Each sheet is **generated from the build pages**, so it always matches them. Run `python3 maintainer/tools/make_bench_sheets.py` after any change to a page.

## Suggested order

1. **Month 1, AVR track:** the simplest, and it proves your PlatformIO and programmer set-up (the `0x1e950f` signature test comes first).
2. **Month 1, PIC track:** proves MPLAB X, XC8, the PICkit 3 and the `#pragma config` block.
3. **Month 2:** the first wide chip, the first I2C, and the fault codes.
4. **Months 3, 4 and 5**, in any order (Month 5 needs XC16 and a 3.3 V supply).
5. **Month 1 Part B** whenever you like: it is optional.

## Sheets

* [Month 1, AVR track (ATmega328P)](month-1a-avr.md)
* [Month 1, PIC track (PIC16F18857)](month-1b-pic.md)
* [Month 1, Part B (optional AVR programmer)](month-1c-partb.md)
* [Month 2 (PIC18F47K42 + MCP23017)](month-2.md)
* [Month 3 (MCP3008 + MCP4822)](month-3.md)
* [Month 4 (PIC16F18446 + MCP7940N)](month-4.md)
* [Month 5 (PIC24FJ64GA002 + 24LC512, 3.3 V)](month-5.md)

## How to report what you find

For anything that does not pass, note the page, the step, what you expected, what you saw, and the **exact message** (copy and paste). Photos of the breadboard help enormously. On GitHub, use the *Bench report* issue template.

When a build passes on your bench, three things change: its status line on the page, its row in `VERIFICATION_LOG.md`, and (for PIC builds) its MPLAB X project is exported into `projects/mplabx/` (see the [projects and hardware guide](../PROJECTS_AND_HARDWARE_GUIDE.md)).
