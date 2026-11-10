# Taking a project further: KiCad and PCBs

A breadboard is for learning and testing. When a project works and you want something permanent, smaller or neater, the next step is a **printed circuit board (PCB)**.
The course gives you a head start.

## What each month gives you

Every month's `hardware/` folder contains:

| File                    | What it is                                                                                |
| ----------------------- | ----------------------------------------------------------------------------------------- |
| `exports/*-bom.csv`     | the **parts list**: every part, its value, and a *suggested* KiCad footprint              |
| `exports/*-netlist.csv` | the **connection list**: every wire, as the pins it joins                                 |
| `kicad/`                | the **KiCad schematic**, when one has been drawn (see the status table in the repository) |

The pictures in `images/` are for building on a breadboard; these files are for designing a board.

## A first PCB in six steps

1. **Install KiCad** (free) and make a new project for the month.
2. **Draw the schematic.** Use the connection list to place each part and wire it. KiCad's library has symbols for most parts; search the part number. If one is missing, KiCad's symbol editor makes one from the datasheet.
3. **Assign footprints.** Start from the suggestions in the parts list, then **check each against your real part** (a resistor's lead spacing, an LED's size, a crystal's shape).
4. **Run the electrical rules check** in KiCad, and compare your schematic with the connection list.
5. **Lay out the board.** Keep each chip's 100 nF capacitor next to its power pins, keep wires short, and keep the programmer header's pins free of other loads.
6. **Run the design rules check**, export the files, and send them to a PCB manufacturer. Boards can cost a few pounds for a small batch.

## Things a breadboard let you get away with

* **A programming header.** Add the 5- or 6-pin header for the PICkit 3 or ISP programmer, wired as in the schematic, so you can still change the program.
* **Power.** Add a connector and a regulator if the board will not sit on a breadboard supply. Check the voltage each chip wants (Month 5's PIC24 is 3.3 V only).
* **Pull-ups and decoupling.** Keep every pull-up and every capacitor from the schematic. They matter more on a PCB, not less.
* **Crystals.** Place them close to the chip, with the load capacitors, and follow the datasheet's layout advice.
* **Test points.** Add pads for the signals you probed with a multimeter.

## Before you order boards

* The project should have passed **every pass check** on the breadboard first.
* Print the board at 1:1 scale on paper and lay your real parts on it to check the footprints.
* Treat the first board as a **prototype**. Expect to change something.

If you design a board for one of the projects, consider sharing it: see the notes in the repository's maintainer guide on committing KiCad files.
