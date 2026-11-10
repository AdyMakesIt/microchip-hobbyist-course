# Projects and hardware guide

How the repository stores **complete working projects** and **KiCad schematics**, and how to add them.

## The layout of a month

```text
month-0N-name/
  README.md, build pages            what the learner reads
  images/                           breadboard and schematic pictures (generated)
  code/<build>/main.c               the source shown on the pages: the ONE source of truth
  projects/
    platformio/<build>/             AVR builds: platformio.ini + src/main.c   (generated; do not edit)
    arduino/<sketch>/<sketch>.ino   Arduino sketches                           (generated; do not edit)
    mplabx/<build>.X/               PIC builds: a real MPLAB X project          (exported after bench-testing)
  hardware/
    kicad/                          the KiCad project drawn by you
    exports/                        parts list and connection list (generated)
```

`code/` is the source of truth. Everything in `projects/` is a copy that must stay identical. `check_all.py` runs `make_projects.py --check`, which fails if a copy has drifted.

## Adding an MPLAB X project (PIC builds)

Do this **after** a build has compiled and run on your bench, so every published project is known to work.

1. In MPLAB X make the project **inside** `projects/mplabx/`, named like the build (for example `build-2-hello-expander.X`), with the settings in that month's `projects/mplabx/README.md` (device, compiler, PICkit 3, "Power target circuit from PICkit3" unticked).
2. Add `main.c` by **copying** it into the project (not linking), and make sure it is **identical** to `code/<build>/main.c`. Edit `code/` first if you changed the program, then copy.
3. **Clean** the project (Production → Clean) and delete any `build/`, `dist/` and `debug/` folders. The repository's `.gitignore` also excludes them.
4. Commit the `.X` folder (it contains `nbproject/` with `configurations.xml` and `project.xml`, the `Makefile`, and `main.c`).
5. Run `python3 maintainer/tools/make_projects.py`: the status table in `PROJECT_STATUS.md` updates and the check confirms `main.c` matches.
6. Note the MPLAB X, compiler and device-pack versions in `VERIFICATION_LOG.md`.

## PlatformIO and Arduino

Generated. Edit `code/…/main.c` (or the `.ino`), then run `python3 maintainer/tools/make_projects.py`. The PlatformIO `platformio.ini` has two environments: `usbasp` and `uno_isp`.

## KiCad schematics

* **Version:** use a current KiCad (7 or newer) and say which in the project's notes.
* **Where:** `hardware/kicad/` in each month, named `<month-folder>.kicad_pro` / `.kicad_sch` (see the `README.md` there). One project per month.
* **Start from the exports:** `hardware/exports/*-bom.csv` lists every part with a *suggested* KiCad footprint, and `*-netlist.csv` lists every net with its pins. Use them to draw the schematic and then to check it against the verified circuit.
* **Libraries:** use KiCad's standard libraries where possible. If you create a symbol or footprint, keep the library in the month's `hardware/kicad/` folder so the project opens anywhere.
* **Also commit** a PDF of the schematic (`<name>-schematic.pdf`) so people can read it without KiCad.
* **Do not commit:** `*-backups/`, `fp-info-cache`, `*.kicad_prl`, `_autosave-*` (already in `.gitignore`).
* **Per build:** mark which build each part belongs to with a custom field (`Build = 2`), or draw one sheet per build.
* **PCBs:** if you lay out a board, commit the `.kicad_pcb` and the fabrication outputs in `hardware/kicad/fabrication/`, and record in the `README.md` there whether the board has been **built and tested**.

## What the generators write

| Tool                 | Writes                                                                   | From                                    |
| -------------------- | ------------------------------------------------------------------------ | --------------------------------------- |
| `make_all.py`        | `images/` (SVG, PNG), after verifying every layout                       | `tools/circuits.py`                     |
| `make_hardware.py`   | `hardware/exports/*.csv` and the `hardware/README.md` files              | `tools/circuits.py`                     |
| `make_projects.py`   | `projects/platformio`, `projects/arduino`, `PROJECT_STATUS.md`           | `code/`                                 |
| `make_purchasing.py` | the overview, purchasing plan, parts catalogue and CSVs in `start-here/` | `tools/course_data.py` and the circuits |
| `sync_docs.py`       | the generated blocks inside the pages                                    | code and circuits                       |
| `check_all.py`       | runs all of the above plus the logic tests and the link check            |                                         |
