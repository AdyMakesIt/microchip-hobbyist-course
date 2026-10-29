#!/usr/bin/env python3
"""Regenerates every diagram (SVG + PNG) after VERIFYING each breadboard layout against its schematic."""
import os, sys, subprocess
from mhc_draw import BBDraw, SchDraw
from circuits import month1, month2, month1_avr, M1_BUILDS, M2_BUILDS, AVR_BUILDS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MONTHS = [("month-01-electronic-dice", month1, M1_BUILDS, "Month 1"),
          ("month-02-workshop-command-centre", month2, M2_BUILDS, "Month 2"),
          ("month-01-electronic-dice/avr-programmer", month1_avr, AVR_BUILDS, "Month 1 Part B")]

def main(png=True):
    bad = 0
    for folder, fn, builds, label in MONTHS:
        c, b = fn()
        img = os.path.join(ROOT, folder, "images"); os.makedirs(img, exist_ok=True)
        for n, name in builds.items():
            problems = b.verify(n)
            if problems:
                bad += 1; print(f"!! {label} build {n}: layout does NOT match schematic:"); [print("   -", p) for p in problems]; continue
            sch = SchDraw(c, n, f"{label} - {name}: schematic").render()
            bb = BBDraw(b, n, f"{label} - {name}: breadboard").render()
            for nm, svg in ((f"build-{n}-schematic", sch), (f"build-{n}-breadboard", bb)):
                p = os.path.join(img, nm + ".svg"); open(p, "w").write(svg)
                if png: subprocess.run(["node", os.path.join(HERE, "svg2png.js"), p, p[:-4] + ".png", "1500"], check=True, capture_output=True)
            print(f"ok  {label} build {n}")
    return bad

if __name__ == "__main__":
    sys.exit(1 if main(png="--no-png" not in sys.argv) else 0)
