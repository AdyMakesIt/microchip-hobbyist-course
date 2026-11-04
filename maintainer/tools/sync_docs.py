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
from circuits import month1, month2, month3, month4, month5, month1_avr, month1_isp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
# folder -> {key: circuit function}. The first key is the default for markers that give no key.
MONTHS = {"month-01-electronic-dice": {"pic": month1, "avr": month1_avr},
          "month-02-workshop-command-centre": {"main": month2},
          "month-03-analogue-in-out": {"main": month3},
          "month-04-binary-clock": {"main": month4},
          "month-05-sixteen-bit-and-memory": {"main": month5},
          "month-01-electronic-dice/avr-programmer": {"main": month1_isp}}

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
        purpose = {"+5V": f"{c.supply_label} power", "GND": "ground"}.get(lab, f"signal {lab}")
        col = {"+5V": "red", "GND": "black"}.get(lab, "any colour")
        return ("jumper wire", f"{hole(it['a'])} → {hole(it['b'])}", f"{purpose} ({col})")
    if k == "POT":
        return (f"{it['ref']} {pretty_ohms(c.parts[it['ref']][1])} potentiometer", f"legs in {hole(it['a'])}, {hole(it['w'])} and {hole(it['b'])}", "outer legs = the two ends of the track, middle leg = the wiper (the moving contact)")
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

def bom_counts(c, b):
    cnt = collections.Counter()
    for ref, (kind, val) in c.parts.items():
        if kind == "R": cnt[("Resistor", pretty_ohms(val))] += 1
        elif kind == "C": cnt[("Ceramic capacitor", val)] += 1
        elif kind == "LED": cnt[("LED, 5 mm", "red")] += 1
        elif kind == "SW": cnt[("Push button (4-leg tact switch)", "6 mm")] += 1
        elif kind == "PIEZO": cnt[("Piezo disc (passive)", "")] += 1
        elif kind == "XTAL": cnt[("Crystal", val)] += 1
        elif kind == "POT": cnt[("Potentiometer (rotary or trimmer)", pretty_ohms(val))] += 1
    cnt[("Jumper wires, solid or male-to-male", "assorted lengths")] = sum(1 for it in b.items if it["kind"] == "wire")
    conns = sorted({c.ics[it["conn"]].part for it in b.items if it["kind"] == "lead"})
    cnt[("LEADS", " / ".join(conns))] = sum(1 for it in b.items if it["kind"] == "lead")
    return cnt

def bom_md(circuits):
    """circuits: list of (c, b). Quantities are the MAXIMUM across the circuits, because the builds reuse parts."""
    merged = collections.Counter()
    for c, b in circuits:
        for k, n in bom_counts(c, b).items():
            if k[0] == "LEADS": k = ("LEADS", "")
            merged[k] = max(merged[k], n)
    conns = sorted({c.ics[it["conn"]].part for c, b in circuits for it in b.items if it["kind"] == "lead"})
    out = ["| Part | Value | Qty used | Buy at least |", "|---|---|---:|---:|"]
    order = ["Resistor", "Ceramic capacitor", "Crystal", "Crystal, HC-49", "Potentiometer (rotary or trimmer)", "LED, 5 mm", "Push button (4-leg tact switch)", "Piezo disc (passive)",
             "Jumper wires, solid or male-to-male", "LEADS"]
    for (k, v) in sorted(merged, key=lambda kv: (order.index(kv[0]), kv[1])):
        n = merged[(k, v)]
        if k == "LEADS": out.append(f"| Female-to-male Dupont leads ({' / '.join(conns)} → breadboard) | | {n} | {n + 1} |")
        elif k.startswith("Jumper"): out.append(f"| {k} | {v} | {n} | {n + 6} |")
        else: out.append(f"| {k} | {v} | {n} | {n + max(1, round(n * .25))} |")
    return "\n".join(out)

def fence_code(path):
    txt = open(path).read().rstrip("\n")
    lang = "cpp" if path.endswith((".ino", ".cpp")) else "c"
    return "```" + lang + "\n" + txt + "\n```"

PAT = re.compile(r"(<!-- (code|placement|connections|bom)(?::([^ ]+))? -->)(.*?)(<!-- /\2 -->)", re.S)

def process(folder, circuits):
    keys = list(circuits)
    built = {k: fn() for k, fn in circuits.items()}
    base = os.path.join(ROOT, folder); changed = 0
    def pick(arg):
        """'avr:2' -> (circuit, 2);  '2' -> (default circuit, 2)"""
        if ":" in arg: k, n = arg.rsplit(":", 1)
        else: k, n = keys[0], arg
        return built[k], int(n)
    for name in sorted(os.listdir(base)):
        if not name.endswith(".md"): continue
        p = os.path.join(base, name); t = open(p, encoding="utf-8").read()
        def rep(m):
            open_tag, kind, arg, _, close = m.groups()
            if kind == "code": body = fence_code(os.path.join(base, arg))
            elif kind == "placement": (c, b), n = (pick(arg)[0], pick(arg)[1]); body = placement_md(c, b, n)
            elif kind == "connections": (c, b), n = (pick(arg)[0], pick(arg)[1]); body = connections_md(c, b, n)
            else:
                use = arg.split("+") if arg else keys
                body = bom_md([built[k] for k in use])
            return f"{open_tag}\n{body}\n{close}"
        new = PAT.sub(rep, t)
        if new != t: open(p, "w", encoding="utf-8").write(new); changed += 1
    return changed

if __name__ == "__main__":
    from format_tables import format_tree
    for folder, circuits in MONTHS.items():
        print(folder, "pages updated:", process(folder, circuits))
    print("tables aligned in", format_tree(ROOT), "pages")
