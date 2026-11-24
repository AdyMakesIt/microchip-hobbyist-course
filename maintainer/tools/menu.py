#!/usr/bin/env python3
"""
menu.py - Cross-platform maintainer menu for Windows and Unix/macOS.
Replaces check_all.ps1 and new_month.ps1 while allowing individual standalone tools and flags.
"""

import argparse
import os
import re
import shlex
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def _can_prompt():
    return sys.stdin is not None and sys.stdin.isatty()


def _sanitize_paths(text):
    if not text:
        return text
    variants = sorted(
        {
            ROOT,
            ROOT.replace("\\", "/"),
            ROOT.replace("/", "\\"),
        },
        key=len,
        reverse=True,
    )
    for base in variants:
        pattern = re.compile(re.escape(base) + r"[\\/]*", re.IGNORECASE)
        text = pattern.sub("<COURSE-DIR>/", text)
    return text


def _run_tool(script_name, args=None, cwd=ROOT):
    script_path = os.path.join(HERE, script_name)
    if not os.path.isfile(script_path):
        print(f"FAIL script not found: {_sanitize_paths(script_path)}")
        return 1

    args = args or []
    cmd = [sys.executable, "-u", script_path] + args
    display = " ".join([script_name] + [shlex.quote(p) for p in args])
    print(f"\nRunning: {display}", flush=True)

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        env=env,
    )

    assert proc.stdout is not None
    for line in proc.stdout:
        print(_sanitize_paths(line), end="", flush=True)

    proc.wait()
    return proc.returncode


def run_full_check(extra_args):
    """
    Replicates check_all.ps1:
      1. Optionally --pull project changes into code/ (or prompt if drifted)
      2. Sync README.md months table from course_data.PLAN
      3. Run check_all.py
    """
    pull_requested = "--pull" in extra_args or "--pull-projects" in extra_args
    passthrough = [
        a for a in extra_args if a not in ("--pull", "--pull-projects")
    ]

    if pull_requested:
        print("Pulling tested project changes back into code/...")
        rc = _run_tool("make_projects.py", ["--pull"], cwd=ROOT)
        if rc != 0:
            print("FAIL could not pull project changes into code/.")
            return rc
        print("PASS projects synced into code/")

    rc = _run_tool("make_projects.py", ["--check"], cwd=ROOT)
    if rc == 0:
        print("PASS projects in step with code")
    else:
        print("FAIL projects in step with code")
        if _can_prompt():
            print("\nProject files differ from code/.")
            ans = input("Sync from the project into code/ now? [y/N]: ").strip().lower()
            if ans in ("y", "yes"):
                rc = _run_tool("make_projects.py", ["--pull"], cwd=ROOT)
                if rc != 0:
                    print("FAIL could not pull project changes into code/.")
                    return rc
                print("PASS projects synced into code/")
            else:
                print("Skipping sync. Update code/<build>/main.c manually or pass --pull.")
                return 1
        else:
            print("\nFAIL project files differ from code/ (non-interactive session).")
            print("Update code/<build>/main.c from the project, or pass --pull.")
            return rc

    rc = _run_tool("sync_readme_months.py", [], cwd=ROOT)
    if rc != 0:
        print("FAIL updating README.md months")
        return rc
    print("PASS updating README.md months")

    return _run_tool("check_all.py", passthrough, cwd=HERE)


