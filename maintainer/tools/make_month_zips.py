#!/usr/bin/env python3
"""Builds one ZIP per month (plus start-here) in dist/ for attaching to a GitHub Release or sharing directly."""
import os, zipfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "dist"); os.makedirs(OUT, exist_ok=True)
folders = ["start-here"] + sorted(d for d in os.listdir(ROOT) if d.startswith("month-"))
for f in folders:
    zp = os.path.join(OUT, f + ".zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, dn, fn in os.walk(os.path.join(ROOT, f)):
            for name in fn:
                full = os.path.join(dp, name); z.write(full, os.path.relpath(full, ROOT))
        z.write(os.path.join(ROOT, "README.md"), "README.md")
    print("wrote", os.path.relpath(zp, ROOT))
