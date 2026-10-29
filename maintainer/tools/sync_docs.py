#!/usr/bin/env python3
"""
sync_docs.py - keeps the Markdown pages in step with the code and the circuit descriptions.

Pages contain marker pairs. This script rewrites what is BETWEEN a pair, so the page can
never disagree with the real file or the verified circuit:

  <!-- code:code/build-1-blink/main.c -->        ...  <!-- /code -->        the file, as a code block
  <!-- placement:2 -->                           ...  <!-- /placement -->    hole-by-hole steps for build 2
  <!-- connections:2 -->                         ...  <!-- /connections --> what connects to what (schematic view)
  <!-- bom -->                                   ...  <!-- /bom -->          parts counted from the circuit

Run:  python3 sync_docs.py        (make_all.py draws the pictures; run it first)
"""
import os, re, sys, collections
from mhc_draw import pin_table, pretty_ohms, RAILS
from circuits import month1, month2, month1_avr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MONTHS = {"month-01-electronic-dice": month1, "month-02-workshop-command-centre": month2,
          "month-01-electronic-dice/avr-programmer": month1_avr}

RAIL_NAME = {"TP": "top **red** rail (+)", "TN": "top **blue** rail (−)", "BN": "bottom **blue** rail (−)", "BP": "bottom **red** rail (+)"}

def hole(h):
    col, row = h
    if row in RAILS: return f"{RAIL_NAME[row]}, near column {col}"
    return f"**{col}{row}**"

def describe(c, b, it):
    k = it["kind"]
    if k == "ic":
        ic = c.ics[it["ref"]]; half = ic.npins // 2; top, bot = it["rows"]
        c0 = it["col"]
        where = (f"Pin 1 in hole **{c0}{bot}**, notch to the **left**. Pins 1–{half} run along row {bot} "
                 f"(columns {c0}–{c0+half-1}); pins {half+1}–{ic.npins} run back along row {top}.")
        extra = ("This is a **wide (600 mil)** chip: it will not sit in the centre channel like a skinny chip. "
                 f"Put its two rows of pins in rows **{top}** and **{bot}** so it straddles the channel.") if ic.width == "wide" else \
                "Skinny (300 mil) chip: one row of pins each side of the centre channel (rows e and f)."
        return (f"{ic.ref} {ic.part}", where, extra)
    if k == "R":
        return (f"{it['ref']} {pretty_ohms(c.parts[it['ref']][1])} resistor", f"{hole(it['a'])} and {hole(it['b'])}", "either way round")
    if k == "C":
        return (f"{it['ref']} {c.parts[it['ref']][1]} capacitor", f"{hole(it['a'])} and {hole(it['b'])}", "ceramic: either way round; keep the legs short")
    if k == "LED":
        return (f"{it['ref']} red LED", f"**long leg** in {hole(it['a'])}, **short leg** in {hole(it['b'])}", "the long leg (+) goes towards the resistor")
    if k == "PIEZO":
        return (f"{it['ref']} piezo", f"{hole(it['a'])} and {hole(it['b'])}", "a bare piezo disc has no polarity")
    if k == "wire":
        lab = it.get("label", "")
        purpose = {"+5V": "+5 V power", "GND": "ground"}.get(lab, f"signal {lab}")
        col = {"+5V": "red", "GND": "black"}.get(lab, "any colour")
        return ("jumper wire", f"{hole(it['a'])} → {hole(it['b'])}", f"{purpose} ({col})")
    if k == "XTAL":
        return (f"{it['ref']} {c.parts[it['ref']][1]} crystal", f"{hole(it['a'])} and {hole(it['b'])}", "no polarity; the metal can may be left standing up")
    if k == "lead":
        conn = c.ics[it["conn"]]
        where = f"from {conn.part} **{it['label']}**" if conn.named_only else f"from {conn.part} pin **{it['pin']}** ({it['label']})"
        return (f"{conn.part} lead: {it['label']}", f"{where} to {hole(it['a'])}", "female-to-male Dupont lead")
    if k == "SW":
        col = it["col"]
        return (f"{it['ref']} push button", f"straddling the centre channel with legs in **{col}e, {col+2}e, {col}f, {col+2}f**",
                f"only the diagonal legs ({col}e and {col+2}f) are wired; keep strips {col+2}e and {col}f empty. Works either way round.")
    raise ValueError(k)

