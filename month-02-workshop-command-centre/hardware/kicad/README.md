# KiCad project files

Put this month's KiCad project here. Use these names so every month looks the same:

| File                     | Name                                                                                   |
| ------------------------ | -------------------------------------------------------------------------------------- |
| project                  | `month-02-workshop-command-centre.kicad_pro`                                           |
| schematic                | `month-02-workshop-command-centre.kicad_sch`                                           |
| PCB (if you make one)    | `month-02-workshop-command-centre.kicad_pcb`                                           |
| schematic printed to PDF | `month-02-workshop-command-centre-schematic.pdf` (so people can read it without KiCad) |

Rules:

* One KiCad project per month. Mark which build each part belongs to with a **field** (for example `Build = 2`), or draw one sheet per build.
* Use KiCad's standard symbol and footprint libraries. If a part is missing, make it in KiCad's editors and store the library **in this folder** (`mhc-parts.kicad_sym`, `mhc-parts.pretty/`), so the project opens on any computer.
* Use the **parts list** in `../exports/` for values and footprints, and the **connection list** to check your wiring.
* Do **not** commit KiCad backups or caches (the repository's `.gitignore` already excludes them).

*No schematic has been drawn here yet.*
