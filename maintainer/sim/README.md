# Logic tests

These tests run each build's **unmodified `main.c`** on a PC against a model of the chip's pins, the I2C bus and (for Month 2) an MCP23017 that follows
the datasheet protocol. They need only `g++` (any recent version).

```sh
sh maintainer/sim/m1/run_tests.sh     # Month 1
sh maintainer/sim/m2/run_tests.sh     # Month 2
```

## What they prove

* register values written to the MCP23017, read-back, address and register numbers
* the I2C sequence (START, address, register, repeated START, read, STOP) and **timing** against the standard-mode limits (4.7 µs / 4.0 µs)
* LED, button, mode, speed and piezo behaviour as described on each page, including contact bounce and long presses
* fault codes (1, 2 and 3 blinks) when the expander is missing, refuses a read, or reads back wrongly
* the dice show all six legal faces and roll **once** per press

## What they cannot prove

* that **XC8 accepts the code** (for example a `#pragma config` name): only the real compiler can say
* that the **configuration values** really give the clock speed the code assumes
* anything about **wiring, contacts, or chips** on a real breadboard
* real timing (the model counts the programmed delays, plus about 20 µs per pin read in Month 1)

## How they were checked

Each test was run against deliberately broken copies of the code (wrong address, missing pull-up, no edge detection, short I2C delays,
bad table values, off-by-one wraps). Every injected fault was caught, apart from one "equivalent" mutant where removing a start-of-roll debounce makes no difference,
because the roll animation takes much longer than any bounce.

The files `xc.h` here are stand-ins for Microchip's `<xc.h>`; they are not used in a real build.
