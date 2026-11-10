#!/usr/bin/env python3
"""
make_purchasing.py - writes the course overview, the global purchasing plan, the parts catalogue and CSV files
from course_data.py plus the verified circuits for Months 1 to 5.

  start-here/course-overview.md
  start-here/purchasing-plan.md
  start-here/parts-catalogue.md
  start-here/purchasing-plan.csv        (spreadsheet: what to order, month by month)
  start-here/lab-stock-matrix.csv       (spreadsheet: lab stock needed, item by month)
"""
import os, math, csv, collections
from course_data import (CHIPS, STOCK, TOOLS, PLAN, PHASES, CAPSTONE_SHORTLIST, product_link, search_links, octopart_link)
from circuits import month1, month1_avr, month1_isp, month2, month3, month4, month5
from sync_docs import bom_counts
from format_tables import format_tree

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "start-here")
MONTH_DIRS = {1: "month-01-electronic-dice", 2: "month-02-workshop-command-centre", 3: "month-03-analogue-in-out",
              4: "month-04-binary-clock", 5: "month-05-sixteen-bit-and-memory"}

RES = {"100 Ω": "r100", "330 Ω": "r330", "680 Ω": "r680", "1 kΩ": "r1k", "4.7 kΩ": "r4k7", "10 kΩ": "r10k", "100 kΩ": "r100k", "120 Ω": "r120"}
CAP = {"10pF": "c10p", "22pF": "c22p", "100nF": "c100n", "1uF": "c1u", "10uF": "c10u", "100uF": "c100u"}
XT = {"16MHz": "xtal16m", "32.768kHz": "xtal32k", "8MHz": "xtal8m"}

def circuit_usage(fns):
    """Lab-stock quantities of the FINAL build of each circuit; the MAXIMUM across circuits (they reuse parts)."""
    out = collections.Counter()
    for fn in fns:
        c, b = fn()
        u = collections.Counter()
        for (k, v), n in bom_counts(c, b).items():
            if k == "Resistor": u[RES[v]] += n
            elif k == "Ceramic capacitor": u[CAP[v]] += n
            elif k == "Crystal": u[XT[v]] += n
            elif k.startswith("LED"): u["led"] += n
            elif k.startswith("Push button"): u["btn"] += n
            elif k.startswith("Piezo"): u["piezo"] += n
            elif k.startswith("Potentiometer"): u["pot10k"] += n
            elif k.startswith("Jumper"): u["wires"] += n
            elif k == "LEADS": u["dupont"] += n
        for kk, n in u.items(): out[kk] = max(out[kk], n)
    return dict(out)

def usage_by_month():
    u = {1: circuit_usage([month1, month1_avr, month1_isp]), 2: circuit_usage([month2]), 3: circuit_usage([month3]),
         4: circuit_usage([month4]), 5: circuit_usage([month5])}
    for m in PLAN:
        if m["n"] > 5: u[m["n"]] = dict(m["stock"])
    return u

def links_md(terms):
    return " · ".join(f"[{k}]({v})" for k, v in search_links(terms).items())

def chip_link(cid):
    c = CHIPS[cid]
    return f"[{c['pn']}]({product_link(c['base'])})"

def month_link(n, text=None):
    text = text or f"Month {n}"
    return f"[{text}](../{MONTH_DIRS[n]}/README.md)" if n in MONTH_DIRS else text

def first_month(usage, sid):
    for n in range(1, 25):
        if usage.get(n, {}).get(sid, 0) > 0: return n
    return None

def stock_name(sid): return STOCK[sid]["name"]

