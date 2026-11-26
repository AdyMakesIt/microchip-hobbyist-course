#!/usr/bin/env python3
"""
sync_docs.py - keeps the Markdown pages in step with the code and the circuit descriptions.

Pages contain marker pairs. This script rewrites what is BETWEEN a pair, so the page can
never disagree with the real file or the verified circuit:

  <!-- code:code/month-01-avr-build-1-blink/main.c -->  ...  <!-- /code -->        the file, as a code block
  <!-- placement:2 -->                               ...  <!-- /placement -->    hole-by-hole steps for build 2
  <!-- connections:2 -->                             ...  <!-- /connections --> what connects to what (schematic view)
  <!-- bom -->                                       ...  <!-- /bom -->          parts counted from the circuit

Run:  python3 sync_docs.py        (make_all.py draws the pictures; run it first)
"""
import os, re, sys, collections
from mhc_draw import pin_table, pretty_ohms, RAILS, hole_node
from circuits import CIRCUITS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def months_from_registry(entries):
    """Build {folder: {key: circuit_fn}} from CIRCUITS; first key is default for unprefixed markers."""
    grouped = collections.defaultdict(dict)
    for entry in entries:
        folder = entry.get("folder")
        fn = entry.get("fn")
        if not folder or not callable(fn):
            continue
        bucket = grouped[folder]
        default_key = entry.get("doc_key") or (
            entry.get("prefix") if folder == "month-01-electronic-dice" else "main"
        )
        for k in (default_key, entry.get("prefix"), entry.get("img_prefix"), entry.get("id")):
            if k:
                bucket.setdefault(k, fn)
    return dict(grouped)


MONTHS = months_from_registry(CIRCUITS)

RAIL_NAME = {
    "TP": "top **red** rail (+)",
    "TN": "top **blue** rail (−)",
    "BN": "bottom **blue** rail (−)",
    "BP": "bottom **red** rail (+)",
}


def hole(h):
    col, row = h
    if row in RAILS:
        return f"{RAIL_NAME[row]}, near column {col}"
    return f"**{col}{row}**"


