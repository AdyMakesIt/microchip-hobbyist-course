#!/usr/bin/env python3
"""
make_projects.py - keeps the ready-to-open projects in step with the code shown on the pages.

  code/<build>/main.c           the source of truth (what the page shows)
  projects/platformio/<build>/  GENERATED here for the AVR builds (platformio.ini + src/main.c)
  projects/arduino/<sketch>/    GENERATED here for Arduino sketches (the folder name must equal the sketch name)
  projects/mplabx/<build>.X/    EXPORTED from MPLAB X by the author after a build has been bench-tested (not generated)

Also writes projects/README.md per month and maintainer/PROJECT_STATUS.md, and CHECKS that every project
holds exactly the same main.c as code/.   Usage:  python3 make_projects.py [--check]
"""
import os, sys, shutil, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

MONTHS = [  # folder, label, PIC device (or None), compiler, notes
    ("month-01-electronic-dice", "Month 1", "PIC16F18857 (for the pic-* builds)", "XC8", ""),
    ("month-02-workshop-command-centre", "Month 2", "PIC18F47K42", "XC8", ""),
    ("month-03-analogue-in-out", "Month 3", "PIC18F47K42", "XC8", ""),
    ("month-04-binary-clock", "Month 4", "PIC16F18446", "XC8", ""),
    ("month-05-sixteen-bit-and-memory", "Month 5", "PIC24FJ64GA002", "XC16", "3.3 V board"),
]
PIO_INI = """; PlatformIO project for the ATmega328P (internal 1 MHz oscillator, factory fuses).
; Choose the environment that matches your programmer. Build: the tick; upload: the arrow.
[platformio]
default_envs = usbasp

[env:usbasp]
platform = atmelavr
board = ATmega328P
board_build.f_cpu = 1000000L
upload_protocol = usbasp
upload_flags =
    -Pusb
    -B10

[env:uno_isp]
; an Arduino Uno R3 running the ArduinoISP example, used as a programmer
platform = atmelavr
board = ATmega328P
board_build.f_cpu = 1000000L
upload_protocol = stk500v1
upload_port = COM3   ; change to your Uno's port (Linux/macOS: /dev/ttyACM0)
upload_speed = 19200
upload_flags =
    -P$UPLOAD_PORT
    -b$UPLOAD_SPEED
"""
def read(p): return open(p, encoding="utf-8").read()
def write(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8").write(t)

def builds(folder):
    cd = os.path.join(ROOT, folder, "code")
    return sorted(d for d in os.listdir(cd) if os.path.isfile(os.path.join(cd, d, "main.c")) or glob.glob(os.path.join(cd, d, "*.ino"))) if os.path.isdir(cd) else []

def generate():
    problems = []
    for folder, label, device, compiler, note in MONTHS:
        base = os.path.join(ROOT, folder); bl = builds(folder)
        avr = [b for b in bl if b.startswith("avr-")]; pic = [b for b in bl if not b.startswith("avr-")]
        for b in avr:
            src = os.path.join(base, "code", b, "main.c")
            write(os.path.join(base, "projects", "platformio", b, "platformio.ini"), PIO_INI)
            write(os.path.join(base, "projects", "platformio", b, "src", "main.c"), read(src))
        mp = os.path.join(base, "projects", "mplabx"); os.makedirs(mp, exist_ok=True)
        existing = {os.path.basename(p)[:-2] for p in glob.glob(os.path.join(mp, "*.X"))}
        lines = ["# MPLAB X projects", "",
                 f"Complete MPLAB X projects for this month's PIC builds: **device {device}**, **compiler {compiler}**, tool **PICkit 3**{' (' + note + ')' if note else ''}.", "",
                 "Each project is a folder ending in `.X`. Open it with **File → Open Project** in MPLAB X. A project is added here only **after** its build has compiled and run on a real board.", "",
                 "| Build | Project folder | Status |", "|---|---|---|"]
        for b in pic:
            lines.append(f"| `code/{b}/main.c` | `{b}.X` | {'present' if b in existing else 'not yet exported'} |")
        lines += ["", "How projects are added: see the [projects and hardware guide](../../../maintainer/PROJECTS_AND_HARDWARE_GUIDE.md).", ""]
        if pic: write(os.path.join(mp, "README.md"), "\n".join(lines))
        # per-month projects README
        pr = ["# Ready-to-open projects", "", "Complete, working projects for every build in this month, so you can open one and run it without typing.", "",
              "| Folder | What is in it |", "|---|---|"]
        if pic: pr.append("| [`mplabx/`](mplabx/README.md) | MPLAB X projects for the PIC builds (added after each has been bench-tested) |")
        if avr: pr.append("| [`platformio/`](platformio/) | PlatformIO projects for the ATmega328P builds: open the folder in VS Code and press Build and Upload |")
        pr += ["", "The source on the build pages comes from `../code/`; these projects always hold an identical copy (checked automatically).", ""]
        write(os.path.join(base, "projects", "README.md"), "\n".join(pr))
    # Part B Arduino sketch
    pb = os.path.join(ROOT, "month-01-electronic-dice", "avr-programmer")
    ino = os.path.join(pb, "code", "blink-d9", "blink-d9.ino")
    write(os.path.join(pb, "projects", "arduino", "blink-d9", "blink-d9.ino"), read(ino))
    write(os.path.join(pb, "projects", "README.md"), "# Ready-to-open projects\n\n| Folder | What is in it |\n|---|---|\n| [`arduino/`](arduino/) | the Arduino sketch (open `blink-d9/blink-d9.ino` in the Arduino IDE; the folder name must match the sketch name) |\n\nThe ArduinoISP programmer program comes with the Arduino IDE (File → Examples → 11.ArduinoISP).\n")
    return problems

def check():
    bad = []
    for folder, label, device, compiler, note in MONTHS:
        base = os.path.join(ROOT, folder)
        for b in builds(folder):
            src = read(os.path.join(base, "code", b, "main.c"))
            for cand in (os.path.join(base, "projects", "platformio", b, "src", "main.c"), os.path.join(base, "projects", "mplabx", b + ".X", "main.c")):
                if os.path.exists(cand) and read(cand) != src: bad.append(f"{os.path.relpath(cand, ROOT)} differs from code/{b}/main.c")
            xdir = os.path.join(base, "projects", "mplabx", b + ".X")
            if os.path.isdir(xdir) and not os.path.exists(os.path.join(xdir, "nbproject")): bad.append(f"{os.path.relpath(xdir, ROOT)} has no nbproject folder (not a real MPLAB X project)")
    pb = os.path.join(ROOT, "month-01-electronic-dice", "avr-programmer")
    a, b2 = os.path.join(pb, "code", "blink-d9", "blink-d9.ino"), os.path.join(pb, "projects", "arduino", "blink-d9", "blink-d9.ino")
    if os.path.exists(b2) and read(a) != read(b2): bad.append("arduino sketch differs from code/")
    return bad

def status():
    rows = ["# Project and hardware status", "", "Generated by `tools/make_projects.py`. Update by running it; export MPLAB X projects as described in [the guide](PROJECTS_AND_HARDWARE_GUIDE.md).", "",
            "| Month | Build | Source | PlatformIO | MPLAB X | Arduino | KiCad schematic |", "|:-:|---|:-:|:-:|:-:|:-:|:-:|"]
    for folder, label, device, compiler, note in MONTHS:
        base = os.path.join(ROOT, folder); kicad = bool(glob.glob(os.path.join(base, "hardware", "kicad", "*.kicad_sch")))
        for b in builds(folder):
            pio = "Yes" if os.path.exists(os.path.join(base, "projects", "platformio", b, "platformio.ini")) else "n/a"
            mpx = "n/a" if b.startswith("avr-") else ("Yes" if os.path.isdir(os.path.join(base, "projects", "mplabx", b + ".X")) else "Not yet")
            rows.append(f"| {label[6:]} | {b} | Yes | {pio} | {mpx} | n/a | {'Yes' if kicad else 'Not yet'} |")
    rows.append("| 1B | blink-d9 | Yes | n/a | n/a | Yes | Not yet |")
    write(os.path.join(ROOT, "maintainer", "PROJECT_STATUS.md"), "\n".join(rows) + "\n")

if __name__ == "__main__":
    if "--check" not in sys.argv: generate()
    status()
    bad = check()
    for x in bad: print("!!", x)
    print("projects in step with code" if not bad else "PROJECT PROBLEMS FOUND")
    sys.exit(1 if bad else 0)
