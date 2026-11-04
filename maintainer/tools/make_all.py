#!/usr/bin/env python3
"""Regenerates every diagram (SVG + PNG) after VERIFYING each breadboard layout against its schematic."""
import os, sys, subprocess
from mhc_draw import BBDraw, SchDraw
from circuits import month1, month2, month3, month4, month5, month1_avr, month1_isp, M1_BUILDS, M2_BUILDS, M3_BUILDS, M4_BUILDS, M5_BUILDS, AVR1_BUILDS, ISP_BUILDS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
# (folder, circuit, builds, label, image-file prefix)
MONTHS = [("month-01-electronic-dice", month1, M1_BUILDS, "Month 1 (PIC)", "pic"),
          ("month-01-electronic-dice", month1_avr, AVR1_BUILDS, "Month 1 (ATmega328P)", "avr"),
          ("month-02-workshop-command-centre", month2, M2_BUILDS, "Month 2", "build"),
          ("month-03-analogue-in-out", month3, M3_BUILDS, "Month 3", "build"),
          ("month-04-binary-clock", month4, M4_BUILDS, "Month 4", "build"),
          ("month-05-sixteen-bit-and-memory", month5, M5_BUILDS, "Month 5", "build"),
          ("month-01-electronic-dice/avr-programmer", month1_isp, ISP_BUILDS, "Month 1 Part B", "build")]

def main(png=True):
    bad = 0
    for folder, fn, builds, label, prefix in MONTHS:
        c, b = fn()
        img = os.path.join(ROOT, folder, "images"); os.makedirs(img, exist_ok=True)
        for n, name in builds.items():
            problems = b.verify(n)
            if problems:
                bad += 1; print(f"!! {label} build {n}: layout does NOT match schematic:"); [print("   -", p) for p in problems]; continue
            sch = SchDraw(c, n, f"{label} - {name}: schematic").render()
            bb = BBDraw(b, n, f"{label} - {name}: breadboard").render()
            for nm, svg in ((f"{prefix}-{n}-schematic", sch), (f"{prefix}-{n}-breadboard", bb)):
                p = os.path.join(img, nm + ".svg"); open(p, "w").write(svg)
                if png: subprocess.run(["node", os.path.join(HERE, "svg2png.js"), p, p[:-4] + ".png", "1500"], check=True, capture_output=True)
            print(f"ok  {label} build {n}")
    return bad

if __name__ == "__main__":
    sys.exit(1 if main(png="--no-png" not in sys.argv) else 0)