def describe(c, b, it):
    k = it["kind"]
    if k == "ic":
        ic = c.ics[it["ref"]]
        half = ic.npins // 2
        top, bot = it["rows"]
        c0 = it["col"]
        where = (
            f"Pin 1 in hole **{c0}{bot}**, notch to the **left** (towards the lower column numbers). Pins 1–{half} run along row {bot} "
            f"(columns {c0}–{c0+half-1}); pins {half+1}–{ic.npins} run back along row {top}."
        )
        extra = (
            "This is a **wide (600 mil)** chip: it will not sit in the centre channel like a skinny chip. "
            f"Put its two rows of pins in rows **{top}** and **{bot}** so it straddles the channel."
            if ic.width == "wide"
            else "Skinny (300 mil) chip: one row of pins each side of the centre channel (rows e and f)."
        )
        return (f"{ic.ref} {ic.part}", where, extra)
    if k == "R":
        return (
            f"{it['ref']} {pretty_ohms(c.parts[it['ref']][1])} resistor",
            f"{hole(it['a'])} and {hole(it['b'])}",
            "either way round",
        )
    if k == "C":
        return (
            f"{it['ref']} {c.parts[it['ref']][1]} capacitor",
            f"{hole(it['a'])} and {hole(it['b'])}",
            "ceramic: either way round; keep the legs short",
        )
    if k == "LED":
        return (
            f"{it['ref']} red LED",
            f"**long leg** in {hole(it['a'])}, **short leg** in {hole(it['b'])}",
            "the long leg (+) goes towards the resistor",
        )
    if k == "PIEZO":
        return (
            f"{it['ref']} piezo",
            f"{hole(it['a'])} and {hole(it['b'])}",
            "a bare piezo disc has no polarity",
        )
    if k == "wire":
        lab = it.get("label", "")
        purpose = {"+5V": f"{c.supply_label} power", "GND": "ground"}.get(lab, f"signal {lab}")
        col = {"+5V": "red", "GND": "black"}.get(lab, "any colour")
        return ("jumper wire", f"{hole(it['a'])} → {hole(it['b'])}", f"{purpose} ({col})")
    if k == "POT":
        return (
            f"{it['ref']} {pretty_ohms(c.parts[it['ref']][1])} potentiometer",
            f"legs in {hole(it['a'])}, {hole(it['w'])} and {hole(it['b'])}",
            "outer legs = the two ends of the track, middle leg = the wiper (the moving contact)",
        )
    if k == "XTAL":
        return (
            f"{it['ref']} {c.parts[it['ref']][1]} crystal",
            f"{hole(it['a'])} and {hole(it['b'])}",
            "no polarity; the metal can may be left standing up",
        )
    if k == "lead":
        conn = c.ics[it["conn"]]
        where = (
            f"from {conn.part} **{it['label']}**"
            if conn.named_only
            else f"from {conn.part} pin **{it['pin']}** ({it['label']})"
        )
        return (f"{conn.part} lead: {it['label']}", f"{where} to {hole(it['a'])}", "female-to-male Dupont lead")
    if k == "SW":
        col = it["col"]
        return (
            f"{it['ref']} push button",
            f"straddling the centre channel with legs in **{col}e, {col+2}e, {col}f, {col+2}f**",
            f"only the diagonal legs ({col}e and {col+2}f) are wired; keep strips {col+2}e and {col}f empty. Works either way round.",
        )
    if k == "mb102":
      v_top = it.get("top_voltage", it.get("voltage", "5 V"))
      v_bot = it.get("bottom_voltage", it.get("voltage", "5 V"))
      v_desc = v_top if v_top == v_bot else f"top rail {v_top}, bottom rail {v_bot}"
      return (
          f"MB102 breadboard power supply ({v_desc})",
          f"plugged into the left end of the power rails at column {it['col']} (`TP{it['col']}`, `TN{it['col']}`, `BN{it['col']}`, `BP{it['col']}`)",
          f"set the yellow jumpers to **{v_desc}**; check the rail voltage with your multimeter before inserting chips",
        )    
    if k == "battery":
        base_label = it.get("label", "Battery pack")
        volt = it.get("voltage")
        part_name = f"{base_label} ({volt})" if volt else base_label
        return (
            part_name,
            f"**red (+)** lead to {hole(it['a'])}, **black (−)** lead to {hole(it['b'])}",
            "check polarity before connecting",
        )
    raise ValueError(k)


def strip_pins(c, b, build):
    """strip node -> list of (ic ref, pin) for every chip placed up to this build"""
    m = {}
    for it in b.items:
        if it["kind"] == "ic" and it["build"] <= build:
            ic = c.ics[it["ref"]]
            for p in range(1, ic.npins + 1):
                m.setdefault(hole_node(b.ic_pin_hole(it["ref"], p)), []).append((it["ref"], p))
    return m


def pins_text(c, b, build, it):
    """the chip pin(s) this item connects to, as a short text (for the 'Pin(s)' column)"""
    k = it["kind"]
    if k == "ic":
        return "1"
    if k == "mb102":
        return "-"
    if k == "battery":
        return "-"
    m = strip_pins(c, b, build)
    holes = []
    if k == "SW":
        col = it["col"]
        holes = [(col, "e"), (col + 2, "f")]
    else:
        for key in ("a", "w", "b"):
            if key in it:
                holes.append(it[key])
    found = []
    for h in holes:
        for ref, p in m.get(hole_node(h), []):
            if (ref, p) not in found:
                found.append((ref, p))
    if not found:
        return "–"
    many = len([r for r in c.ics if not c.ics[r].connector]) > 1
    return " / ".join((f"{r}:{p}" if many else str(p)) for r, p in found)


def rail_note(it):
    if it["kind"] == "wire" and it["a"][1] in RAILS and it["b"][1] in RAILS:
        return " After placing it, **check the power**: measure across the rails with the meter."
    return ""


