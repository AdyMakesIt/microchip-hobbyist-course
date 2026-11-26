# Contributing

Thank you for considering a contribution! This course is built with a specific structure and tooling. Please read this guide before submitting changes.

## How the Course Works

- **One folder per month** (`month-NN-name/`) containing pages, images, and code
- **One page per build** with a consistent 8-section template
- **Plain C** — no generated code in early months
- **Single source of truth**: `maintainer/tools/course_data.py` defines chips, parts, and the course plan
- **Machine-verified diagrams**: circuits → schematics + breadboard layouts that self-verify
- **Simulation tests**: Every `main.c` runs against a PC model of chips/buses

## Writing a New Month

See **[maintainer/AUTHORING_GUIDE.md](maintainer/AUTHORING_GUIDE.md)** for:
- The 10 rules every month must follow
- Page template (8 sections)
- Step-by-step workflow
- Style guidelines

## The Check Workflow

Before committing, run:

```bash
python3 maintainer/tools/check_all.py
```

This runs all logic tests, verifies layouts match schematics, regenerates diagrams, injects code/tables into pages, and checks links. **CI runs this on every PR.**

## Reporting Issues

If you build a month on real hardware and something doesn't work:

1. Open an issue using the **Bench Report template** (`.github/ISSUE_TEMPLATE/bench-report.md`)
2. **Attach a photo of your breadboard** — it's the fastest way to spot wiring slips
3. Include: month, build, tool versions (MPLAB X, XC8, PlatformIO, etc.), exact error message

## Code Style

- Short sentences. Say what each part is *for* the first time it appears.
- Use hole names (`16b`) and pin numbers, never "next to the chip".
- Explain **why** a rule exists once (decoupling capacitor, pull-up), then link back.
- Tables for lists of facts, prose for reasons.
- Never put version numbers in file names — use git tags and CHANGELOG.md.

## Licence

By contributing, you agree that your contributions will be licensed under:
- **CC BY-SA 4.0** for text, images, diagrams, documentation
- **MIT** for C source code (`main.c`)

See [LICENSE](LICENSE) for details.

## Questions?

Open a GitHub Issue or start a Discussion — happy to help!