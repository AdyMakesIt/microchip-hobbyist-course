# Microchip Hobbyist Course

Learn to build with Microchip's **PIC** and **AVR** microcontrollers on a breadboard, one small project a month,
using **free chip samples** and a **low-cost PICkit 3 programmer**. No soldering. No degree needed.

> **Status: Months 1 to 5 are complete.** Their programs are tested in simulation and their wiring is machine-checked,
> but they still need their first **bench test** on real hardware (see [the verification log](maintainer/VERIFICATION_LOG.md)).
> Months 6 to 24 are in preparation.

## Start here

1. [How the course works](start-here/01-how-the-course-works.md) (5 min)
2. [Course overview](start-here/course-overview.md): what you will build in each of the 24 months
3. [Ordering and budget](start-here/02-ordering-and-budget.md): how ordering works
4. [Purchasing plan](start-here/purchasing-plan.md): what to order each month, and what to buy ahead
5. [Parts catalogue](start-here/parts-catalogue.md): specifications and links for every part
6. [AVR software and programmer setup](start-here/03-avr-setup.md) (ATmega328P, VS Code + PlatformIO)
7. [PIC software and programmer setup](start-here/04-pic-setup.md) (MPLAB X v6.20, XC8, PICkit 3)
8. [Electronics and breadboard basics](start-here/05-electronics-and-breadboard-basics.md)
9. [Troubleshooting](start-here/06-troubleshooting.md)
10. [Taking a project further](start-here/07-taking-a-project-further.md): KiCad and PCBs

## The months

| Month                                           | Project                               | Chips                           | Status                        |
| :---------------------------------------------: | ------------------------------------- | ------------------------------- | ----------------------------- |
|     [1](month-01-electronic-dice/README.md)     | Electronic dice (AVR first, then PIC) | ATmega328P + PIC16F18857        | complete: awaiting bench test |
| [2](month-02-workshop-command-centre/README.md) | Workshop Command Centre               | PIC18F47K42 + MCP23017          | complete: awaiting bench test |
|     [3](month-03-analogue-in-out/README.md)     | Analogue in, analogue out             | PIC18F47K42 + MCP3008 + MCP4822 | complete: awaiting bench test |
|      [4](month-04-binary-clock/README.md)       | The binary clock                      | PIC16F18446 + MCP7940N          | complete: awaiting bench test |
| [5](month-05-sixteen-bit-and-memory/README.md)  | A 16-bit chip at 3.3 V                | PIC24FJ64GA002 + 24LC512        | complete: awaiting bench test |
|                      6–24                       | in preparation                        |                                 |                               |

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
start-here/                        introduction, overview, ordering and purchasing, setup, basics, troubleshooting
month-01-electronic-dice/          pages + images + code, all together
month-02-workshop-command-centre/  pages + images + code, all together
month-03-analogue-in-out/          (and months 4 and 5, the same layout)
maintainer/                        tests, diagram tools, GitHub guide, verification log
```

## For maintainers and contributors

See [maintainer/README.md](maintainer/README.md).

## Licence

Not yet chosen. See the note in [maintainer/GITHUB_GUIDE.md](maintainer/GITHUB_GUIDE.md#licence).
