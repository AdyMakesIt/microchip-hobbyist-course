#!/usr/bin/env python3
"""
check_all.py - one command that proves the package is consistent.  Run it before every commit.

  1. logic tests for every build (needs g++)
  2. every breadboard layout verified against its schematic, diagrams regenerated
  3. Markdown pages re-synced with code / tables
  4. every relative link, image and #anchor in every .md file exists
  5. no stale markers (TODO, PLACEHOLDER, version stamps in file names)

Usage:  python3 maintainer/tools/check_all.py        (from the repository root, or anywhere)
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ok = True

def step(name, good, detail=""):
    global ok
    ok &= bool(good)
    print(("PASS  " if good else "FAIL  ") + name + (("\n      " + detail.replace("\n", "\n      ")) if detail and not good else ""))

def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr)[-1500:]

# 1 logic tests
for m in ("m1pic", "m1avr", "m2", "m3", "m4", "m5"):
    good, out = run(["sh", "run_tests.sh"], os.path.join(ROOT, "maintainer", "sim", m))
    n_fail = len(re.findall(r"FAILED|FAIL:", out))
    step(f"logic tests ({m})", good and n_fail == 0, out)

# 2 diagrams
good, out = run([sys.executable, "make_all.py"], HERE); step("breadboard layouts match schematics; diagrams regenerated", good, out)
good, out = run([sys.executable, "make_extra.py"], HERE); step("teaching diagrams generated", good, out)
good, out = run([sys.executable, "make_hardware.py"], HERE); step("KiCad parts lists and connection lists generated", good, out)
good, out = run([sys.executable, "make_projects.py"], HERE); step("ready-to-open projects in step with the code", good, out)
good, out = run([sys.executable, "make_purchasing.py"], HERE); step("overview, purchasing plan and parts catalogue generated", good, out)

# 3 sync
good, out = run([sys.executable, "sync_docs.py"], HERE); step("pages synced with code and circuits", good, out)

# 4 links
def slug(h):
    h = re.sub(r"[*`_]", "", h.strip().lower())
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")
mds = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in (".git", "node_modules", "dist")]
    mds += [os.path.join(dp, f) for f in fn if f.endswith(".md")]
anchors = {}
def anchors_of(p):
    if p not in anchors:
        txt = open(p).read()
        txt = re.sub(r"```.*?```", "", txt, flags=re.S)
        anchors[p] = {slug(m.group(2)) for m in re.finditer(r"^(#{1,6})\s+(.*)$", txt, re.M)}
    return anchors[p]
bad = []
for p in mds:
    txt = re.sub(r"```.*?```", "", open(p).read(), flags=re.S)
    for m in re.finditer(r"!?\[[^\]]*\]\(([^)\s]+)\)", txt):
        link = m.group(1)
        if re.match(r"^(https?:|mailto:)", link): continue
        path, _, frag = link.partition("#")
        target = os.path.normpath(os.path.join(os.path.dirname(p), path)) if path else p
        if not os.path.exists(target): bad.append(f"{os.path.relpath(p, ROOT)}: missing file {link}"); continue
        if frag and target.endswith(".md") and frag not in anchors_of(target):
            bad.append(f"{os.path.relpath(p, ROOT)}: missing anchor {link}")
step(f"all links, images and anchors resolve ({len(mds)} pages)", not bad, "\n".join(bad[:25]))

# 5 stale markers
stale = []
for p in mds:
    if p.endswith("CHANGELOG.md"): continue
    t = open(p).read()
    for pat in (r"TODO", r"PLACEHOLDER", r"\bV\d{2}\b", r"FIXME", r"\b(old|earlier|previous) (package|course|version|Month|edition)", r"rewritten", r"\bpilot\b"):
        if re.search(pat, t): stale.append(f"{os.path.relpath(p, ROOT)}: contains {pat}")
badnames = [f for dp, _, fs in os.walk(ROOT) for f in fs if re.search(r"_V\d+", f)]
step("no TODO / placeholder / version stamps in pages or file names", not stale and not badnames, "\n".join(stale + badnames))

print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
