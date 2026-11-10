#!/usr/bin/env python3
"""
make_hardware.py - writes the KiCad head-start files for every circuit, from the verified circuit descriptions:

  <month>/hardware/exports/<name>-bom.csv       parts list with SUGGESTED KiCad footprints
  <month>/hardware/exports/<name>-netlist.csv   every net and the pins on it
  <month>/hardware/README.md                    what lives in the hardware folder
  <month>/hardware/kicad/README.md              where the KiCad project goes, and how to name it

The schematic itself (.kicad_sch) is drawn in KiCad and committed to hardware/kicad/ (see the guide).
"""
import os, csv
from circuits import month1, month1_avr, month1_isp, month2, month3, month4, month5
from mhc_draw import pretty_ohms

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# (folder, circuit fn, file prefix, title)
TARGETS = [("month-01-electronic-dice", month1, "pic", "Month 1, PIC track"),
           ("month-01-electronic-dice", month1_avr, "avr", "Month 1, ATmega328P track"),
           ("month-01-electronic-dice/avr-programmer", month1_isp, "programmer", "Month 1 Part B, AVR programmer"),
           ("month-02-workshop-command-centre", month2, "month2", "Month 2"),
           ("month-03-analogue-in-out", month3, "month3", "Month 3"),
           ("month-04-binary-clock", month4, "month4", "Month 4"),
           ("month-05-sixteen-bit-and-memory", month5, "month5", "Month 5")]

FOOT = {
    "R": "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
    "C": "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm",
    "LED": "LED_THT:LED_D5.0mm",
    "SW": "Button_Switch_THT:SW_PUSH_6mm",
    "PIEZO": "Buzzer_Beeper:Buzzer_12x9.5RM7.6",
    "POT": "Potentiometer_THT:Potentiometer_Alps_RK09K_Single_Vertical",
}
def xtal_foot(value): return "Crystal:Crystal_C26-LF_D2.1mm_L6.5mm_Vertical" if "kHz" in value else "Crystal:Crystal_HC49-U_Vertical"
def dip_foot(ic):
    if ic.connector:
        return {5: "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical", 4: "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical",
                6: "Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical"}.get(ic.npins, "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical")
    return f"Package_DIP:DIP-{ic.npins}_W{'15.24' if ic.width == 'wide' else '7.62'}mm"

def intro_build(b, ref):
    bl = [it["build"] for it in b.items if it.get("ref") == ref or it.get("conn") == ref]
    return min(bl) if bl else ""

def export(folder, fn, prefix, title):
    c, b = fn()
    d = os.path.join(ROOT, folder, "hardware", "exports"); os.makedirs(d, exist_ok=True)
    top = max(it["build"] for it in b.items)
    rows = [["Reference", "Value / part", "Type", "Suggested KiCad footprint (check it matches your part)", "Added in build"]]
    for ref, ic in c.ics.items():
        rows.append([ref, ic.part, "connector" if ic.connector else "IC", dip_foot(ic), intro_build(b, ref)])
    def keyfn(r): return (r[0].rstrip("0123456789"), int("".join(ch for ch in r[0] if ch.isdigit()) or 0))
    for ref, (kind, val) in sorted(c.parts.items(), key=lambda kv: keyfn([kv[0]])):
        if kind == "XTAL": foot = xtal_foot(val)
        else: foot = FOOT[kind]
        shown = pretty_ohms(val) if kind == "R" else val
        rows.append([ref, shown, {"R": "resistor", "C": "capacitor", "LED": "LED", "SW": "push button", "PIEZO": "piezo", "XTAL": "crystal", "POT": "potentiometer"}[kind], foot, intro_build(b, ref)])
    with open(os.path.join(d, f"{prefix}-bom.csv"), "w", newline="", encoding="utf-8") as f: csv.writer(f).writerows(rows)
    nets = c.netlist(top)
    nrows = [["Net", "Pins on this net"]]
    def pinlabel(ref, pin):
        if ref in c.ics:
            nm = c.ics[ref].pins.get(pin, ""); return f"{ref}.{pin}" + (f" ({nm})" if nm else "")
        return f"{ref}.{pin}"
    supply = c.supply_label.replace(" ", "")
    for name in sorted(nets, key=lambda n: (n not in ("+5V", "GND"), n)):
        pins = sorted(nets[name], key=lambda p: (p[0], str(p[1])))
        shown = supply if name == "+5V" else (name if not name.startswith("U") and "." not in name else "(unnamed) " + name)
        nrows.append([shown, "; ".join(pinlabel(r, p) for r, p in pins)])
    with open(os.path.join(d, f"{prefix}-netlist.csv"), "w", newline="", encoding="utf-8") as f: csv.writer(f).writerows(nrows)
    return len(rows) - 1, len(nrows) - 1

HW_README = """# Hardware files: {title}

This folder holds everything you need to turn this month's circuit into a printed circuit board (PCB).

| Folder | What is in it |
|---|---|
| [`kicad/`](kicad/README.md) | the **KiCad** schematic and project files (see the note there) |
| [`exports/`](exports/) | **parts lists** (`*-bom.csv`, with suggested KiCad footprints) and **connection lists** (`*-netlist.csv`, every wire and the pins on it), generated from the same circuit description as the pictures |

The pictures in `../images/` show the circuit on a breadboard. The files here are for designing a board. How to use them: [Taking a project further]({up}start-here/07-taking-a-project-further.md).
"""
KICAD_README = """# KiCad project files

Put this month's KiCad project here. Use these names so every month looks the same:

| File | Name |
|---|---|
| project | `{slug}.kicad_pro` |
| schematic | `{slug}.kicad_sch` |
| PCB (if you make one) | `{slug}.kicad_pcb` |
| schematic printed to PDF | `{slug}-schematic.pdf` (so people can read it without KiCad) |

Rules:

* One KiCad project per month. Mark which build each part belongs to with a **field** (for example `Build = 2`), or draw one sheet per build.
* Use KiCad's standard symbol and footprint libraries. If a part is missing, make it in KiCad's editors and store the library **in this folder** (`mhc-parts.kicad_sym`, `mhc-parts.pretty/`), so the project opens on any computer.
* Use the **parts list** in `../exports/` for values and footprints, and the **connection list** to check your wiring.
* Do **not** commit KiCad backups or caches (the repository's `.gitignore` already excludes them).

*No schematic has been drawn here yet.*
"""
def write_readmes(folder, title):
    hw = os.path.join(ROOT, folder, "hardware"); os.makedirs(os.path.join(hw, "kicad"), exist_ok=True)
    open(os.path.join(hw, "README.md"), "w", encoding="utf-8").write(HW_README.format(title=title, up="../" * (folder.count("/") + 2)))
    slug = os.path.basename(folder) if "/" not in folder else os.path.basename(os.path.dirname(folder)) + "-" + os.path.basename(folder)
    if not os.path.exists(os.path.join(hw, "kicad", "README.md")):
        open(os.path.join(hw, "kicad", "README.md"), "w", encoding="utf-8").write(KICAD_README.format(slug=slug))

if __name__ == "__main__":
    done = set()
    for folder, fn, prefix, title in TARGETS:
        n_parts, n_nets = export(folder, fn, prefix, title)
        if folder not in done: write_readmes(folder, title); done.add(folder)
        print(f"{folder}: {prefix}: {n_parts} parts, {n_nets} nets")
