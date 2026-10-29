# Microchip Hobbyist Course

Learn to build with Microchip's **PIC** and **AVR** microcontrollers on a breadboard, one small project a month,
using **free chip samples** and a **low-cost PICkit 3 programmer**. No soldering. No degree needed.

> **Status: first release.** Months 1 and 2 are complete. Their programs are tested in simulation and their wiring is
> machine-checked, but they still need their first **bench test** on real hardware (see
> [the verification log](maintainer/VERIFICATION_LOG.md)). Months 3 to 24 are in preparation.

## Start here

1. [How the course works](start-here/01-how-the-course-works.md) (5 min)
2. [Ordering and budget](start-here/02-ordering-and-budget.md): starter kit and free samples
3. [AVR software and programmer setup](start-here/03-avr-setup.md) (ATmega328P, VS Code + PlatformIO)
4. [PIC software and programmer setup](start-here/04-pic-setup.md) (MPLAB X v6.20, XC8, PICkit 3)
5. [Electronics and breadboard basics](start-here/05-electronics-and-breadboard-basics.md)
6. [Troubleshooting](start-here/06-troubleshooting.md)

## The months

| Month                                           | Project                 | Chips                                   | Status                        |
| :---------------------------------------------: | ----------------------- | --------------------------------------- | ----------------------------- |
|     [1](month-01-electronic-dice/README.md)     | Electronic dice         | PIC16F18857 (+ optional AVR programmer) | complete: awaiting bench test |
| [2](month-02-workshop-command-centre/README.md) | Workshop Command Centre | PIC18F47K42 + MCP23017                  | complete: awaiting bench test |
|                      3–24                       | in preparation          |                                         |                               |

## What is different in this version

* **One folder per month** with the pages, pictures and code together.
* **One short page per build**, each ending in a pass check.
* **Plain-C programs** you can read from top to bottom. No generated code in the early months.
* **Every circuit is drawn from one description** and the breadboard layout is **machine-checked** against the schematic.
* **Hole-by-hole assembly tables** instead of "wire it like the picture".
* **Fault codes** on the heartbeat LED, so a failure tells you *what* failed.
* **Honest status labels** on every page.

## Repository layout

```text
README.md                          this page
start-here/                        introduction, ordering, setup, basics, troubleshooting
month-01-electronic-dice/          pages + images + code, all together
month-02-workshop-command-centre/  pages + images + code, all together
maintainer/                        tests, diagram tools, GitHub guide, verification log
```

## For maintainers and contributors

See [maintainer/README.md](maintainer/README.md).

## Licence

Not yet chosen. See the note in [maintainer/GITHUB_GUIDE.md](maintainer/GITHUB_GUIDE.md#licence).
