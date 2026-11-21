#!/usr/bin/env python3
"""
make_bench_sheets.py - writes printable validation sheets from the build pages themselves,
placing each sheet directly alongside its build folder so learners can find it easily.
"""
import os, re
from collections import defaultdict
from circuits import CIRCUITS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SUBDIR = ""  # Use "" to write directly in <folder>/, or "bench-sheets" for <folder>/bench-sheets/


def section(text, key):
    m = re.search(r"^## \d+\. " + key + r".*?\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def assumptions():
    t = open(os.path.join(ROOT, "maintainer", "VERIFICATION_LOG.md"), encoding="utf-8").read()
    a = t.index("## Assumptions that only the real tools")
    out = {}
    for line in t[a:].split("\n"):
        if line.startswith("|"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if c and c[0].isdigit():
                out[int(c[0])] = c[1:]
    return out


def sheet_out_dir(folder):
    base = os.path.join(ROOT, folder)
    return os.path.join(base, SUBDIR) if SUBDIR else base


def resolve_sheet_name(entry):
    raw = entry.get("sheet_filename") or entry.get("sheet_file")
    if raw:
        return raw if raw.endswith(".md") else f"{raw}.md"
    prefix = entry.get("sheet_prefix") or entry.get("prefix") or entry["id"]
    return f"{prefix}-bench.md"


def main():
    A = assumptions()
    by_folder = defaultdict(list)
    count = 0

    for entry in CIRCUITS:
        if "pages" not in entry or "folder" not in entry:
            continue
        folder = entry["folder"]
        filename = resolve_sheet_name(entry)
        title = entry.get("sheet_title", entry["title"])
        pages = entry["pages"]
        tools = entry.get("tools", "MPLAB X v6.20, XC8, PICkit 3, multimeter")
        assum = entry.get("assumptions", [])

        out_dir = sheet_out_dir(folder)
        os.makedirs(out_dir, exist_ok=True)

        L = [
            f"# Bench validation sheet: {title}", "",
            f"**Tools:** {tools}", "",
            "Date: ____________   Photo of the breadboard taken: [ ]", "",
            "Work through the builds **in order**. Tick what happened, and write down any message you saw (compiler, programmer, avrdude) exactly as it appeared.", ""
        ]
        for pg in pages:
            p = os.path.join(ROOT, folder, pg)
            if not os.path.exists(p):
                print(f"   (skipping missing page: {folder}/{pg})")
                continue
            t = open(p, encoding="utf-8").read().replace("\r\n", "\n")
            name = re.search(r"^# (.*)$", t, re.M).group(1)
            L += [f"## {name}", "", f"Page: `{pg}`", ""]
            chk = section(t, "Check before you power it")
            items = [re.sub(r"^\s*(\d+\.|[*-])\s*", "- [ ] ", l) for l in chk.split("\n") if re.match(r"^\s*(\d+\.|[*-])\s", l)]
            if items:
                L += ["**Before power (meter checks):**", ""] + items + [""]
            L += ["**Programming:**", "", "- [ ] Built with no errors", "- [ ] Programmed", "- [ ] Program runs", ""]
            ps = section(t, "Pass check")
            boxes = [l.replace("* [ ]", "- [ ]") for l in ps.split("\n") if l.startswith("* [ ]")]
            if boxes:
                L += ["**Pass checks:**", ""] + boxes + [""]
            L += ["| Result | Notes / exact messages |", "|---|---|", "| [ ] passed   [ ] partly   [ ] failed | |", ""]
        if assum:
            L += [
                "## Assumptions to confirm this month", "",
                "These were written from datasheets and published examples, not from a real build. Tick each when you have confirmed it, or note what differs.", "",
                "| # | Assumption | Confirmed? |", "|:-:|---|:-:|"
            ]
            for n in assum:
                if n in A:
                    L.append(f"| {n} | {A[n][0]} | [ ] |")
            L.append("")
        L += ["## Summary", "", "Overall: [ ] all builds passed   [ ] some failed.   Biggest problem: ______________________________", ""]

        sheet_path = os.path.join(out_dir, filename)
        open(sheet_path, "w", encoding="utf-8").write("\n".join(L).rstrip("\n") + "\n")
        print(f"wrote {os.path.relpath(sheet_path, ROOT)}")
        by_folder[folder].append((filename, title))
        count += 1

    print(f"wrote {count} bench sheets across {len(by_folder)} folders")


if __name__ == "__main__":
    main()
    