def placement_md(c, b, build):
    rows = []
    for it in b.items:
        if it["build"] == build:
            p, w, n = describe(c, b, it)
            rows.append((p, pins_text(c, b, build, it), w, n + rail_note(it)))
    out = ["| Step | Part | Pin(s) | Where it goes | Notes |", "|---:|---|:-:|---|---|"]
    for i, (p, pin, w, n) in enumerate(rows, 1):
        out.append(f"| {i} | {p} | {pin} | {w} | {n} |")
    return "\n".join(out)


def connections_md(c, b, build):
    rows = pin_table(c, b, build)
    out = ["| Starts at | Then goes through |", "|---|---|"]
    for s, t in rows:
        out.append(f"| {s} | {t} |")
    return "\n".join(out)


def bom_counts(c, b):
    cnt = collections.Counter()
    for ref, (kind, val) in c.parts.items():
        if kind == "R":
            cnt[("Resistor", pretty_ohms(val))] += 1
        elif kind == "C":
            cnt[("Ceramic capacitor", val)] += 1
        elif kind == "LED":
            cnt[("LED, 5 mm", "red")] += 1
        elif kind == "SW":
            cnt[("Push button (4-leg tact switch)", "6 mm")] += 1
        elif kind == "PIEZO":
            cnt[("Piezo disc (passive)", "")] += 1
        elif kind == "XTAL":
            cnt[("Crystal", val)] += 1
        elif kind == "POT":
            cnt[("Potentiometer (rotary or trimmer)", pretty_ohms(val))] += 1
    cnt[("Jumper wires, solid or male-to-male", "assorted lengths")] = sum(1 for it in b.items if it["kind"] == "wire")
    conns = sorted({c.ics[it["conn"]].part for it in b.items if it["kind"] == "lead"})
    cnt[("LEADS", " / ".join(conns))] = sum(1 for it in b.items if it["kind"] == "lead")
    return cnt


def bom_md(circuits):
    """circuits: list of (c, b). Quantities are the MAXIMUM across the circuits, because the builds reuse parts."""
    merged = collections.Counter()
    for c, b in circuits:
        for k, n in bom_counts(c, b).items():
            if k[0] == "LEADS":
                k = ("LEADS", "")
            merged[k] = max(merged[k], n)
    conns = sorted({c.ics[it["conn"]].part for c, b in circuits for it in b.items if it["kind"] == "lead"})
    out = ["| Part | Value | Qty used | Buy at least |", "|---|---|---:|---:|"]
    order = [
        "Resistor",
        "Ceramic capacitor",
        "Crystal",
        "Crystal, HC-49",
        "Potentiometer (rotary or trimmer)",
        "LED, 5 mm",
        "Push button (4-leg tact switch)",
        "Piezo disc (passive)",
        "Jumper wires, solid or male-to-male",
        "LEADS",
    ]
    for (k, v) in sorted(merged, key=lambda kv: (order.index(kv[0]), kv[1])):
        n = merged[(k, v)]
        if k == "LEADS":
            out.append(f"| Female-to-male Dupont leads ({' / '.join(conns)} → breadboard) | | {n} | {n + 1} |")
        elif k.startswith("Jumper"):
            out.append(f"| {k} | {v} | {n} | {n + 6} |")
        else:
            out.append(f"| {k} | {v} | {n} | {n + max(1, round(n * .25))} |")
    return "\n".join(out)


