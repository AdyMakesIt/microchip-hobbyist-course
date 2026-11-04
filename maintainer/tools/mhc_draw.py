#!/usr/bin/env python3
"""
mhc_draw.py - draws the course's circuits from ONE description and checks them.

A circuit is described once, as 'chains' (a pin, then the parts in series, then where
it ends: GND, +5V or a named net).  From that single description this file produces:

  1. the schematic (SVG)
  2. the breadboard layout (SVG)  -- from a list of hole-by-hole placements
  3. a CHECK that the breadboard placement connects exactly the same things as the
     schematic (no missing link, no accidental short). If the check fails, no
     picture is written, so a wrong diagram cannot reach the course.
  4. the wiring / placement tables (Markdown) used in the build pages.

Only the Python standard library is needed.  Run via make_all.py.
"""
import re, html, math, collections

FONT = "DejaVu Sans, Verdana, Arial, sans-serif"
MONO = "DejaVu Sans Mono, Consolas, monospace"

# ----------------------------------------------------------------------------
# 1. Circuit description
# ----------------------------------------------------------------------------
class IC:
    def __init__(self, ref, part, npins, width, pins, notes="", connector=False, named_only=False):
        self.connector, self.named_only = connector, named_only
        self.ref, self.part, self.npins, self.width = ref, part, npins, width   # width: 'skinny'|'wide'
        self.pins = pins        # {pin_number: "NAME"}   (names for the pins we use)
        self.notes = notes
        self.at = (0, 0)        # schematic position
        self.sides = {}         # pin -> 'L'|'R' on the schematic

class Chain:
    def __init__(self, start, elems, build, side=None, until=99):
        self.start, self.elems, self.build, self.side, self.until = start, elems, build, side, until

class Circuit:
    """elems are strings:  'R:R2:680R'  'LED:D1:red'  'C:C1:100nF'  'SW:SW1:MODE'
       'PIEZO:BZ1'  and a terminal:  'GND' | '+5V' | 'NET:SCL' """
    def __init__(self, title):
        self.title = title
        self.supply_label = "+5 V"      # text shown for the +5V net (set "+3.3 V" for a 3.3 V month)
        self.ics = {}
        self.chains = []
        self.parts = {}         # ref -> (kind, value)

    def ic(self, ref, part, npins, width, pins, at=(0, 0), sides=None, notes="", connector=False, named_only=False):
        i = IC(ref, part, npins, width, pins, notes, connector, named_only); i.at = at; i.sides = sides or {}
        self.ics[ref] = i
        return i

    def chain(self, start, elems, build, side=None, until=99):
        """start = (ic_ref, pin) or ('NET', name)."""
        self.chains.append(Chain(start, elems, build, side, until))
        for e in elems:
            k = e.split(":")
            if k[0] in ("R", "LED", "C", "SW", "PIEZO", "XTAL", "POT"):
                self.parts[k[1]] = (k[0], k[2] if len(k) > 2 else "")

    # ---- netlist --------------------------------------------------------
    def netlist(self, upto):
        """-> {netname: set((ref, pin))}.  Only chains with build <= upto."""
        parent = {}
        def f(x):
            parent.setdefault(x, x)
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        def u(a, b): parent[f(a)] = f(b)
        for ci, ch in enumerate(self.chains):
            if ch.build > upto or ch.until < upto: continue
            cur = ("pin",) + tuple(ch.start) if ch.start[0] != "NET" else ("net", ch.start[1])
            f(cur)
            n = 0
            for e in ch.elems:
                k = e.split(":")
                if k[0] == "WIPER":
                    u(cur, ("pin", k[1], "W")); continue
                if k[0] in ("R", "C", "PIEZO", "SW", "LED", "XTAL", "POT"):
                    p1, p2 = (("A", "K") if k[0] == "LED" else ("1", "2"))
                    nxt = ("int", ci, n); n += 1
                    u(cur, ("pin", k[1], p1)); u(nxt, ("pin", k[1], p2)); cur = nxt
                elif k[0] == "GND": u(cur, ("net", "GND"))
                elif k[0] == "+5V": u(cur, ("net", "+5V"))
                elif k[0] == "NET": u(cur, ("net", k[1]))
        groups = collections.defaultdict(set)
        for x in list(parent):
            groups[f(x)].add(x)
        nets = {}
        for g in groups.values():
            pins = {(x[1], x[2]) for x in g if x[0] == "pin"}
            names = [x[1] for x in g if x[0] == "net"]
            if len(pins) + len(names) < 2 and not names: continue
            name = names[0] if names else "/".join(sorted(f"{a}.{b}" for a, b in pins))
            if names and len(names) > 1: name = sorted(names, key=lambda s: (s not in ("GND", "+5V"), s))[0]
            nets.setdefault(name, set()).update(pins)
        return nets

    def all_pins(self, upto):
        """every (ref,pin) that exists in the circuit up to this build."""
        pins = set()
        for ch in self.chains:
            if ch.build > upto or ch.until < upto: continue
            if ch.start[0] != "NET": pins.add(tuple(ch.start))
            for e in ch.elems:
                k = e.split(":")
                if k[0] in ("R", "C", "PIEZO", "SW", "XTAL", "POT"): pins |= {(k[1], "1"), (k[1], "2")}
                if k[0] == "WIPER": pins.add((k[1], "W"))
                if k[0] == "LED": pins |= {(k[1], "A"), (k[1], "K")}
        return pins


# ----------------------------------------------------------------------------
# 2. Breadboard model + verification
# ----------------------------------------------------------------------------
ROWS_TOP, ROWS_BOT = "abcde", "fghij"
RAILS = {"TP": "+5V", "TN": "GND", "BN": "GND", "BP": "+5V"}
RAIL_SPLIT = 31      # columns <= 31 are the 'left' rail segment; many boards have a break here

def parse_hole(s):
    m = re.match(r"^(TP|TN|BN|BP)(\d+)$", s)
    if m: return (int(m.group(2)), m.group(1))
    m = re.match(r"^(\d+)([a-j])$", s)
    if m: return (int(m.group(1)), m.group(2))
    raise ValueError("bad hole " + s)

