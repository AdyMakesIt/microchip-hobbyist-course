# Maintainer guide

Everything here is for the person *writing* the course, not the learner.

| File                                       | What it is                                                        |
| ------------------------------------------ | ----------------------------------------------------------------- |
| [GITHUB_GUIDE.md](GITHUB_GUIDE.md)         | how to put the course on GitHub and bundle it month by month      |
| [VERIFICATION_LOG.md](VERIFICATION_LOG.md) | what has been checked, what has not, and what was assumed         |
| [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md)   | the rules and the template for writing a new month                |
| `sim/`                                     | logic tests that run each `main.c` on a PC ([how](sim/README.md)) |
| `tools/`                                   | diagram generator, page sync, checks, zip maker                   |

## The workflow for any change

```text
edit  ->  python3 maintainer/tools/check_all.py  ->  commit
```

`check_all.py` runs the logic tests, **re-verifies every breadboard layout against its schematic**, regenerates all pictures, re-injects code and
tables into the pages, and checks every link. If it passes, the package is internally consistent.

## How the pieces fit

* `tools/course_data.py` holds **the course plan and every part** (chips, lab stock, links). Edit it to change the plan; `make_purchasing.py` regenerates the overview, purchasing plan and parts catalogue.
* `tools/circuits.py` holds **one description per month**: the schematic chains and the breadboard holes.
* `tools/mhc_draw.py` draws the schematic and breadboard SVGs and **refuses to produce a picture** if the two disagree.
* `tools/sync_docs.py` fills marked blocks in the pages (`<!-- code:... -->`, `<!-- placement:N -->`, `<!-- connections:N -->`, `<!-- bom -->`).
  **Never edit between those markers by hand**: the next sync will overwrite it. Edit the circuit or code instead.
* Requirements: Python 3, `g++`, and Node.js with the `sharp` package (only for PNG export).
