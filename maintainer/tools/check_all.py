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
import os
import re
import shutil
import subprocess
import sys
from circuits import CIRCUITS

if shutil.which("node") is None:
    sys.exit(
        "ERROR: Node.js was not found on PATH.\n"
        "Install Node.js LTS, then reopen PowerShell and run check_all.py again."
    )

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

IS_WINDOWS = os.name == "nt"

if IS_WINDOWS:
    BASH = r"C:\msys64\usr\bin\bash.exe"

    if not os.path.isfile(BASH):
        BASH = shutil.which("bash")

    if BASH is None:
        sys.exit(
            "ERROR: bash was not found.\n"
            "Install MSYS2 and ensure C:\\msys64\\usr\\bin\\bash.exe exists,\n"
            "or add C:\\msys64\\usr\\bin to PATH."
        )

    MSYS_ROOT = os.path.dirname(os.path.dirname(BASH))

    MSYS_PATHS = [
        os.path.join(MSYS_ROOT, "usr", "bin"),
        os.path.join(MSYS_ROOT, "ucrt64", "bin"),
    ]

    SUBPROCESS_ENV = os.environ.copy()
    SUBPROCESS_ENV["PATH"] = os.pathsep.join(
        MSYS_PATHS + [SUBPROCESS_ENV.get("PATH", "")]
    )
else:
    BASH = shutil.which("bash")

    if BASH is None:
        sys.exit("ERROR: bash was not found on PATH.")

    MSYS_PATHS = []
    SUBPROCESS_ENV = os.environ.copy()

ok = True


def step(name, good, detail=""):
    global ok
    ok &= bool(good)
    print(
        ("PASS " if good else "FAIL ")
        + name
        + (("\n  " + detail.replace("\n", "\n  ")) if detail and not good else "")
    )


def run(cmd, cwd):
    r = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=SUBPROCESS_ENV,
    )
    return r.returncode == 0, (r.stdout + r.stderr)[-1500:]


# 1 logic tests
sim_targets = [
    entry["id"]
    for entry in CIRCUITS
    if "id" in entry
    and os.path.isfile(os.path.join(ROOT, "maintainer", "sim", entry["id"], "run_tests.sh"))
]

for m in sim_targets:
    sim_dir = os.path.join(ROOT, "maintainer", "sim", m)

    bash_command = (
        'export PATH="/usr/bin:/ucrt64/bin:$PATH"; '
        'exec bash ./run_tests.sh'
    )

    good, out = run([BASH, "-c", bash_command], sim_dir)

    n_fail = len(re.findall(r"FAILED|FAIL:", out))
    step(f"logic tests ({m})", good and n_fail == 0, out)

# 2 diagrams & project sync
good, out = run([sys.executable, "make_all.py"], HERE)
step("breadboard layouts match schematics; diagrams regenerated", good, out)

good, out = run([sys.executable, "make_extra.py"], HERE)
step("teaching diagrams generated", good, out)

good, out = run([sys.executable, "make_hardware.py"], HERE)
step("KiCad parts lists and connection lists generated", good, out)

good_proj_drift, out_proj_drift = run([sys.executable, "make_projects.py", "--check"], HERE)
step("project files match code/ before sync", good_proj_drift, out_proj_drift)

good, out = run([sys.executable, "make_projects.py"], HERE)
step("ready-to-open projects in step with the code", good, out)

good, out = run([sys.executable, "make_purchasing.py"], HERE)
step("overview, purchasing plan and parts catalogue generated", good, out)

good, out = run([sys.executable, "make_bench_sheets.py"], HERE)
step("bench validation sheets generated", good, out)

# 3 sync
good, out = run([sys.executable, "sync_readme_months.py"], HERE)
step("root README months table synced with course_data", good, out)

good, out = run([sys.executable, "sync_docs.py"], HERE)
step("pages synced with code and circuits", good, out)

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
        txt = open(p, encoding="utf-8").read()
        txt = re.sub(r"```.*?```", "", txt, flags=re.S)
        anchors[p] = {slug(m.group(2)) for m in re.finditer(r"^(#{1,6})\s+(.*)$", txt, re.M)}
    return anchors[p]


bad = []
for p in mds:
    txt = re.sub(r"```.*?```", "", open(p, encoding="utf-8").read(), flags=re.S)
    for m in re.finditer(r"!?\[[^\]]*\]\(([^)\s]+)\)", txt):
        link = m.group(1)
        if re.match(r"^(https?:|mailto:)", link):
            continue
        path, _, frag = link.partition("#")
        target = os.path.normpath(os.path.join(os.path.dirname(p), path)) if path else p
        if not os.path.exists(target):
            bad.append(f"{os.path.relpath(p, ROOT)}: missing file {link}")
            continue
        if frag and target.endswith(".md") and frag not in anchors_of(target):
            bad.append(f"{os.path.relpath(p, ROOT)}: missing anchor {link}")
step(f"all links, images and anchors resolve ({len(mds)} pages)", not bad, "\n".join(bad[:25]))

# 5 stale markers
stale = []
for p in mds:
    if p.endswith("CHANGELOG.md"):
        continue
    t = open(p, encoding="utf-8").read()
    for pat in (
        r"TODO",
        r"PLACEHOLDER",
        r"\bV\d{2}\b",
        r"FIXME",
        r"\b(old|earlier|previous) (package|course|version|Month|edition)",
        r"rewritten",
        r"\bpilot\b",
    ):
        if re.search(pat, t):
            stale.append(f"{os.path.relpath(p, ROOT)}: contains {pat}")
badnames = [f for dp, _, fs in os.walk(ROOT) for f in fs if re.search(r"_V\d+", f)]
step("no TODO / placeholder / version stamps in pages or file names", not stale and not badnames, "\n".join(stale + badnames))

print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