def placement_md(c, b, build):
    rows = []
    for it in b.items:
        if it["build"] == build: rows.append(describe(c, b, it))
    removed = [it for it in b.items if it.get("until", 99) == build - 1 and build > 1]
    out = ["| Step | Part | Where it goes | Notes |", "|---:|---|---|---|"]
    for i, (p, w, n) in enumerate(rows, 1):
        out.append(f"| {i} | {p} | {w} | {n} |")
    return "\n".join(out)

def connections_md(c, b, build):
    rows = pin_table(c, b, build)
    out = ["| Starts at | Then goes through |", "|---|---|"]
    for s, t in rows: out.append(f"| {s} | {t} |")
    return "\n".join(out)

def bom_md(c, b):
    cnt = collections.Counter()
    for ref, (kind, val) in c.parts.items():
        if kind == "R": cnt[("Resistor", pretty_ohms(val))] += 1
        elif kind == "C": cnt[("Ceramic capacitor", val)] += 1
        elif kind == "LED": cnt[("LED, 5 mm", "red")] += 1
        elif kind == "SW": cnt[("Push button (4-leg tact switch)", "6 mm")] += 1
        elif kind == "PIEZO": cnt[("Piezo disc (passive)", "")] += 1
        elif kind == "XTAL": cnt[("Crystal, HC-49", val)] += 1
    wires = sum(1 for it in b.items if it["kind"] == "wire")
    leads = sum(1 for it in b.items if it["kind"] == "lead")
    out = ["| Part | Value | Qty used | Buy at least |", "|---|---|---:|---:|"]
    order = ["Resistor", "Ceramic capacitor", "Crystal, HC-49", "LED, 5 mm", "Push button (4-leg tact switch)", "Piezo disc (passive)"]
    for (k, v) in sorted(cnt, key=lambda kv: (order.index(kv[0]), kv[1])):
        n = cnt[(k, v)]
        out.append(f"| {k} | {v} | {n} | {n + max(1, round(n * .25))} |")
    out.append(f"| Jumper wires, solid or male-to-male | assorted lengths | {wires} | {wires + 6} |")
    conns = sorted({c.ics[it["conn"]].part for it in b.items if it["kind"] == "lead"})
    out.append(f"| Female-to-male Dupont leads ({' / '.join(conns)} → breadboard) | | {leads} | {leads + 1} |")
    return "\n".join(out)

def fence_code(path):
    txt = open(path).read().rstrip("\n")
    lang = "cpp" if path.endswith((".ino", ".cpp")) else "c"
    return "```" + lang + "\n" + txt + "\n```"

PAT = re.compile(r"(<!-- (code|placement|connections|bom)(?::([^ ]+))? -->)(.*?)(<!-- /\2 -->)", re.S)

def process(folder, fn):
    c, b = fn()
    base = os.path.join(ROOT, folder); changed = 0
    for name in sorted(os.listdir(base)):
        if not name.endswith(".md"): continue
        p = os.path.join(base, name); t = open(p).read()
        def rep(m):
            open_tag, kind, arg, _, close = m.groups()
            if kind == "code": body = fence_code(os.path.join(base, arg))
            elif kind == "placement": body = placement_md(c, b, int(arg))
            elif kind == "connections": body = connections_md(c, b, int(arg))
            else: body = bom_md(c, b)
            return f"{open_tag}\n{body}\n{close}"
        new = PAT.sub(rep, t)
        if new != t: open(p, "w").write(new); changed += 1
    return changed

if __name__ == "__main__":
    from format_tables import format_tree
    for folder, fn in MONTHS.items():
        print(folder, "pages updated:", process(folder, fn))
    print("tables aligned in", format_tree(ROOT), "pages")
