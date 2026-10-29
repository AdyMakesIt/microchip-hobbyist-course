#!/usr/bin/env python3
"""
format_tables.py - pads every Markdown table so the | characters line up in the SOURCE text too.
(The rendered page always aligns; this makes the raw file readable as well.)  Safe to run repeatedly.
"""
import os, re, unicodedata

def width(s):
    w = 0
    for ch in s:
        w += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return w

def split_row(line):
    line = line.strip()
    if line.startswith("|"): line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"): line = line[:-1]
    cells, cur, i = [], "", 0
    while i < len(line):
        if line[i] == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            cur += "\\|"; i += 2; continue
        if line[i] == "`":                      # keep pipes inside inline code together
            j = line.find("`", i + 1)
            if j != -1: cur += line[i:j + 1]; i = j + 1; continue
        if line[i] == "|": cells.append(cur.strip()); cur = ""
        else: cur += line[i]
        i += 1
    cells.append(cur.strip())
    return cells

def is_sep(cells):
    return all(re.fullmatch(r":?-{1,}:?", c) for c in cells) and len(cells) > 0

def pad(c, w, align):
    gap = w - width(c)
    if align == "r": return " " * gap + c
    if align == "c": l = gap // 2; return " " * l + c + " " * (gap - l)
    return c + " " * gap

def format_table(lines):
    rows = [split_row(l) for l in lines]
    n = max(len(r) for r in rows)
    rows = [r + [""] * (n - len(r)) for r in rows]
    sep_i = 1 if len(rows) > 1 and is_sep(rows[1]) else None
    if sep_i is None: return lines
    aligns = []
    for c in rows[1]:
        aligns.append("c" if c.startswith(":") and c.endswith(":") else "r" if c.endswith(":") else "l")
    widths = [max(3, max(width(r[i]) for k, r in enumerate(rows) if k != 1)) for i in range(n)]
    out = []
    for k, r in enumerate(rows):
        if k == 1:
            cells = []
            for i in range(n):
                d = "-" * widths[i]
                if aligns[i] == "c": d = ":" + "-" * (widths[i] - 2) + ":"
                elif aligns[i] == "r": d = "-" * (widths[i] - 1) + ":"
                cells.append(d)
        else:
            cells = [pad(r[i], widths[i], aligns[i] if k != 0 else "l") for i in range(n)]
        out.append("| " + " | ".join(cells) + " |")
    return out

def format_text(text):
    lines = text.split("\n"); out = []; i = 0; fence = False
    while i < len(lines):
        l = lines[i]
        if l.lstrip().startswith("```"): fence = not fence
        if not fence and l.lstrip().startswith("|") and "|" in l.strip()[1:]:
            j = i
            while j < len(lines) and lines[j].lstrip().startswith("|"): j += 1
            out += format_table(lines[i:j]); i = j; continue
        out.append(l); i += 1
    return "\n".join(out)

def format_tree(root):
    n = 0
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", "node_modules", "dist")]
        for f in fn:
            if f.endswith(".md"):
                p = os.path.join(dp, f); t = open(p).read(); nt = format_text(t)
                if nt != t: open(p, "w").write(nt); n += 1
    return n

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    print("tables re-aligned in", format_tree(os.path.abspath(os.path.join(here, "..", ".."))), "pages")
