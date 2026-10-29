#!/usr/bin/env python3
"""Small teaching diagrams (dice pip map, chip pin numbering, breadboard connections)."""
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
F = "DejaVu Sans, Verdana, Arial, sans-serif"

def save(path, svg):
    open(path, "w").write(svg)
    subprocess.run(["node", os.path.join(HERE, "svg2png.js"), path, path[:-4] + ".png", "1200"], check=True, capture_output=True)

def dice():
    pips = {"TOP_LEFT": (0, 0, "RC0", 11), "MID_LEFT": (0, 1, "RC1", 12), "BOTTOM_LEFT": (0, 2, "RC2", 13),
            "CENTRE": (1, 1, "RC3", 14), "TOP_RIGHT": (2, 0, "RC4", 15), "MID_RIGHT": (2, 1, "RC5", 16), "BOTTOM_RIGHT": (2, 2, "RC6", 17)}
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 330" width="640" height="330" font-family="{F}"><rect width="100%" height="100%" fill="#fff"/>',
         '<text x="14" y="26" font-size="16" font-weight="bold">Dice pip map: which LED is which pin</text>',
         '<rect x="40" y="46" width="230" height="250" rx="26" fill="#fafafa" stroke="#333" stroke-width="3"/>']
    for nm, (cx, cy, rc, pin) in pips.items():
        x = 95 + cx * 80; y = 100 + cy * 80
        o.append(f'<circle cx="{x}" cy="{y}" r="24" fill="#d32f2f" stroke="#7a1010" stroke-width="2"/>')
        o.append(f'<text x="{x}" y="{y+4}" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">{rc}</text>')
    o.append('<text x="300" y="80" font-size="13" font-weight="bold">LED order along the breadboard row</text>')
    for i, (nm, (cx, cy, rc, pin)) in enumerate(pips.items()):
        o.append(f'<text x="300" y="{106+i*26}" font-size="13">{i+1}. {nm.replace("_"," ").lower()} = <tspan font-weight="bold">{rc}</tspan> (chip pin {pin})</text>')
    o.append('</svg>'); return "\n".join(o)

def dip():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 330" width="760" height="330" font-family="{F}"><rect width="100%" height="100%" fill="#fff"/>',
         '<text x="14" y="26" font-size="16" font-weight="bold">Reading a chip: where is pin 1, and which way do the numbers go?</text>']
    x0, y0, n = 140, 110, 8
    o.append(f'<rect x="{x0}" y="{y0}" width="{n*52}" height="96" rx="4" fill="#2b2b2b"/>')
    o.append(f'<path d="M {x0} {y0+36} a 12 12 0 0 1 0 24" fill="#fff"/>')
    o.append(f'<circle cx="{x0+22}" cy="{y0+80}" r="5" fill="#ddd"/>')
    for i in range(n):
        x = x0 + 26 + i * 52
        o.append(f'<rect x="{x-6}" y="{y0+96}" width="12" height="26" fill="#cfcfcf" stroke="#555"/>')
        o.append(f'<text x="{x}" y="{y0+144}" font-size="14" font-weight="bold" text-anchor="middle">{i+1}</text>')
        o.append(f'<rect x="{x-6}" y="{y0-26}" width="12" height="26" fill="#cfcfcf" stroke="#555"/>')
        o.append(f'<text x="{x}" y="{y0-34}" font-size="14" font-weight="bold" text-anchor="middle" fill="#0b3d91">{2*n-i}</text>')
    o.append(f'<text x="{x0+n*26}" y="{y0+50}" font-size="14" fill="#fff" text-anchor="middle">notch (or dot) at the LEFT</text>')
    o.append('<text x="40" y="288" font-size="13">Hold the chip with the notch on the left. Pin 1 is the bottom-left pin (next to the dot).</text>')
    o.append('<text x="40" y="308" font-size="13">Numbers run right along the bottom, then back left along the top. (Example: a 16-pin chip.)</text>')
    o.append('</svg>'); return "\n".join(o)

def strips():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 330" width="720" height="330" font-family="{F}"><rect width="100%" height="100%" fill="#fff"/>',
         '<text x="14" y="26" font-size="16" font-weight="bold">How the holes are connected inside a breadboard</text>',
         '<rect x="20" y="44" width="680" height="252" rx="8" fill="#f4efe6" stroke="#b9b09f" stroke-width="2"/>',
         '<rect x="20" y="152" width="680" height="34" fill="#d9d2c2"/>']
    cols = 14; x0 = 120; p = 34
    for i in range(cols):
        x = x0 + i * p
        for half, rows in (("T", (0, 1, 2, 3, 4)), ("B", (0, 1, 2, 3, 4))):
            ys = [64 + r * 18 for r in rows] if half == "T" else [200 + r * 18 for r in rows]
            hl = i in (3, 8)
            if hl: o.append(f'<rect x="{x-9}" y="{ys[0]-10}" width="18" height="{ys[-1]-ys[0]+20}" rx="9" fill="#ffe34d" opacity=".8"/>')
            for y in ys: o.append(f'<rect x="{x-3}" y="{y-3}" width="6" height="6" fill="#5b5547"/>')
        o.append(f'<text x="{x}" y="58" font-size="10" fill="#7a725f" text-anchor="middle" opacity="0">{i}</text>')
    for r, lab in enumerate("abcde"): o.append(f'<text x="84" y="{68+r*18}" font-size="12" fill="#555" text-anchor="middle">{lab}</text>')
    for r, lab in enumerate("fghij"): o.append(f'<text x="84" y="{204+r*18}" font-size="12" fill="#555" text-anchor="middle">{lab}</text>')
    o.append('<text x="360" y="174" font-size="12" fill="#6b6354" text-anchor="middle">centre channel: NOT connected across</text>')
    o.append('<text x="40" y="318" font-size="13">The 5 holes of one column (a-e, or f-j) are joined. Yellow shows two examples. Rows run across, columns run up and down.</text>')
    o.append('</svg>'); return "\n".join(o)

if __name__ == "__main__":
    save(os.path.join(ROOT, "month-01-electronic-dice", "images", "dice-pip-map.svg"), dice())
    save(os.path.join(ROOT, "start-here", "images", "chip-pin-numbering.svg"), dip())
    save(os.path.join(ROOT, "start-here", "images", "breadboard-connections.svg"), strips())
    print("ok")
