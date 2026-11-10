# Month 5 – A 16-Bit Chip at 3.3 V (PIC24FJ64GA002 and 24LC512)

**Time:** three or four evenings  **Chips:** PIC24FJ64GA002 and 24LC512, both free samples  **Supply:** **3.3 V** (not 5 V)
**Everything for this month is in this folder:** pages, pictures and code.

You move up to a **16-bit** microcontroller from Microchip's PIC24 family, and meet an **EEPROM**: memory that keeps its contents when the power is off. You will make a counter that remembers how many times the board has been switched on.

New this month:

* **3.3 V.** This chip runs from 3.3 V. It is **not** safe on 5 V. Every part on the board runs at 3.3 V.
* **A new compiler (XC16)** and a few differences from the PIC16 and PIC18 chips.
* **EEPROM:** a 16-bit address, page writes, and the 5 ms "write cycle" you wait out with **ACK polling**.

## The three builds

Do them in order. Each ends with a **pass check**.

| #   | Build                                                     | You add                                     | You prove                                    |
| :-: | --------------------------------------------------------- | ------------------------------------------- | -------------------------------------------- |
|  1  | [Blink at 3.3 V](build-1-blink.md)                        | the PIC24, power, programmer leads, one LED | the chip, the 3.3 V supply and XC16 all work |
|  2  | [Say hello to the EEPROM](build-2-eeprom-hello.md)        | the 24LC512, eight LEDs                     | you can store and fetch a byte               |
|  3  | [Memory that survives power-off](build-3-boot-counter.md) | a button                                    | a counter that remembers across power cycles |

**Status:** the logic of all three programs, including the I2C conversation with a simulated EEPROM (16-bit addresses, pages, the 5 ms busy time, and several simulated power cycles),
has been tested (see [`../maintainer/VERIFICATION_LOG.md`](../maintainer/VERIFICATION_LOG.md)). The wiring pictures are machine-checked against the schematics.
Nothing here has been run on a real bench yet. If something does not work, that is useful information, so please report it.

## What you need

### Free samples (order these in month 5)

| Part                                   | Order | Used for             |
| -------------------------------------- | ----: | -------------------- |
| **PIC24FJ64GA002-I/SP** (28-pin SPDIP) |     3 | the main chip        |
| **24LC512-I/P** (8-pin PDIP)           |     3 | the 64 KB I2C EEPROM |

### Parts used (counted automatically from the circuit)

<!-- bom -->
| Part                                                     | Value            | Qty used | Buy at least |
| -------------------------------------------------------- | ---------------- | -------: | -----------: |
| Resistor                                                 | 10 kΩ            |        2 |            3 |
| Resistor                                                 | 330 Ω            |        9 |           11 |
| Resistor                                                 | 4.7 kΩ           |        2 |            3 |
| Ceramic capacitor                                        | 100nF            |        2 |            3 |
| Ceramic capacitor                                        | 10uF             |        1 |            2 |
| LED, 5 mm                                                | red              |        9 |           11 |
| Push button (4-leg tact switch)                          | 6 mm             |        1 |            2 |
| Jumper wires, solid or male-to-male                      | assorted lengths |       30 |           36 |
| Female-to-male Dupont leads (PICkit 3 ICSP → breadboard) |                  |        5 |            6 |
<!-- /bom -->

**One part needs care:** the **10 µF capacitor on pin 20 (VCAP)**. The chip has a small internal regulator that makes its 2.5 V core supply, and that regulator needs a capacitor to be stable.
Use a **10 µF ceramic** (or tantalum) capacitor, not an ordinary aluminium electrolytic: the datasheet asks for low ESR (a "good quality" capacitor). If you use a polarised one, its **+** leg goes to the chip.

### Tools

Everything from Month 4, plus the **XC16 compiler** (free): see the [PIC setup page](../start-here/04-pic-setup.md#pic24-and-dspic-the-xc16-compiler).

## Before you start: the 3.3 V rule

1. Set **both** supply jumpers on your breadboard power module to **3.3 V**.
2. **Measure the rails with the multimeter before the chip goes in.** They must read **3.2 V to 3.4 V**.
3. **Never connect a 5 V signal to this board.** This chip's supply must stay between 2.0 V and 3.6 V; 5 V can destroy it.
4. The LEDs use **330 Ω** resistors this month (not 680 Ω), because at 3.3 V 680 Ω gives only a dim glow.

## Ready-made projects and hardware files

* **Working projects:** [`projects/`](projects/README.md) holds complete, ready-to-open projects for the builds (MPLAB X).
* **Hardware files:** [`hardware/`](hardware/README.md) holds the KiCad schematic location, a **parts list** and a **connection list** you can use to design a PCB. See [Taking a project further](../start-here/07-taking-a-project-further.md).

## Folder contents

```text
month-05-sixteen-bit-and-memory/
  README.md                          this page
  build-1-blink.md ... build-3-boot-counter.md
  images/                            schematic + breadboard picture for every build
  projects/              ready-to-open projects (see projects/README.md)
  hardware/              KiCad schematic, parts list and connection list
  code/
    build-1-blink/main.c             one complete file per build
    build-2-eeprom-hello/main.c
    build-3-boot-counter/main.c
```