def _scaffold_month(month, slug, prefix="main", title=""):
    mm = f"{month:02d}"
    fn_name = f"month{month}"
    if not title.strip():
        title = f"Month {month}"

    circuits_dir = os.path.join(HERE, "circuits")
    module_path = os.path.join(circuits_dir, f"month{mm}.py")

    if not os.path.exists(module_path):
        os.makedirs(circuits_dir, exist_ok=True)
        template = (
            "from mhc_draw import Circuit, Board\n"
            "from ._helpers import add_standard_rails, add_decoupling_cap\n\n\n"
            f"def {fn_name}():\n"
            f'    c = Circuit("{title}")\n'
            "    b = Board(c)\n"
            "    add_standard_rails(b, build=1)\n"
            f"    # TODO: Add IC, schematic chains, and breadboard placement for {title}\n"
            "    return c, b\n"
        )
        with open(module_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(template)
        print(f"Created {_sanitize_paths(module_path)}")
    else:
        print(f"Module already exists: {_sanitize_paths(module_path)}")

    print("\nAdd this import and entry to maintainer/tools/circuits/__init__.py:")
    print(f"  from .month{mm} import {fn_name}")
    print(
        f'  {{"id": "m{month}", "month": {month}, "track": "{prefix}", '
        f'"folder": "{slug}", "prefix": "{prefix}", "title": "{title}", "fn": {fn_name}}},'
    )
    return 0


def run_new_month(extra_args):
    parser = argparse.ArgumentParser(prog="new-month", add_help=True, exit_on_error=False)
    parser.add_argument("--month", type=int)
    parser.add_argument("--slug", type=str)
    parser.add_argument("--prefix", type=str, default="main")
    parser.add_argument("--title", type=str, default="")

    if extra_args:
        try:
            ns = parser.parse_args(extra_args)
        except SystemExit as exc:
            return exc.code if isinstance(exc.code, int) else 1
        if ns.month is None or not ns.slug:
            print("FAIL --month and --slug are required when passing flags.")
            return 2
        return _scaffold_month(ns.month, ns.slug, ns.prefix, ns.title)

    if not _can_prompt():
        print("FAIL --month and --slug are required in non-interactive mode.")
        return 2

    try:
        month_raw = input("Month number (e.g. 6): ").strip()
        month = int(month_raw)
        slug = input("Folder slug (e.g. month-06-...): ").strip()
        if not slug:
            print("FAIL slug cannot be empty.")
            return 1
        prefix = input("Prefix [main]: ").strip() or "main"
        title = input(f"Title [Month {month}]: ").strip()
    except ValueError:
        print("FAIL month must be an integer.")
        return 1

    return _scaffold_month(month, slug, prefix, title)


ACTIONS = [
    {
        "key": "1",
        "label": "Full verification suite (check_all)",
        "hint": "Checks project drift (prompts to --pull), syncs README months, runs check_all.py",
        "fn": run_full_check,
    },
    {
        "key": "2",
        "label": "Sync project files (make_projects.py)",
        "hint": "Optional flags: --check, --pull",
        "script": "make_projects.py",
        "cwd": ROOT,
    },
    {
        "key": "3",
        "label": "Sync README months table (sync_readme_months.py)",
        "hint": "Optional flags: --check",
        "script": "sync_readme_months.py",
        "cwd": ROOT,
    },
    {
        "key": "4",
        "label": "Sync documentation pages (sync_docs.py)",
        "hint": "Syncs markdown pages with code and circuits",
        "script": "sync_docs.py",
        "cwd": ROOT,
    },
    {
        "key": "5",
        "label": "Generate purchasing & parts docs (make_purchasing.py)",
        "hint": "Regenerates overview, purchasing plan and parts catalogue",
        "script": "make_purchasing.py",
        "cwd": ROOT,
    },
    {
        "key": "6",
        "label": "Generate bench validation sheets (make_bench_sheets.py)",
        "hint": "Regenerates bench validation sheets",
        "script": "make_bench_sheets.py",
        "cwd": ROOT,
    },
    {
        "key": "7",
        "label": "Regenerate breadboard & schematic diagrams (make_all.py)",
        "hint": "Verifies breadboard layouts and regenerates SVGs",
        "script": "make_all.py",
        "cwd": ROOT,
    },
    {
        "key": "8",
        "label": "Generate teaching diagrams (make_extra.py)",
        "hint": "Regenerates supplemental teaching diagrams",
        "script": "make_extra.py",
        "cwd": ROOT,
    },
    {
        "key": "9",
        "label": "Generate KiCad BOM & netlists (make_hardware.py)",
        "hint": "Regenerates KiCad parts lists and connection lists",
        "script": "make_hardware.py",
        "cwd": ROOT,
    },
    {
        "key": "10",
        "label": "Scaffold new circuit module (new_month)",
        "hint": "Creates circuits/monthXX.py or pass --month 6 --slug ...",
        "fn": run_new_month,
    },
    {
        "key": "11",
        "label": "Build release ZIPs in dist/ (make_month_zips.py)",
        "hint": "Packages start-here and month-* folders with README.md into dist/",
        "script": "make_month_zips.py",
        "cwd": ROOT,
    },]


def execute_action(action, extra_args):
    print("-" * 60)
    if "fn" in action:
        rc = action["fn"](extra_args)
    else:
        rc = _run_tool(action["script"], extra_args, cwd=action["cwd"])
    print("-" * 60)
    print(f"Exit code: {rc}\n")
    return rc


def print_menu():
    print("\n=== Maintainer Menu ===")
    for act in ACTIONS:
        print(f"  {act['key']:>2}. {act['label']}")
        print(f"       {act['hint']}")
    print("   q. Quit")


def main():
    by_key = {act["key"]: act for act in ACTIONS}

    # Direct CLI mode: e.g. menu.cmd 1 --pull  or  ./menu.sh 10 --month 6 --slug month-06-foo
    if len(sys.argv) > 1:
        choice = sys.argv[1].strip().lower()
        action = by_key.get(choice)
        if not action:
            print(f"Unknown option '{sys.argv[1]}'. Valid options: {', '.join(by_key)}")
            return 2
        return execute_action(action, sys.argv[2:])

    while True:
        print_menu()
        choice = input("\nSelect an option: ").strip().lower()
        if choice in ("q", "quit", "exit"):
            print("Bye.")
            return 0

        action = by_key.get(choice)
        if not action:
            print("Invalid selection. Try again.")
            continue

        raw_flags = input(
            "Optional arguments (e.g. --check, --pull, or Enter for none): "
        ).strip()
        try:
            extra_args = (
                shlex.split(raw_flags, posix=(os.name != "nt")) if raw_flags else []
            )
        except ValueError as exc:
            print(f"Could not parse arguments: {exc}")
            continue

        execute_action(action, extra_args)
        input("Press Enter to return to the menu...")


if __name__ == "__main__":
    sys.exit(main())
