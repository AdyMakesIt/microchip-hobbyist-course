#!/usr/bin/env python3
"""Regenerates every diagram (SVG + PNG) after VERIFYING each breadboard layout against its schematic."""
import os, sys, subprocess
from mhc_draw import BBDraw, SchDraw
from circuits import CIRCUITS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def main(png=True):
    bad = 0
    for entry in CIRCUITS:
        folder = entry["folder"]
        fn = entry["fn"]
        builds = entry["builds"]
        label = entry["title"]
        prefix = entry.get("img_prefix", entry["prefix"])

        c, b = fn()
        img = os.path.join(ROOT, folder, "images")
        os.makedirs(img, exist_ok=True)
        for n, name in builds.items():
            problems = b.verify(n)
            if problems:
                bad += 1
                print(f"!! {label} build {n}: layout does NOT match schematic:")
                for p in problems:
                    print("   -", p)
                continue
            sch = SchDraw(c, n, f"{label} - {name}: schematic").render()
            bb = BBDraw(b, n, f"{label} - {name}: breadboard").render()
            for nm, svg in ((f"{prefix}-{n}-schematic", sch), (f"{prefix}-{n}-breadboard", bb)):
                p = os.path.join(img, nm + ".svg")
                open(p, "w", encoding="utf-8").write(svg)
                if png:
                    subprocess.run(
                        ["node", os.path.join(HERE, "svg2png.js"), p, p[:-4] + ".png", "1500"],
                        check=True,
                        capture_output=True,
                    )
            print(f"ok  {label} build {n}")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(png="--no-png" not in sys.argv) else 0)
    