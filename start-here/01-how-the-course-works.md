# How the course works

**Read time: 5 minutes.**

## The idea

Microchip gives away a small number of sample chips for free. This course turns that into a self-taught path:
each month you order two free chips, build something with them on a breadboard, and learn one new idea.
After 24 months you have a drawer full of real parts and hands-on experience with Microchip's PIC and AVR families,
for the cost of a modest starter kit plus resistors, LEDs and wire.

It is written for **keen amateurs**. No electronics degree, no soldering, no expensive tools. The programmer is a
**PICkit 3** (cheap clones are common) rather than a costly modern debugger.

## How a month is laid out

Every month is one folder. Everything for that month sits inside it:

```text
month-NN-name/
  README.md        what you build, what to order, the list of builds
  build-1-....md   one short page per build
  build-2-....md
  images/          a schematic and a breadboard picture for every build
  code/            one folder per build, each with a complete main.c
```

A **build** is one small step that ends with something you can see working. You never build more than one step at a time.

## Every build page has the same sections

1. **Goal**: one sentence.
2. **What you are building**: the schematic, in plain words.
3. **Build it**: a picture of the breadboard plus a hole-by-hole table.
4. **Check before you power it**: a few multimeter checks that save chips.
5. **Program it**: the complete code, and how it works.
6. **Pass check**: tick boxes. If they are not all ticked, you are not done.
7. **If it does not work**: the likely causes, most likely first.
8. **Try this**: optional experiments.

## Four rules that prevent most problems

1. **Power off before you change the wiring.** Always. Including the programmer leads.
2. **Pass each build before starting the next.** The next build assumes the last one works.
3. **Measure before you power on.** The checks take two minutes.
4. **Change one thing at a time.** If it stopped working, undo the last change.

## What "status" on each page means

Each build page shows how far it has been checked. We are honest about this:

| Level                          | Meaning                                                                                                                                                                      |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Logic tested in simulation** | the program was run on a PC against a model of the chip's pins and the other chips, and behaved as described (see [the verification log](../maintainer/VERIFICATION_LOG.md)) |
| **Compiled**                   | built with Microchip's XC compiler without errors                                                                                                                            |
| **Bench tested**               | built on a real breadboard and every pass check ticked                                                                                                                       |

A build is only "finished" when it is **bench tested**. Until then, treat the pages as a careful draft and tell us what you find.

## Reporting a problem

If a pass check fails and you have followed the troubleshooting table, note: the page, the step, what you expected, what you saw,
and the exact compiler/programmer message. That is enough to fix the page for everyone.

## Where to go next

1. [Ordering and budget](02-ordering-and-budget.md)
2. [Software and programmer setup](03-software-setup.md)
3. [Electronics and breadboard basics](04-electronics-and-breadboard-basics.md)
4. [Month 1](../month-01-electronic-dice/README.md)