def build():
    usage = usage_by_month()
    peaks = {sid: max((usage[n].get(sid, 0) for n in usage), default=0) for sid in STOCK}
    totals = {sid: sum(usage[n].get(sid, 0) for n in usage) for sid in STOCK}
    first = {sid: first_month(usage, sid) for sid in STOCK}
    rec = {sid: ((max(peaks[sid] + 2, math.ceil(peaks[sid] * 1.25)) if STOCK[sid]["commodity"] else peaks[sid] + 1) if peaks[sid] else 0) for sid in STOCK}
    # round of purchase
    def round_of(sid):
        f = first[sid]
        if STOCK[sid]["commodity"] or f is None or f <= 6: return "A"
        return "B" if f <= 12 else ("C" if f <= 19 else "D")
    rounds = {sid: round_of(sid) for sid in STOCK if peaks[sid]}
    out = {}

    # ===================================================== course overview
    L = ["# Course overview: the 24 months", "",
         "A high-level plan of what you will build each month, which chips you will use and what else you need.",
         "**Months 1 to 5 are complete.** Months 6 to 24 are a **plan and may change** as the course develops.", "",
         "Every month uses **two new free-sample chips** (three of each), plus parts from your **lab stock**. "
         "The [purchasing plan](purchasing-plan.md) shows what to order and when, and the [parts catalogue](parts-catalogue.md) has the specifications and links.", "",
         "## The path", "", "| Phase | Months | What it covers |", "|---|:-:|---|"]
    for name, a, b, what in PHASES: L.append(f"| {name} | {a}–{b} | {what} |")
    L += ["", "## Month by month", "",
          "| Month | Project | New chips (free samples) | Main chip | What you learn | Extra parts to buy |", "|:-:|---|---|---|---|---|"]
    for m in PLAN:
        n = m["n"]
        samples = ", ".join(CHIPS[s]["pn"].split(" ")[0] for s in m["samples"]) if m["samples"] else "two of your choice"
        extra = ", ".join(STOCK[s]["name"].split(",")[0] for s in sorted(STOCK, key=lambda s: STOCK[s]["order"]) if first[s] == n and not STOCK[s]["commodity"] and s not in ("wires", "dupont")) or "–"
        proj = month_link(n, m["title"]) if n in MONTH_DIRS else m["title"]
        L.append(f"| {n} | {proj} | {samples} | {m['host']} | {m['learn']} | {extra} |")
    L += ["", "## Details of each month", ""]
    for m in PLAN:
        n = m["n"]
        L += [f"### Month {n}: {m['title']}" + (" (complete)" if m["status"] == "built" else " (planned)"), "",
              f"**Subject:** {m['theme']}.  **Main chip:** {m['host']}.", ""]
        if m["samples"]:
            L.append("**New chips:** " + "; ".join(f"{chip_link(s)} ({CHIPS[s]['what']})" for s in m["samples"]) + ".")
        else:
            L.append("**New chips:** two of your choice from the shortlist: " + ", ".join(chip_link(s) for s in CAPSTONE_SHORTLIST) + ".")
        if m["uses"]: L.append("")
        if m["uses"]: L.append("**Also uses:** " + ", ".join(CHIPS[s]["pn"].split(" ")[0] for s in m["uses"]) + " (from earlier months).")
        L += ["", "**Builds:** " + "; ".join(f"{i+1}. {b}" for i, b in enumerate(m["builds"])) + ".", "",
              "**Project ideas:** " + "; ".join(m["projects"]) + ".", ""]
    out["course-overview.md"] = "\n".join(L)

    # ===================================================== purchasing plan
    L = ["# Purchasing plan", "",
         "The global shopping guide for the whole course: **which chips to order as free samples each month**, **which parts come from your lab stock**, and **what to buy ahead** so you can use bulk prices and free postage.", "",
         "* **Samples:** each month you order **two new chips**, three of each. They are free from Microchip, so order them even if you do not need them for a few weeks.",
         "* **Lab stock:** everyday parts (LEDs, resistors, capacitors, buttons) that you reuse month after month. Buying them once, in bulk, is cheaper and keeps you from stopping to shop.",
         "* **Links:** every part links to its specification; for lab stock, the links search the usual marketplaces so you can choose the cheapest. Check the search results against the specifications in the [parts catalogue](parts-catalogue.md).", "",
         "## 1. Buy ahead: the four rounds", "",
         "| Round | Buy before | What it contains |", "|---|---|---|",
         "| **A** | Month 1 | tools, plus **all the everyday parts in bulk**, plus anything needed up to Month 6 |",
         "| **B** | Month 7 | specialist parts first needed in Months 7 to 12 |",
         "| **C** | Month 13 | specialist parts first needed in Months 13 to 19 |",
         "| **D** | Month 20 | specialist parts first needed in Months 20 to 24 |", "",
         "The quantities below are the **largest amount you use in any one month**, plus a margin. That is enough if you **take each project apart** when the month ends. "
         "If you would rather **keep every project built**, buy the larger \"keep everything\" quantity in section 6.", ""]
    letters = {"A": "Round A: before Month 1", "B": "Round B: before Month 7", "C": "Round C: before Month 13", "D": "Round D: before Month 20"}
    L += ["## 2. What to buy, round by round", "", "### Round A: before Month 1", "", "**Tools (buy once)**", "", "| Item | Qty | What for | Where to find it |", "|---|:-:|---|---|"]
    for name, why, terms, qty in TOOLS: L.append(f"| {name} | {qty} | {why} | {links_md(terms)} |")
    for r in "ABCD":
        items = [s for s in sorted(STOCK, key=lambda s: STOCK[s]["order"]) if rounds.get(s) == r]
        if not items: continue
        if r == "A": L += ["", "**Everyday parts in bulk, and anything needed up to Month 6**"]
        else: L += ["", f"### {letters[r]}"]
        L += ["", "| Item | Buy | First needed | What for | Where to find it |", "|---|:-:|:-:|---|---|"]
        for s in items:
            st = STOCK[s]
            L.append(f"| {st['name']} | {rec[s]} | Month {first[s]} | {st['spec'] or '–'} | {links_md(st['search'])} |")
    L += ["", "*Resistor, capacitor and LED **assortment kits** from a marketplace usually cover every value in this list for a few pounds. Count the kit against the \"Buy\" column.*", ""]
    # samples
    L += ["## 3. Free samples: two new chips every month", "",
          "Order the next month's chips **about four weeks ahead**. Order three of each. Always choose the **through-hole** package named below. If a part is out of stock, see the notes at the end.", "",
          "| Month | Order (3 of each) | Package | Supply | What it is |", "|:-:|---|---|---|---|"]
    for m in PLAN:
        if m["samples"]:
            for i, s in enumerate(m["samples"]):
                c = CHIPS[s]
                L.append(f"| {m['n'] if i == 0 else ''} | {chip_link(s)} | {c['pkg']} | {c['supply']} | {c['what']} |")
        else:
            L.append(f"| {m['n']} | two of your choice from the shortlist | | | see the [parts catalogue](parts-catalogue.md#capstone-shortlist-month-24) |")
    # month by month
    L += ["", "## 4. Month by month: samples, lab stock and extra purchases", "",
          "| Month | Order as samples | From your lab stock | Also buy |", "|:-:|---|---|---|"]
    for m in PLAN:
        n = m["n"]
        u = usage[n]
        stock_txt = ", ".join(f"{STOCK[s]['name'].split(',')[0]} ×{u[s]}" for s in sorted(u, key=lambda s: STOCK[s]['order']) if u[s]) or "–"
        samples = ", ".join(CHIPS[s]["pn"].split(" ")[0] for s in m["samples"]) if m["samples"] else "two from the shortlist"
        buy = ", ".join(f"{STOCK[s]['name'].split(',')[0]} (round {rounds[s]})" for s in sorted(STOCK, key=lambda s: STOCK[s]["order"]) if first[s] == n and not STOCK[s]["commodity"]) or "nothing new"
        L.append(f"| {month_link(n, str(n))} | {samples} | {stock_txt} | {buy} |")
    # stock summary
    L += ["", "## 5. Lab stock summary", "",
          "| Item | First needed | Largest use in one month | Buy (with margin) | Total if you keep every build |", "|---|:-:|:-:|:-:|:-:|"]
    for s in sorted(STOCK, key=lambda s: STOCK[s]["order"]):
        if peaks[s]: L.append(f"| {STOCK[s]['name']} | Month {first[s]} | {peaks[s]} | {rec[s]} | {totals[s]} |")
    L += ["", "## 6. Keeping every project built", "",
          "If you want each project to stay on its own board, add up the last column above. In practice the cheapest way is a **bulk assortment** (100 LEDs, 600 resistors) plus a **second or third breadboard**. "
          "Each month's page tells you what to move and what to keep.", ""]
    L += ["## 7. Tips for ordering", "",
          "* **Chips:** use the free samples. Do **not** buy microcontrollers from marketplace sellers: counterfeit and relabelled chips exist. If a sample is out of stock, buy from a recognised electronics distributor; the catalogue links a distributor search for each chip.",
          "* **Everyday parts:** marketplaces are fine. Choose assortments, and match the value, size and \"1/4 W\" or \"5 mm\" to the specification.",
          "* **Postage:** one big Round A order is cheaper than many small ones. Combine the programmer, power module and assortments.",
          "* **Delays:** marketplace parts can take weeks. Order each round well before you need it.",
          "* **Check what arrived:** measure a few resistors with the multimeter and test a few LEDs before building.",
          "* **Prices change.** The quantities here are what matters; the links find current prices.", ""]
    out["purchasing-plan.md"] = "\n".join(L)

    # ===================================================== parts catalogue
    L = ["# Parts catalogue", "",
         "Every chip and every everyday part in the course, with its specification and links. Chip links open the manufacturer's product page (specifications, datasheet and sample button). "
         "If a link has moved, search the part number.", "",
         "## Chips (free samples)", "",
         "| Part | Package | Supply | What it is | Used from | Links |", "|---|---|---|---|:-:|---|"]
    firstchip = {}
    for m in PLAN:
        for s in m["samples"]: firstchip.setdefault(s, m["n"])
    for s in CHIPS:
        if s in CAPSTONE_SHORTLIST: continue
        c = CHIPS[s]
        L.append(f"| {c['pn']} | {c['pkg']} | {c['supply']} | {c['what']} | {month_link(firstchip[s], str(firstchip[s]))} | [Microchip]({product_link(c['base'])}) · [distributors]({octopart_link(c['pn'])}) |")
    L += ["", "## Capstone shortlist (Month 24)", "", "Choose two for your capstone.", "",
          "| Part | Package | Supply | What it is | Links |", "|---|---|---|---|---|"]
    for s in CAPSTONE_SHORTLIST:
        c = CHIPS[s]
        L.append(f"| {c['pn']} | {c['pkg']} | {c['supply']} | {c['what']} | [Microchip]({product_link(c['base'])}) · [distributors]({octopart_link(c['pn'])}) |")
    L += ["", "## Everyday parts (lab stock)", "",
          "| Item | Specification | Used from | Where to find it |", "|---|---|:-:|---|"]
    for s in sorted(STOCK, key=lambda s: STOCK[s]["order"]):
        if peaks[s]: L.append(f"| {STOCK[s]['name']} | {STOCK[s]['spec'] or '–'} | Month {first[s]} | {links_md(STOCK[s]['search'])} |")
    L += ["", "## Tools", "", "| Item | What for | Where to find it |", "|---|---|---|"]
    for name, why, terms, qty in TOOLS: L.append(f"| {name} | {why} | {links_md(terms)} |")
    L += ["", "*Supply ranges are for planning. Always check the datasheet for your exact part.*", ""]
    out["parts-catalogue.md"] = "\n".join(L)

    # ===================================================== CSV
    rows = [["Month", "Type", "Item", "Part number / specification", "Quantity", "Package", "Link"]]
    for m in PLAN:
        for s in m["samples"]:
            c = CHIPS[s]; rows.append([m["n"], "sample (free)", c["pn"], c["what"], 3, c["pkg"], product_link(c["base"])])
        if not m["samples"]: rows.append([m["n"], "sample (free)", "two of your choice from the shortlist", "", 3, "", ""])
        for s in sorted(usage[m["n"]], key=lambda s: STOCK[s]["order"]):
            if usage[m["n"]][s]: rows.append([m["n"], "lab stock", STOCK[s]["name"], STOCK[s]["spec"], usage[m["n"]][s], "", search_links(STOCK[s]["search"])["AliExpress"]])
    with open(os.path.join(OUT, "purchasing-plan.csv"), "w", newline="", encoding="utf-8") as f: csv.writer(f).writerows(rows)
    mat = [["Item", "Round", "Buy (with margin)"] + [f"M{n}" for n in range(1, 25)]]
    for s in sorted(STOCK, key=lambda s: STOCK[s]["order"]):
        if peaks[s]: mat.append([STOCK[s]["name"], rounds[s], rec[s]] + [usage[n].get(s, 0) for n in range(1, 25)])
    with open(os.path.join(OUT, "lab-stock-matrix.csv"), "w", newline="", encoding="utf-8") as f: csv.writer(f).writerows(mat)

    for name, text in out.items(): open(os.path.join(OUT, name), "w", encoding="utf-8").write(text.rstrip("\n") + "\n")
    return usage, peaks, rec

if __name__ == "__main__":
    u, peaks, rec = build()
    format_tree(ROOT)
    print("wrote start-here/course-overview.md, purchasing-plan.md, parts-catalogue.md, purchasing-plan.csv, lab-stock-matrix.csv")
    print("peaks:", {k: v for k, v in peaks.items() if v})