def hole_node(h):
    col, row = h
    if row in RAILS: return ("rail", row, 0 if col <= RAIL_SPLIT else 1)
    return ("strip", col, "T" if row in ROWS_TOP else "B")

class Board:
    """Placements.  Every item has a 'build' number: the build in which you add it."""
    def __init__(self, circuit):
        self.c = circuit
        self.items = []     # dicts

    def ic(self, ref, col, build, rows=None):
        ic = self.c.ics[ref]
        rows = rows or (("e", "f") if ic.width == "skinny" else ("d", "h"))
        self.items.append(dict(kind="ic", ref=ref, col=col, rows=rows, build=build))

    def two(self, ref, a, b, build, **kw):
        """a resistor, capacitor, LED (a=anode,b=cathode) or piezo between two holes."""
        kind = self.c.parts[ref][0]
        self.items.append(dict(kind=kind, ref=ref, a=parse_hole(a), b=parse_hole(b), build=build, **kw))

    def wire(self, a, b, build, label="", until=99, **kw):
        self.items.append(dict(kind="wire", a=parse_hole(a), b=parse_hole(b), build=build, label=label, until=until, **kw))

    def pot(self, ref, a, w, b, build):
        """Potentiometer: a and b are the outer legs (the track ends), w the middle leg (wiper)."""
        self.items.append(dict(kind="POT", ref=ref, a=parse_hole(a), w=parse_hole(w), b=parse_hole(b), build=build))

    def switch(self, ref, col, build):
        """Tact switch straddling the centre gap: legs at (col,e) (col+2,e) (col,f) (col+2,f).
        Only the diagonal legs (col,e) and (col+2,f) are used, whichever way round the switch is."""
        self.items.append(dict(kind="SW", ref=ref, col=col, build=build))

    def lead(self, conn, pin, hole, build, label, until=99):
        """A lead from a hole to pin <pin> of an off-board connector (programmer, USB-serial adapter...)."""
        self.items.append(dict(kind="lead", conn=conn, pin=str(pin), a=parse_hole(hole), build=build, label=label, until=until))

    # ---- IC geometry ------------------------------------------------------
    def ic_pin_hole(self, ref, pin):
        for it in self.items:
            if it["kind"] == "ic" and it["ref"] == ref:
                ic = self.c.ics[ref]; half = ic.npins // 2
                top, bot = it["rows"]
                if pin <= half: return (it["col"] + pin - 1, bot)
                return (it["col"] + (ic.npins - pin), top)
        raise KeyError(ref)

    # ---- connectivity -----------------------------------------------------
    def classes(self, upto):
        parent = {}
        def f(x):
            parent.setdefault(x, x)
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        def u(a, b): parent[f(a)] = f(b)
        used_holes = collections.defaultdict(list)
        for it in self.items:
            if it["build"] > upto or it.get("until", 99) < upto: continue
            k = it["kind"]
            if k == "ic":
                ic = self.c.ics[it["ref"]]
                for p in range(1, ic.npins + 1):
                    h = self.ic_pin_hole(it["ref"], p)
                    u(("pin", it["ref"], p), hole_node(h)); used_holes[hole_node(h)].append((it["ref"], p))
            elif k in ("R", "C", "PIEZO", "XTAL"):
                u(("pin", it["ref"], "1"), hole_node(it["a"])); u(("pin", it["ref"], "2"), hole_node(it["b"]))
            elif k == "LED":
                u(("pin", it["ref"], "A"), hole_node(it["a"])); u(("pin", it["ref"], "K"), hole_node(it["b"]))
            elif k == "POT":
                u(("pin", it["ref"], "1"), hole_node(it["a"])); u(("pin", it["ref"], "W"), hole_node(it["w"]))
                u(("pin", it["ref"], "2"), hole_node(it["b"]))
            elif k == "wire":
                u(hole_node(it["a"]), hole_node(it["b"]))
            elif k == "lead":
                u(("pin", it["conn"], int(it["pin"])), hole_node(it["a"]))
            elif k == "SW":
                col = it["col"]
                # schematic pin 1 = the signal side (bottom-right leg), pin 2 = the GND side (top-left leg)
                u(("pin", it["ref"], "2"), hole_node((col, "e")))
                u(("pin", it["ref"], "1"), hole_node((col + 2, "f")))
        # the supply feeds the LEFT end of the top rails
        u(("net", "+5V"), ("rail", "TP", 0)); u(("net", "GND"), ("rail", "TN", 0))
        groups = collections.defaultdict(set)
        for x in list(parent): groups[f(x)].add(x)
        return groups, f

    def reserved_strips(self, upto):
        """strips occupied by the unused legs of a switch: must stay empty."""
        res = set()
        for it in self.items:
            if it["kind"] == "SW" and it["build"] <= upto <= it.get("until", 99):
                res.add(("strip", it["col"], "B")); res.add(("strip", it["col"] + 2, "T"))
        return res

    def verify(self, upto):
        """Return a list of problems (empty list = breadboard matches schematic)."""
        problems = []
        nets = self.c.netlist(upto)
        groups, f = self.classes(upto)
        # which pins exist physically up to this build
        placed_ics = {it["ref"] for it in self.items if it["kind"] == "ic" and it["build"] <= upto} | {r for r, i in self.c.ics.items() if i.connector}
        want_pins = {p for p in self.c.all_pins(upto)}
        # expected: each net's pins share one class (named nets also join the supply nets)
        pin_class = {}
        for g in groups.values():
            fg = f(next(iter(g)))
            for x in g:
                if x[0] == "pin": pin_class[(x[1], x[2])] = fg
        net_class = {}
        for name, pins in nets.items():
            pins = {p for p in pins if p[0] in placed_ics or p[0] not in self.c.ics}
            cls = set()
            for p in pins:
                p2 = (p[0], int(p[1]) if p[0] in self.c.ics else p[1])
                if p2 not in pin_class:
                    problems.append(f"{p[0]} pin {p[1]} (net {name}) is not placed on the breadboard"); continue
                cls.add(pin_class[p2])
            if name in ("GND", "+5V"): cls.add(f(("net", name)))
            if len(cls) > 1:
                problems.append(f"net {name}: its pins are NOT all connected on the breadboard")
            for c_ in cls: net_class.setdefault(c_, set()).add(name)
        # no two different nets in one class; no stray pins in a class
        for c_, names in net_class.items():
            if len(names) > 1: problems.append(f"SHORT: nets {sorted(names)} are connected together on the breadboard")
        # any class that holds pins but belongs to no net -> stray connection
        for g in groups.values():
            pins = [x for x in g if x[0] == "pin"]
            gc = f(next(iter(g)))
            if len(pins) > 1 and gc not in net_class:
                problems.append("stray connection between " + ", ".join(f"{a[1]}.{a[2]}" for a in pins[:6]))
        # reserved switch strips must be empty
        for r in self.reserved_strips(upto):
            for g in groups.values():
                if r in g and len([x for x in g if x[0] == "pin" and x[1] not in ("SW1", "SW2", "SW3", "SW4")]) > 0:
                    problems.append(f"something is plugged into a reserved switch-leg strip {r}")
        return problems

    # ---- tables -------------------------------------------------------------
    def place_text(self, it):
        def hs(h):
            col, row = h
            if row in RAILS:
                return f"**{ {'TP':'top red (+) rail','TN':'top blue (−) rail','BN':'bottom blue (−) rail','BP':'bottom red (+) rail'}[row] }**, near column {col}"
            return f"**{col}{row}**"
        return hs(it)


