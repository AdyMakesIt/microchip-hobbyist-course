# PIC software and programmer setup

**Do this once.** About 30–40 minutes, mostly downloading. This page is for the **PIC chips**. For the ATmega328P (AVR), see [AVR software and programmer setup](03-avr-setup.md).

> **Tested combination (bench-tested on a PIC16F18857 on 2026-08-08):** MPLAB XC8 **v3.10** with the
> PIC16F1xxxx device pack 1.31.465. Use the **MPLAB X IDE v6.20** installer: it is the **last version that supports the PICkit 3**.

## What you will install

| Tool                   | Version                                                                         | What it is                                        |
| ---------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------- |
| **MPLAB X IDE**        | **v6.20**                                                                       | the editor and programming tool                   |
| **MPLAB XC8** compiler | v3.10 (or the version your Microchip download page lists as current for XC8 v3) | turns your C into a program for PIC16/PIC18 chips |

You do **not** need MPLAB Code Configurator (MCC) for months 1 and 2.

## Install MPLAB X IDE v6.20

1. Go to Microchip's [MPLAB X IDE page](https://www.microchip.com/en-us/tools-resources/develop/mplab-x-ide).
   Older versions are in the **Downloads Archive** on that page. Choose **v6.20** for your operating system.
2. Run the installer. Accept the defaults. When it offers **MPLAB IPE** (the stand-alone programmer), keep it ticked.
3. On Windows the installer may also install USB drivers. Allow it.

**Why v6.20 and not the newest?** Microchip stopped supporting the PICkit 3 in newer MPLAB X releases. v6.20 is the final one that still does.
If you later buy a newer programmer (PICkit 4/5 or Snap), you can move to the current version.

## Install the XC8 compiler

1. From the same Microchip site, download **MPLAB XC8** (free edition) and install it with the defaults.
2. Start MPLAB X. Open **Tools → Options → Embedded** and press **Rescan** if the compiler is not listed. XC8 should appear under *Build Tools*.

## Connect the PICkit 3

1. Plug the PICkit 3 into USB. Its light should come on. (A clone's LED behaviour can differ from an original.)
2. The first time it is used, MPLAB X may offer to **update the PICkit 3 firmware**. Accept; it takes under a minute.
   Do not unplug it during the update.

## Create a project

Do this once per build. (Each build is a small project of its own.)

1. **File → New Project → Microchip Embedded → Standalone Project → Next.**
2. **Device:** type the chip: `PIC16F18857` (Month 1) or `PIC18F47K42` (Month 2). **Next.**
3. **Tool:** choose **PICkit 3**. (If the entry is not green or not listed, see [PICkit 3 problems](#pickit-3-problems).) **Next.**
4. **Compiler:** choose **XC8 (v3.10)**. **Next.**
5. **Project name:** for example `M1_Build1`. Put it somewhere short, such as `Documents/MPLABXProjects`. **Finish.**
6. In the **Projects** panel, right-click **Source Files → New → main.c** and delete everything in the new file,
   *or* right-click **Source Files → Add Existing Item** and pick the build's `main.c` from the course folder (choose **Copy** so the course folder stays untouched).
7. If you pasted the code, paste it over the whole file.

### Tell MPLAB X how to power the chip

Your breadboard has its own 5 V supply, so the PICkit 3 must **not** also power the chip:

1. Right-click the project → **Properties → PICkit 3** category.
2. In the drop-down at the top, choose **Power**.
3. **Untick** "Power target circuit from PICkit3". **OK.**

The PICkit 3's VDD wire still connects to the +5 V rail so the programmer can *see* the supply voltage.

## Build and program

1. **Clean and Build** (the hammer-and-broom icon). The **Output** panel should end with **BUILD SUCCESSFUL**.
2. **Make and Program Device** (the icon with a down arrow into a chip). Watch the Output panel: you want **Programming/Verify complete**.
3. The program starts running by itself.

> If you see **warnings** but BUILD SUCCESSFUL, that is fine for now. **Errors** (red) are not.

## If a #pragma config line is rejected

The lines starting `#pragma config` choose how the chip starts: clock, watchdog and so on. The names are written by Microchip's
device header, so a different compiler or device-pack version can occasionally spell one differently. If the compiler complains about one:

1. **Window → Target Memory Views → Configuration Bits.**
2. Set the values in the table for your chip (below). Anything not listed can stay at its default.
3. Click **Generate Source Code to Output.** The Output window shows a block of `#pragma config` lines written by MPLAB itself.
4. Replace the `#pragma config` block at the top of your `main.c` with that block, and rebuild.

**Values to set**

| Setting                          | PIC16F18857 (Month 1)     | PIC18F47K42 (Month 2)                                     |
| -------------------------------- | ------------------------- | --------------------------------------------------------- |
| FEXTOSC (external oscillator)    | OFF                       | OFF                                                       |
| RSTOSC (clock at start-up)       | HFINTOSC 1 MHz (`HFINT1`) | HFINTOSC with HFFRQ = 64 MHz, CDIV 1:1 (`HFINTOSC_64MHZ`) |
| CLKOUTEN                         | OFF                       | OFF                                                       |
| CSWEN (clock switching)          | ON                        | ON                                                        |
| FCMEN (fail-safe clock monitor)  | OFF                       | OFF                                                       |
| MCLRE (reset pin)                | ON                        | (not needed when LVP is ON)                               |
| WDTE (watchdog)                  | **OFF**                   | **OFF**                                                   |
| LVP (low-voltage programming)    | ON                        | ON                                                        |
| XINST (extended instruction set) | n/a                       | **OFF**                                                   |
| CP (code protect)                | OFF                       | n/a                                                       |

The one that matters most is **WDTE = OFF**: left on, the chip resets itself every few seconds and nothing seems to work.

If you had to change the block, please report which name differed so the course can be fixed.

## PICkit 3 problems

| Message or symptom                                     | Try                                                                                                                                                                                                   |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MPLAB X says "no tool found" / PICkit 3 not listed     | another USB port and cable (use a data cable, not charge-only); unplug and re-plug; on Windows check Device Manager for a "PICkit 3" entry                                                            |
| PICkit 3 firmware needs updating, repeatedly           | accept the update once and wait; if it loops, try another USB port; a faulty clone may not hold firmware: try the **MPLAB IPE** instead                                                               |
| **Target device was not found**                        | check the leads are on the **right wires** (pin 1 = MCLR), that **PGD and PGC are not swapped**, the chip has 5 V (measure it), the chip is the right way round, and the 10 kΩ pull-up on pin 1 is in |
| **Target voltage too low / VDD not detected**          | the PICkit's VDD lead must go to the +5 V rail, and the rail must be on                                                                                                                               |
| Device ID mismatch                                     | wrong device chosen in the project, or a bad connection: check the device name against the chip marking                                                                                               |
| Programming succeeds but nothing happens               | watchdog (`WDTE`), configuration, or the wrong hex programmed: do a **Clean and Build**, then program again                                                                                           |
| MPLAB X will not offer PICkit 3 for the chip you chose | the PICkit 3 may not support that device in v6.20: stop and report; do not buy the chip yet                                                                                                           |

## Quick reference

| I want to...              | Do this                                   |
| ------------------------- | ----------------------------------------- |
| compile only              | **Clean and Build** (hammer and broom)    |
| program the chip          | **Make and Program Device**               |
| see the compiler messages | **Window → Output → Output**, tab *Build* |
| start a new build         | **File → New Project**, as above          |

Next: [Electronics and breadboard basics](05-electronics-and-breadboard-basics.md)
