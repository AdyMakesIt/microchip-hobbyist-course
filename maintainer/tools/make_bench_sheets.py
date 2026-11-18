#!/usr/bin/env python3
"""
make_bench_sheets.py - writes printable validation sheets from the build pages themselves, so a sheet can never
disagree with its page.  One sheet per month in maintainer/bench-sheets/, plus an index with the recommended order.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "maintainer", "bench-sheets"); os.makedirs(OUT, exist_ok=True)

SHEETS = [  # file, title, folder, pages, tools, assumption numbers from VERIFICATION_LOG.md
    ("month-1a-avr", "Month 1, AVR track (ATmega328P)", "month-01-electronic-dice", ["avr-1-blink.md", "avr-2-button.md", "avr-3-dice.md"],
     "VS Code + PlatformIO, USBasp or Uno R3, multimeter", [2, 4, 6]),
    ("month-1b-pic", "Month 1, PIC track (PIC16F18857)", "month-01-electronic-dice", ["pic-1-blink.md", "pic-2-button.md", "pic-3-dice.md"],
     "MPLAB X v6.20, XC8, PICkit 3, multimeter", [1, 2, 5]),
    ("month-1c-partb", "Month 1, Part B (optional AVR programmer)", "month-01-electronic-dice/avr-programmer",
     ["build-b1-minimum-board.md", "build-b2-programmer.md", "build-b3-program-a-chip.md"], "Arduino IDE, USBasp or Uno, USB-serial adapter", [7]),
    ("month-2", "Month 2 (PIC18F47K42 + MCP23017)", "month-02-workshop-command-centre",
     ["build-1-blink.md", "build-2-hello-expander.md", "build-3-led-chase.md", "build-4-command-centre.md"], "MPLAB X v6.20, XC8, PICkit 3", [1, 2, 3, 5]),
    ("month-3", "Month 3 (MCP3008 + MCP4822)", "month-03-analogue-in-out",
     ["build-1-adc-bar-graph.md", "build-2-dac.md", "build-3-loopback.md"], "MPLAB X v6.20, XC8, PICkit 3, multimeter", [2, 8]),
    ("month-4", "Month 4 (PIC16F18446 + MCP7940N)", "month-04-binary-clock",
     ["build-1-blink.md", "build-2-rtc-hello.md", "build-3-binary-clock.md"], "MPLAB X v6.20, XC8, PICkit 3", [1, 9, 11]),
    ("month-5", "Month 5 (PIC24FJ64GA002 + 24LC512, 3.3 V)", "month-05-sixteen-bit-and-memory",
     ["build-1-blink.md", "build-2-eeprom-hello.md", "build-3-boot-counter.md"], "MPLAB X v6.20, XC16, PICkit 3, multimeter", [1, 2, 10]),
]

def section(text, key):
    m = re.search(r"^## \d+\. " + key + r".*?\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""

def assumptions():
    t = open(os.path.join(ROOT, "maintainer", "VERIFICATION_LOG.md"), encoding="utf-8").read()
    a = t.index("## Assumptions that only the real tools")
    out = {}
    for line in t[a:].split("\n"):
        if line.startswith("|"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if c and c[0].isdigit(): out[int(c[0])] = c[1:]
    return out

def main():
    A = assumptions(); index = []
    for fn, title, folder, pages, tools, assum in SHEETS:
        L = [f"# Bench validation sheet: {title}", "", f"**Tools:** {tools}", "", "Date: ____________   Photo of the breadboard taken: [ ]", "",
             "Work through the builds **in order**. Tick what happened, and write down any message you saw (compiler, programmer, avrdude) exactly as it appeared.", ""]
        for pg in pages:
            p = os.path.join(ROOT, folder, pg)
            if not os.path.exists(p): continue
            t = open(p, encoding="utf-8").read().replace("\r\n", "\n")
            name = re.search(r"^# (.*)$", t, re.M).group(1)
            L += [f"## {name}", "", f"Page: `{folder}/{pg}`", ""]
            chk = section(t, "Check before you power it")
            items = [re.sub(r"^\s*(\d+\.|[*-])\s*", "- [ ] ", l) for l in chk.split("\n") if re.match(r"^\s*(\d+\.|[*-])\s", l)]
            if items: L += ["**Before power (meter checks):**", ""] + items + [""]
            L += ["**Programming:**", "", "- [ ] Built with no errors", "- [ ] Programmed", "- [ ] Program runs", ""]
            ps = section(t, "Pass check")
            boxes = [l.replace("* [ ]", "- [ ]") for l in ps.split("\n") if l.startswith("* [ ]")]
            if boxes: L += ["**Pass checks:**", ""] + boxes + [""]
            L += ["| Result | Notes / exact messages |", "|---|---|", "| [ ] passed   [ ] partly   [ ] failed | |", ""]
        if assum:
            L += ["## Assumptions to confirm this month", "", "These were written from datasheets and published examples, not from a real build. Tick each when you have confirmed it, or note what differs.", "",
                  "| # | Assumption | Confirmed? |", "|:-:|---|:-:|"]
            for n in assum:
                if n in A: L.append(f"| {n} | {A[n][0]} | [ ] |")
            L.append("")
        L += ["## Summary", "", "Overall: [ ] all builds passed   [ ] some failed.   Biggest problem: ______________________________", ""]
        open(os.path.join(OUT, fn + ".md"), "w", encoding="utf-8").write("\n".join(L).rstrip("\n") + "\n")
        index.append((fn, title))
    I = ["# Bench validation kit", "",
         "Printable sheets for testing the course on real hardware. Each sheet is **generated from the build pages**, so it always matches them. "
         "Run `python3 maintainer/tools/make_bench_sheets.py` after any change to a page.", "",
         "## Suggested order", "",
         "1. **Month 1, AVR track:** the simplest, and it proves your PlatformIO and programmer set-up (the `0x1e950f` signature test comes first).",
         "2. **Month 1, PIC track:** proves MPLAB X, XC8, the PICkit 3 and the `#pragma config` block.",
         "3. **Month 2:** the first wide chip, the first I2C, and the fault codes.",
         "4. **Months 3, 4 and 5**, in any order (Month 5 needs XC16 and a 3.3 V supply).",
         "5. **Month 1 Part B** whenever you like: it is optional.", "",
         "## Sheets", ""]
    for fn, title in index: I.append(f"* [{title}]({fn}.md)")
    I += ["", "## How to report what you find", "",
          "For anything that does not pass, note the page, the step, what you expected, what you saw, and the **exact message** (copy and paste). "
          "Photos of the breadboard help enormously. On GitHub, use the *Bench report* issue template.", "",
          "When a build passes on your bench, three things change: its status line on the page, its row in `VERIFICATION_LOG.md`, and (for PIC builds) its MPLAB X project is exported into `projects/mplabx/` "
          "(see the [projects and hardware guide](../PROJECTS_AND_HARDWARE_GUIDE.md)).", ""]
    open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write("\n".join(I))
    print("wrote", len(index), "bench sheets")

if __name__ == "__main__": main()