# ----------------------------------------------------------------------------
# 3. SVG helpers
# ----------------------------------------------------------------------------
def esc(s): return html.escape(str(s), quote=True)

NET_COLORS = ["#d62728", "#1f77b4", "#2ca02c", "#9467bd", "#ff7f0e", "#8c564b", "#e377c2", "#17becf", "#bcbd22", "#7f7f7f"]
def wire_color(label):
    if label in ("+5V", "5V"): return "#d62728"
    if label == "GND": return "#222222"
    h = sum(ord(c) for c in label) if label else 0
    pal = ["#1f77b4", "#2ca02c", "#9467bd", "#ff7f0e", "#8c564b", "#e377c2", "#17becf", "#bcbd22"]
    return pal[h % len(pal)]


# ---------------- breadboard drawing ----------------
P = 18.0                 # pixels per 0.1 inch
ROWY = {"TP": 0, "TN": 1, "a": 3.0, "b": 4.0, "c": 5.0, "d": 6.0, "e": 7.0,
        "f": 10.0, "g": 11.0, "h": 12.0, "i": 13.0, "j": 14.0, "BN": 16.0, "BP": 17.0}

class BBDraw:
    def __init__(self, board, upto, title, cmin=None, cmax=None):
        self.b, self.upto, self.title = board, upto, title
        cols = []
        for it in board.items:
            if it["build"] > upto: continue
            if it["kind"] == "ic":
                ic = board.c.ics[it["ref"]]; cols += [it["col"], it["col"] + ic.npins // 2 - 1]
            elif it["kind"] == "SW": cols += [it["col"], it["col"] + 2]
            else:
                for k in ("a", "b", "w"):
                    if k in it: cols.append(it[k][0])
        # always show the same crop for every build of a month so pictures line up
        allcols = []
        for it in board.items:
            if it["kind"] == "ic":
                ic = board.c.ics[it["ref"]]; allcols += [it["col"], it["col"] + ic.npins // 2 - 1]
            elif it["kind"] == "SW": allcols += [it["col"], it["col"] + 2]
            else:
                for k in ("a", "b", "w"):
                    if k in it: allcols.append(it[k][0])
        self.cmin = cmin if cmin is not None else max(1, min(allcols) - 3)
        self.cmax = cmax if cmax is not None else min(63, max(allcols) + 3)
        self.X0 = 190.0; self.Y0 = 70.0

    def xy(self, h):
        col, row = h
        return (self.X0 + (col - self.cmin) * P, self.Y0 + ROWY[row] * P)

    def render(self):
        b, upto = self.b, self.upto
        W = self.X0 + (self.cmax - self.cmin + 1) * P + 40
        H = self.Y0 + 19 * P + 44
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" font-family="{FONT}">']
        o.append(f'<rect width="100%" height="100%" fill="#ffffff"/>')
        o.append(f'<text x="14" y="26" font-size="17" font-weight="bold" fill="#111">{esc(self.title)}</text>')
        o.append(f'<text x="14" y="46" font-size="11.5" fill="#444">Breadboard layout. Yellow glow = parts to add in THIS build. Hole names such as 13j mean column 13, row j.</text>')
        bx0 = self.X0 - 38; bx1 = self.X0 + (self.cmax - self.cmin) * P + 16
        by0 = self.Y0 - 22; by1 = self.Y0 + 17 * P + 22
        o.append(f'<rect x="{bx0}" y="{by0}" width="{bx1-bx0}" height="{by1-by0}" rx="6" fill="#f4efe6" stroke="#b9b09f" stroke-width="1.5"/>')
        # centre channel
        cy0 = self.Y0 + 7 * P + 5; cy1 = self.Y0 + 10 * P - 5
        o.append(f'<rect x="{bx0}" y="{cy0}" width="{bx1-bx0}" height="{cy1-cy0}" fill="#d9d2c2"/>')
        # rail colour stripes
        for rname, colr in (("TP", "#d62728"), ("TN", "#1f5fbf"), ("BN", "#1f5fbf"), ("BP", "#d62728")):
            y = self.Y0 + ROWY[rname] * P
            o.append(f'<line x1="{bx0+6}" y1="{y-8.5}" x2="{bx1-6}" y2="{y-8.5}" stroke="{colr}" stroke-width="1.3" opacity=".7"/>')
            sym = "+" if rname in ("TP", "BP") else "−"
            o.append(f'<text x="{bx0+14}" y="{y+4}" font-size="11" font-weight="bold" fill="{colr}">{sym}</text>')
        # holes
        for col in range(self.cmin, self.cmax + 1):
            for row in ROWS_TOP + ROWS_BOT:
                x, y = self.xy((col, row))
                o.append(f'<rect x="{x-2.2:.1f}" y="{y-2.2:.1f}" width="4.4" height="4.4" fill="#5b5547"/>')
            for r in RAILS:
                if col % 6 == 0: continue
                x, y = self.xy((col, r))
                o.append(f'<rect x="{x-2.2:.1f}" y="{y-2.2:.1f}" width="4.4" height="4.4" fill="#5b5547"/>')
        # row letters & column numbers
        for row in ROWS_TOP + ROWS_BOT:
            y = self.xy((self.cmin, row))[1]
            o.append(f'<text x="{bx0+24}" y="{y+3.5}" font-size="9.5" fill="#7a725f" text-anchor="middle">{row}</text>')
        for col in range(self.cmin, self.cmax + 1):
            if col % 5 == 0 or col == self.cmin:
                x = self.xy((col, "a"))[0]
                o.append(f'<text x="{x}" y="{self.Y0+2.05*P}" font-size="9" fill="#7a725f" text-anchor="middle">{col}</text>')
                o.append(f'<text x="{x}" y="{self.Y0+15.15*P}" font-size="9" fill="#7a725f" text-anchor="middle">{col}</text>')
        # items (draw order: ICs, flat parts, switches, wires, leads)
        order = {"ic": 0, "R": 1, "C": 1, "LED": 1, "PIEZO": 1, "XTAL": 1, "POT": 1, "SW": 2, "wire": 3, "lead": 4}
        wi = 0
        self.labels = []
        self.lead_idx = 0
        for it in sorted([i for i in b.items if i["build"] <= upto <= i.get("until", 99)], key=lambda i: order[i["kind"]]):
            new = it["build"] == upto
            k = it["kind"]
            if k == "ic": o.append(self.draw_ic(it, new))
            elif k in ("R", "C", "LED", "PIEZO", "XTAL"): o.append(self.draw_part(it, new))
            elif k == "POT": o.append(self.draw_pot(it, new))
            elif k == "SW": o.append(self.draw_switch(it, new))
            elif k == "wire": o.append(self.draw_wire(it, new, wi)); wi += 1
            elif k == "lead": o.append(self.draw_lead(it, new))
        o.extend(self.labels)
        o.append("</svg>")
        return "\n".join(o)

    # -- items
    def draw_ic(self, it, new):
        ic = self.b.c.ics[it["ref"]]; half = ic.npins // 2
        top, bot = it["rows"]
        x0, yt = self.xy((it["col"], top)); x1, yb = self.xy((it["col"] + half - 1, bot))
        s = []
        if new: s.append(f'<rect x="{x0-10}" y="{yt-6}" width="{x1-x0+20}" height="{yb-yt+12}" rx="6" fill="#ffe34d" opacity=".6"/>')
        s.append(f'<rect x="{x0-6}" y="{yt+4}" width="{x1-x0+12}" height="{yb-yt-8}" rx="3" fill="#2b2b2b" stroke="#000"/>')
        s.append(f'<path d="M {x0-6} {(yt+yb)/2-6} a 6 6 0 0 1 0 12" fill="#f4efe6" stroke="#000"/>')
        wide_body = (x1 - x0) > 210
        if wide_body:
            s.append(f'<text x="{(x0+x1)/2}" y="{(yt+yb)/2-3}" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">{esc(ic.ref)}  {esc(ic.part)}</text>')
            s.append(f'<text x="{(x0+x1)/2}" y="{(yt+yb)/2+12}" font-size="10" fill="#ddd" text-anchor="middle">notch ◖ at the LEFT; pin 1 is bottom-left</text>')
        else:   # narrow chip: shorter text so it stays inside the body
            short = ic.part.split("-")[0]
            s.append(f'<text x="{(x0+x1)/2}" y="{(yt+yb)/2-1}" font-size="9.5" font-weight="bold" fill="#fff" text-anchor="middle">{esc(ic.ref)} {esc(short)}</text>')
            s.append(f'<text x="{(x0+x1)/2}" y="{(yt+yb)/2+11}" font-size="8" fill="#ddd" text-anchor="middle">pin 1 bottom-left</text>')
        for p in range(1, ic.npins + 1):
            h = self.b.ic_pin_hole(ic.ref, p); x, y = self.xy(h)
            s.append(f'<rect x="{x-3.4}" y="{y-3.4}" width="6.8" height="6.8" fill="#cfcfcf" stroke="#555" stroke-width=".6"/>')
            ty = y + (13 if y < (yt + yb) / 2 else -7)
            col = "#ffe34d" if p in ic.pins else "#9a9a9a"
            s.append(f'<text x="{x}" y="{ty}" font-size="8.5" fill="{col}" text-anchor="middle">{p}</text>')
        return "\n".join(s)

    def draw_part(self, it, new):
        (xa, ya), (xb, yb) = self.xy(it["a"]), self.xy(it["b"])
        mx, my = (xa + xb) / 2, (ya + yb) / 2
        L = math.hypot(xb - xa, yb - ya) or 1
        ang = math.degrees(math.atan2(yb - ya, xb - xa))
        vertical = abs(xa - xb) < 1
        ref, k = it["ref"], it["kind"]
        val = self.b.c.parts[ref][1]
        s = []
        if new: s.append(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="#ffe34d" stroke-width="22" stroke-linecap="round" opacity=".6"/>')
        s.append(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="#9aa0a6" stroke-width="2"/>')
        if k == "R":
            bl = min(L - 6, 34)
            if vertical:
                s.append(f'<g transform="translate({mx},{my})"><rect x="-6" y="{-bl/2}" width="12" height="{bl}" rx="4" fill="#d9b779" stroke="#6b5a2d"/>'
                         f'<text transform="rotate(-90)" x="0" y="3" font-size="8.5" font-weight="bold" fill="#3b2a00" text-anchor="middle">{esc(ref)}</text></g>')
            else:
                s.append(f'<g transform="translate({mx},{my}) rotate({ang})"><rect x="{-bl/2}" y="-5.5" width="{bl}" height="11" rx="4" fill="#d9b779" stroke="#6b5a2d"/>'
                         f'<text x="0" y="3" font-size="8.5" font-weight="bold" fill="#3b2a00" text-anchor="middle">{esc(ref)}</text></g>')
                s.append(f'<text x="{mx}" y="{my-10}" font-size="9" fill="#222" text-anchor="middle">{esc(pretty_ohms(val))}</text>')
        elif k == "LED":
            s.append(f'<circle cx="{mx}" cy="{my}" r="8.6" fill="#d32f2f" stroke="#7a1010"/>')
            s.append(f'<text x="{mx}" y="{my+3}" font-size="8.5" font-weight="bold" fill="#fff" text-anchor="middle">{esc(ref)}</text>')
            # mark the anode (long leg) with a red + beside its hole
            s.append(f'<text x="{xa+6}" y="{ya-4}" font-size="11" font-weight="bold" fill="#c00" stroke="#fff" stroke-width="2.4" paint-order="stroke">+</text>')
        elif k == "XTAL":
            s.append(f'<g transform="translate({mx},{my}) rotate({ang if not vertical else 90})"><rect x="-14" y="-6" width="28" height="12" rx="6" fill="#c9ced4" stroke="#555"/>'
                     f'<text x="0" y="3" font-size="7.5" font-weight="bold" fill="#222" text-anchor="middle">{esc(ref)}</text></g>')
            s.append(f'<text x="{mx}" y="{my-10}" font-size="9" fill="#222" text-anchor="middle">{esc(val)}</text>')
        elif k == "C":
            s.append(f'<ellipse cx="{mx}" cy="{my}" rx="7" ry="8" fill="#f2c94c" stroke="#8a6d00"/>')
            s.append(f'<text x="{mx}" y="{my+19}" font-size="9" fill="#222" text-anchor="middle">{esc(ref)} {esc(val)}</text>')
        else:  # piezo
            s.append(f'<circle cx="{mx}" cy="{my}" r="9" fill="#d4af37" stroke="#7a6310"/>')
            s.append(f'<text x="{mx}" y="{my+3}" font-size="8" font-weight="bold" fill="#4a3b00" text-anchor="middle">BZ</text>')
        for (x, y) in ((xa, ya), (xb, yb)):
            s.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#555"/>')
        return "\n".join(s)

    def draw_pot(self, it, new):
        (xa, ya), (xw, yw), (xb, yb) = self.xy(it["a"]), self.xy(it["w"]), self.xy(it["b"])
        s = []
        if new: s.append(f'<rect x="{xa-13}" y="{ya-6}" width="{xb-xa+26}" height="{(yb-ya)+ (46 if ya < self.Y0 + 8*P else -46)}" rx="8" fill="#ffe34d" opacity=".6"/>' if False else f'<rect x="{xa-14}" y="{ya-48}" width="{xb-xa+28}" height="60" rx="8" fill="#ffe34d" opacity=".6"/>')
        s.append(f'<rect x="{xa-10}" y="{ya-42}" width="{xb-xa+20}" height="48" rx="6" fill="#2d6cdf" stroke="#12347a" stroke-width="1.5"/>')
        s.append(f'<circle cx="{xw}" cy="{ya-20}" r="14" fill="#cfd6e4" stroke="#12347a"/><line x1="{xw}" y1="{ya-20}" x2="{xw+8}" y2="{ya-28}" stroke="#12347a" stroke-width="2.5"/>')
        s.append(f'<text x="{xw}" y="{ya-45}" font-size="9" fill="#12347a" text-anchor="middle">{esc(it["ref"])} {esc(pretty_ohms(self.b.c.parts[it["ref"]][1]))} pot</text>')
        for (x, y, lab) in ((xa, ya, "end"), (xw, yw, "wiper"), (xb, yb, "end")):
            s.append(f'<circle cx="{x}" cy="{y}" r="2.8" fill="#555"/>')
        return "\n".join(s)

    def draw_switch(self, it, new):
        col = it["col"]
        x0, y0 = self.xy((col, "e")); x1, y1 = self.xy((col + 2, "f"))
        s = []
        if new: s.append(f'<rect x="{x0-12}" y="{y0-12}" width="{x1-x0+24}" height="{y1-y0+24}" rx="6" fill="#ffe34d" opacity=".6"/>')
        s.append(f'<rect x="{x0-6}" y="{y0-5}" width="{x1-x0+12}" height="{y1-y0+10}" rx="3" fill="#6d6d72" stroke="#222"/>')
        s.append(f'<circle cx="{(x0+x1)/2}" cy="{(y0+y1)/2}" r="9" fill="#2a2a2e" stroke="#000"/>')
        s.append(f'<text x="{(x0+x1)/2}" y="{(y0+y1)/2+3.5}" font-size="8" fill="#fff" text-anchor="middle">{esc(it["ref"])}</text>')
        for (x, y, used) in ((x0, y0, 1), (x1, y1, 1), (x1, y0, 0), (x0, y1, 0)):
            s.append(f'<rect x="{x-3.4}" y="{y-3.4}" width="6.8" height="6.8" fill="{"#cfcfcf" if used else "#9a9a9a"}" stroke="#333" stroke-width=".6"/>')
            if not used: s.append(f'<text x="{x}" y="{y+3}" font-size="7" fill="#c00" text-anchor="middle">×</text>')
        return "\n".join(s)

    def draw_wire(self, it, new, idx):
        (xa, ya), (xb, yb) = self.xy(it["a"]), self.xy(it["b"])
        col = wire_color(it.get("label", ""))
        mid_y = self.Y0 + 8.5 * P
        L = math.hypot(xb - xa, yb - ya)
        arch = min(46, 10 + 0.18 * L) + (idx % 4) * 3
        up = ((ya + yb) / 2) < mid_y
        sgn = -1 if up else 1
        if abs(xa - xb) < 1:   # vertical: bow sideways
            cx1, cy1, cx2, cy2 = xa + 14 * (1 if idx % 2 else -1), ya + (yb - ya) * .3, xb + 14 * (1 if idx % 2 else -1), ya + (yb - ya) * .7
        else:
            cx1, cy1 = xa + (xb - xa) * .2, ya + sgn * arch
            cx2, cy2 = xa + (xb - xa) * .8, yb + sgn * arch
        d = f"M {xa:.1f} {ya:.1f} C {cx1:.1f} {cy1:.1f}, {cx2:.1f} {cy2:.1f}, {xb:.1f} {yb:.1f}"
        s = []
        if new: s.append(f'<path d="{d}" fill="none" stroke="#ffe34d" stroke-width="8" stroke-linecap="round" opacity=".7"/>')
        s.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="3.2" stroke-linecap="round"/>')
        s.append(f'<circle cx="{xa}" cy="{ya}" r="3" fill="{col}" stroke="#fff" stroke-width=".8"/><circle cx="{xb}" cy="{yb}" r="3" fill="{col}" stroke="#fff" stroke-width=".8"/>')
        lab = it.get("label", "")
        if lab and lab not in ("+5V", "GND"):
            ends = sorted([(ya, xa, it["a"]), (yb, xb, it["b"])])
            ty0, tx0, hole = ends[0]
            if hole[1] in ROWS_TOP:
                self.labels.append(f'<text transform="translate({tx0:.1f},{ty0-8:.1f}) rotate(-90)" font-size="8.5" font-weight="bold" fill="{col}" stroke="#fff" stroke-width="2.6" paint-order="stroke">{esc(lab)}</text>')
            else:
                tx, ty = (cx1 + cx2) / 2, (cy1 + cy2) / 2 * 0.75 + (ya + yb) / 2 * 0.25
                self.labels.append(f'<text x="{tx:.1f}" y="{ty-3:.1f}" font-size="9.5" font-weight="bold" fill="{col}" text-anchor="middle" stroke="#fff" stroke-width="2.6" paint-order="stroke">{esc(lab)}</text>')
        return "\n".join(s)

    def draw_lead(self, it, new):
        xa, ya = self.xy(it["a"])
        conn = self.b.c.ics[it["conn"]]
        self.lead_idx += 1
        bx = 10.0; bw = 140.0
        yy = self.Y0 + (0.6 + self.lead_idx * 1.45) * P
        xe = bx + bw
        d = f"M {xa:.1f} {ya:.1f} C {xa-60:.1f} {ya:.1f}, {xe+60:.1f} {yy:.1f}, {xe:.1f} {yy:.1f}"
        txt = f"{conn.part}: {it['label']}" if conn.named_only else f"{conn.part} pin {it['pin']}  {it['label']}"
        s = []
        if new: s.append(f'<path d="{d}" fill="none" stroke="#ffe34d" stroke-width="8" stroke-linecap="round" opacity=".7"/>')
        s.append(f'<path d="{d}" fill="none" stroke="#7a3fb0" stroke-width="2.4" stroke-dasharray="6 3" stroke-linecap="round"/>')
        s.append(f'<circle cx="{xa}" cy="{ya}" r="3" fill="#7a3fb0"/>')
        s.append(f'<rect x="{bx}" y="{yy-9}" width="{bw}" height="18" rx="3" fill="#efe4fa" stroke="#7a3fb0"/>'
                 f'<text x="{bx+bw/2}" y="{yy+4}" font-size="9.5" fill="#4a1f78" text-anchor="middle">{esc(txt)}</text>')
        return "\n".join(s)


# ----------------------------------------------------------------------------
# 4. Schematic drawing
# ----------------------------------------------------------------------------
ROWP = 46     # vertical pitch of pins on the schematic

class SchDraw:
    def __init__(self, circuit, upto, title, size=None):
        self.c, self.upto, self.title, self.size = circuit, upto, title, size

    def render(self):
        c, upto = self.c, self.upto
        o = []
        maxx = maxy = 0
        # --- ICs
        boxes = {}
        for ref, ic in c.ics.items():
            pins = sorted(p for p in {ch.start[1] for ch in c.chains if ch.start[0] == ref})
            left = [p for p in pins if ic.sides.get(p, "L") == "L"]
            right = [p for p in pins if ic.sides.get(p, "L") == "R"]
            n = max(len(left), len(right), 1)
            w = max(150, int(8.4 * len(ref + '  ' + ic.part)) + 24); h = n * ROWP + 34
            x, y = ic.at
            boxes[ref] = (x, y, w, h, left, right)
            maxx = max(maxx, x + w + 300); maxy = max(maxy, y + h + 40)
        for ref, (x, y, w, h, left, right) in boxes.items():
            ic = c.ics[ref]
            if ic.connector and not any(ch.start[0] == ref and ch.build <= self.upto <= ch.until for ch in c.chains):
                continue      # a connector that is not plugged in during this build is not drawn
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f6f8fb" stroke="#1d3557" stroke-width="2"/>')
            o.append(f'<text x="{x+w/2}" y="{y+17}" font-size="13" font-weight="bold" fill="#1d3557" text-anchor="middle">{esc(ref)}  {esc(ic.part)}</text>')
            for side, plist in (("L", left), ("R", right)):
                for i, p in enumerate(plist):
                    py = y + 34 + i * ROWP + 8
                    nm = ic.pins.get(p, "")
                    pnum = "" if ic.named_only else p
                    chains = [ch for ch in c.chains if ch.start == (ref, p)]
                    shown = [ch for ch in chains if ch.build <= self.upto <= ch.until]
                    fade = "" if shown else ' opacity=".28"'
                    if side == "L":
                        o.append(f'<text x="{x+8}" y="{py+4}" font-size="11" fill="#111"{fade}><tspan font-weight="bold">{pnum}</tspan>  {esc(nm)}</text>')
                    else:
                        o.append(f'<text x="{x+w-8}" y="{py+4}" font-size="11" fill="#111" text-anchor="end"{fade}>{esc(nm)}  <tspan font-weight="bold">{pnum}</tspan></text>')
                    for ch in shown:
                        sx = x if side == "L" else x + w
                        o.append(self.draw_chain(sx, py, -1 if side == "L" else 1, ch))
        # --- free chains (start from a named net) in a panel below
        free = [ch for ch in c.chains if ch.start[0] == "NET" and ch.build <= upto <= ch.until]
        fx0 = 40; fy0 = maxy + 10
        if free:
            o.append(f'<text x="{fx0}" y="{fy0}" font-size="12" font-weight="bold" fill="#444">Parts hanging on a net (same net name = same wire)</text>')
            for i, ch in enumerate(free):
                col, row = i % 2, i // 2
                x = fx0 + 120 + col * 430; y = fy0 + 44 + row * 66
                o.append(self.draw_chain(x, y, 1, ch, start_label=True))
            maxy = fy0 + 44 + ((len(free) + 1) // 2) * 66 + 10
        W = max(maxx, 760); H = maxy + 20
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H+34}" width="{W}" height="{H+34}" font-family="{FONT}">',
               '<rect width="100%" height="100%" fill="#fff"/>',
               f'<text x="14" y="24" font-size="17" font-weight="bold" fill="#111">{esc(self.title)}</text>',
               f'<g transform="translate(0,34)">'] + o + ['</g></svg>']
        return "\n".join(out)

    # a chain drawn horizontally; d = +1 to the right, -1 to the left
    def draw_chain(self, x, y, d, ch, start_label=False):
        new = ch.build == self.upto
        col = "#0a7a2f" if new else "#222"
        s = []
        cur = x
        if start_label:
            nm = ch.start[1]
            s.append(self.flag(cur - 6, y, -1, nm, col))
            s.append(f'<line x1="{cur-6}" y1="{y}" x2="{cur}" y2="{y}" stroke="{col}" stroke-width="1.8"/>')
        for e in ch.elems:
            k = e.split(":")
            if k[0] == "WIPER":
                s.append(f'<line x1="{cur}" y1="{y}" x2="{cur+d*14}" y2="{y}" stroke="{col}" stroke-width="1.8"/>')
                s.append(f'<text x="{cur+d*18}" y="{y+4}" font-size="10" fill="{col}">wiper of {esc(k[1])}</text>')
                continue
            if k[0] in ("R", "C", "LED", "SW", "PIEZO", "XTAL", "POT"):
                s.append(f'<line x1="{cur}" y1="{y}" x2="{cur+d*14}" y2="{y}" stroke="{col}" stroke-width="1.8"/>')
                cur += d * 14
                s.append(self.symbol(k, cur, y, d, col, new))
                cur += d * 54
                s.append(f'<line x1="{cur-d*0}" y1="{y}" x2="{cur+d*12}" y2="{y}" stroke="{col}" stroke-width="1.8"/>')
                cur += d * 12
            elif k[0] == "GND":
                s.append(f'<line x1="{cur}" y1="{y}" x2="{cur+d*14}" y2="{y}" stroke="{col}" stroke-width="1.8"/>')
                s.append(self.gnd(cur + d * 14, y, col, d))
            elif k[0] == "+5V":
                s.append(f'<line x1="{cur}" y1="{y}" x2="{cur+d*14}" y2="{y}" stroke="{col}" stroke-width="1.8"/>')
                s.append(self.vcc(cur + d * 14, y, col))
            elif k[0] == "NET":
                s.append(f'<line x1="{cur}" y1="{y}" x2="{cur+d*14}" y2="{y}" stroke="{col}" stroke-width="1.8"/>')
                s.append(self.flag(cur + d * 14, y, d, k[1], col))
        return "\n".join(s)

    def symbol(self, k, x, y, d, col, new):
        kind, ref = k[0], k[1]; val = k[2] if len(k) > 2 else ""
        cx = x + d * 27
        s = []
        lab = f'<text x="{cx}" y="{y-12}" font-size="10" font-weight="bold" fill="{col}" text-anchor="middle">{esc(ref)}</text>'
        if kind == "R":
            s.append(f'<rect x="{cx-18}" y="{y-6}" width="36" height="12" fill="#fff" stroke="{col}" stroke-width="1.8"/>')
            s.append(lab + f'<text x="{cx}" y="{y+21}" font-size="10" fill="{col}" text-anchor="middle">{esc(pretty_ohms(val))}</text>')
        elif kind == "LED":
            # triangle pointing in the direction of current flow (away from the pin)
            tip = cx + d * 8; base = cx - d * 8
            s.append(f'<polygon points="{base},{y-9} {base},{y+9} {tip},{y}" fill="#fff" stroke="{col}" stroke-width="1.8"/>')
            s.append(f'<line x1="{tip}" y1="{y-9}" x2="{tip}" y2="{y+9}" stroke="{col}" stroke-width="1.8"/>')
            s.append(f'<path d="M {cx-2} {y-12} l 7 -7 m -3 0 h 3 v 3 M {cx+6} {y-9} l 7 -7 m -3 0 h 3 v 3" fill="none" stroke="{col}" stroke-width="1.1"/>')
            s.append(lab.replace(f'y="{y-12}"', f'y="{y-23}"') )
        elif kind == "POT":
            s.append(f'<rect x="{cx-18}" y="{y-6}" width="36" height="12" fill="#fff" stroke="{col}" stroke-width="1.8"/>')
            s.append(f'<path d="M {cx} {y-20} L {cx} {y-7} M {cx-4} {y-12} L {cx} {y-7} L {cx+4} {y-12}" fill="none" stroke="{col}" stroke-width="1.6"/>')
            s.append(lab.replace(f'y="{y-12}"', f'y="{y-24}"') + f'<text x="{cx}" y="{y+21}" font-size="10" fill="{col}" text-anchor="middle">{esc(pretty_ohms(val))} pot</text>')
        elif kind == "XTAL":
            s.append(f'<line x1="{cx-10}" y1="{y-11}" x2="{cx-10}" y2="{y+11}" stroke="{col}" stroke-width="2"/><line x1="{cx+10}" y1="{y-11}" x2="{cx+10}" y2="{y+11}" stroke="{col}" stroke-width="2"/>')
            s.append(f'<rect x="{cx-5}" y="{y-8}" width="10" height="16" fill="#fff" stroke="{col}" stroke-width="1.8"/>')
            s.append(lab + f'<text x="{cx}" y="{y+25}" font-size="10" fill="{col}" text-anchor="middle">{esc(val)}</text>')
        elif kind == "C":
            s.append(f'<line x1="{cx-4}" y1="{y-11}" x2="{cx-4}" y2="{y+11}" stroke="{col}" stroke-width="2"/><line x1="{cx+4}" y1="{y-11}" x2="{cx+4}" y2="{y+11}" stroke="{col}" stroke-width="2"/>')
            s.append(lab + f'<text x="{cx}" y="{y+25}" font-size="10" fill="{col}" text-anchor="middle">{esc(val)}</text>')
        elif kind == "SW":
            s.append(f'<circle cx="{cx-14}" cy="{y}" r="3" fill="#fff" stroke="{col}" stroke-width="1.6"/><circle cx="{cx+14}" cy="{y}" r="3" fill="#fff" stroke="{col}" stroke-width="1.6"/>')
            s.append(f'<line x1="{cx-14}" y1="{y-3}" x2="{cx+12}" y2="{y-13}" stroke="{col}" stroke-width="1.8"/>')
            s.append(lab + f'<text x="{cx}" y="{y+21}" font-size="10" fill="{col}" text-anchor="middle">{esc(val)} button</text>')
        elif kind == "PIEZO":
            s.append(f'<rect x="{cx-16}" y="{y-10}" width="32" height="20" rx="3" fill="#fff6d6" stroke="{col}" stroke-width="1.8"/>')
            s.append(f'<path d="M {cx-10} {y} q 3 -8 5 0 t 5 0 t 5 0" fill="none" stroke="{col}" stroke-width="1.4"/>')
            s.append(lab.replace(f'y="{y-12}"', f'y="{y-15}"') + f'<text x="{cx}" y="{y+24}" font-size="10" fill="{col}" text-anchor="middle">piezo</text>')
        return "\n".join(s)

    def gnd(self, x, y, col, d=1):
        return (f'<line x1="{x}" y1="{y-9}" x2="{x}" y2="{y+9}" stroke="{col}" stroke-width="1.8"/>' if False else
                f'<g stroke="{col}" stroke-width="1.8"><line x1="{x}" y1="{y}" x2="{x}" y2="{y+6}"/><line x1="{x-10}" y1="{y+6}" x2="{x+10}" y2="{y+6}"/><line x1="{x-6}" y1="{y+10}" x2="{x+6}" y2="{y+10}"/><line x1="{x-2.5}" y1="{y+14}" x2="{x+2.5}" y2="{y+14}"/></g>'
                f'<text x="{x+14*d}" y="{y+13}" font-size="9" fill="{col}" text-anchor="{"start" if d>0 else "end"}">GND</text>')

    def vcc(self, x, y, col):
        return (f'<g stroke="{col}" stroke-width="1.8"><line x1="{x}" y1="{y}" x2="{x}" y2="{y-8}"/><line x1="{x-9}" y1="{y-8}" x2="{x+9}" y2="{y-8}"/></g>'
                f'<text x="{x}" y="{y-12}" font-size="10" font-weight="bold" fill="#b00020" text-anchor="middle">{esc(self.c.supply_label)}</text>')

    def flag(self, x, y, d, name, col):
        w = 12 + 7.2 * len(name)
        if d > 0:
            pts = f"{x},{y} {x+8},{y-8} {x+w},{y-8} {x+w},{y+8} {x+8},{y+8}"; tx = x + 10 + (w - 10) / 2 - 1
        else:
            pts = f"{x},{y} {x-8},{y-8} {x-w},{y-8} {x-w},{y+8} {x-8},{y+8}"; tx = x - 10 - (w - 10) / 2 + 1
        return (f'<polygon points="{pts}" fill="#eef4ff" stroke="{col}" stroke-width="1.6"/>'
                f'<text x="{tx}" y="{y+4}" font-size="11" font-weight="bold" fill="#0b3d91" text-anchor="middle">{esc(name)}</text>')


# ----------------------------------------------------------------------------
# 5. Tables
# ----------------------------------------------------------------------------
def pin_table(circuit, board, build):
    """Markdown 'what connects to what' for the parts added in this build (chains)."""
    rows = []
    for ch in circuit.chains:
        if ch.build != build: continue
        if ch.start[0] == "NET": start = f"net **{ch.start[1]}**"
        else:
            ic = circuit.ics[ch.start[0]]
            start = f"{ic.ref} pin **{ch.start[1]}** ({ic.pins.get(ch.start[1], '')})"
        steps = []
        for e in ch.elems:
            k = e.split(":")
            if k[0] == "R": steps.append(f"{k[1]} {pretty_ohms(k[2])}")
            elif k[0] == "LED": steps.append(f"{k[1]} LED (long leg towards the resistor)")
            elif k[0] == "C": steps.append(f"{k[1]} {k[2]}")
            elif k[0] == "SW": steps.append(f"{k[1]} button")
            elif k[0] == "PIEZO": steps.append(f"{k[1]} piezo")
            elif k[0] == "GND": steps.append("**GND**")
            elif k[0] == "+5V": steps.append(f"**{circuit.supply_label}**")
            elif k[0] == "POT": steps.append(f"{k[1]} {k[2]} potentiometer (outer legs)")
            elif k[0] == "WIPER": steps.append(f"{k[1]} wiper (middle leg)")
            elif k[0] == "XTAL": steps.append(f"{k[1]} {k[2]} crystal")
            elif k[0] == "NET": steps.append(f"net **{k[1]}**")
        rows.append((start, " → ".join(steps)))
    return rows

def pretty_ohms(v):
    if v.endswith("R"): return v[:-1] + " Ω"
    if "k" in v:
        a, _, b = v.partition("k")
        return f"{a}.{b} kΩ" if b else f"{a} kΩ"
    return v