def resolve_code_path(base, md_name, arg):
    """Resolve a code marker target using <md_stem> as the canonical code subdirectory name."""
    direct = os.path.normpath(os.path.join(base, arg))
    if os.path.isfile(direct):
        return direct, arg

    parts = arg.replace("\\", "/").split("/")
    if parts and parts[0] == "code" and len(parts) >= 3:
        code_root = os.path.join(base, "code")
        tail = os.path.join(*parts[2:])
        old_sub = parts[1]
        md_stem = os.path.splitext(md_name)[0]

        # 1. Canonical match: code/<md_stem>/<tail>
        if md_stem and md_stem != "README":
            canonical_cand = os.path.join(code_root, md_stem, tail)
            if os.path.isfile(canonical_cand):
                rel = os.path.relpath(canonical_cand, base).replace("\\", "/")
                return canonical_cand, rel

        # 2. Fallback match: any code/<dir>/<tail> where <dir> matches or ends with <old_sub>
        if os.path.isdir(code_root):
            matches = []
            for entry in sorted(os.listdir(code_root)):
                sub_dir = os.path.join(code_root, entry)
                if os.path.isdir(sub_dir) and (entry == old_sub or entry.endswith(old_sub)):
                    cand = os.path.join(sub_dir, tail)
                    if os.path.isfile(cand):
                        rel = os.path.relpath(cand, base).replace("\\", "/")
                        matches.append((cand, rel))
            if len(matches) == 1:
                return matches[0]
            if len(matches) > 1:
                raise FileNotFoundError(
                    f"Ambiguous code path {arg!r} in {base}: {[m[1] for m in matches]}"
                )

    raise FileNotFoundError(f"Code file not found for {arg!r} under {base} (page: {md_name})")


def fence_code(path):
    txt = open(path, encoding="utf-8").read().rstrip("\n")
    lang = "cpp" if path.endswith((".ino", ".cpp")) else "c"
    return "```" + lang + "\n" + txt + "\n```"


def resolve_key(built, k):
    if k in built:
        return built[k]
    aliases = {
        "pic": ("m01_pic", "m1pic", "build-pic"),
        "avr": ("m01_avr", "m1avr", "build-avr"),
    }
    for cand in aliases.get(k, ()):
        if cand in built:
            return built[cand]
    for candidate, fn_pair in built.items():
        if candidate.endswith(f"_{k}") or candidate.endswith(f"-{k}"):
            return fn_pair
    raise KeyError(k)


PAT = re.compile(r"(<!-- (code|placement|connections|bom)(?::([^ ]+))? -->)(.*?)(<!-- /\2 -->)", re.S)


def process(folder, circuits):
    keys = list(circuits)
    built = {k: fn() for k, fn in circuits.items()}
    base = os.path.join(ROOT, folder)
    changed = 0

    def pick(arg):
        """'avr:2' -> (circuit, 2);  '2' -> (default circuit, 2)"""
        if ":" in arg:
            k, n = arg.rsplit(":", 1)
        else:
            k, n = keys[0], arg
        try:
            circuit_pair = resolve_key(built, k)
        except KeyError:
            raise KeyError(f"{folder}: unknown circuit key {k!r}; available keys: {list(built.keys())}")
        return circuit_pair, int(n)

    for name in sorted(os.listdir(base)):
        if not name.endswith(".md"):
            continue
        p = os.path.join(base, name)
        t = open(p, encoding="utf-8").read()

        def rep(m):
            open_tag, kind, arg, _, close = m.groups()
            if kind == "code":
                resolved_path, resolved_arg = resolve_code_path(base, name, arg)
                if resolved_arg != arg:
                    open_tag = f"<!-- code:{resolved_arg} -->"
                body = fence_code(resolved_path)
            elif kind == "placement":
                (c, b), n = pick(arg)
                body = placement_md(c, b, n)
            elif kind == "connections":
                (c, b), n = pick(arg)
                body = connections_md(c, b, n)
            else:
                requested = arg.split("+") if arg else keys
                selected = []
                missing = []
                for k in requested:
                    try:
                        selected.append(resolve_key(built, k))
                    except KeyError:
                        missing.append(k)
                if missing:
                    raise KeyError(
                        f"{folder}/{name}: unknown BOM key(s) {missing}; available keys: {list(built.keys())}"
                    )
                body = bom_md(selected)
            return f"{open_tag}\n{body}\n{close}"

        new = PAT.sub(rep, t)
        if new != t:
            open(p, "w", encoding="utf-8").write(new)
            changed += 1
    return changed


if __name__ == "__main__":
    from format_tables import format_tree

    for folder, circuits in MONTHS.items():
        print(folder, "pages updated:", process(folder, circuits))
    print("tables aligned in", format_tree(ROOT), "pages")
    