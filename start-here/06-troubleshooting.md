# Troubleshooting: the ladder

When something does not work, **do not guess; climb this ladder one rung at a time**. Each rung tells you which half of the problem you are in.
Most faults are found by rung 4.

## Rung 1: Power off. Look.

* Is every chip the **right way round** (notch left) and **pushed fully in**?
* Are any legs bent under the chip instead of in the holes?
* Is there a **wire in the wrong hole** (one column out is the commonest mistake)? Compare each wire with the hole-by-hole table, one at a time, ticking them off.
* Does any resistor or LED leg touch another?

## Rung 2: Power off. Beep.

Use continuity to check, for each chip, that **every VDD and VSS pin** reaches the right rail, and that **+5 V and GND are not connected** to each other.

## Rung 3: Power on. Measure.

* DC volts between the chip's VDD and VSS pins: **4.8–5.2 V**. If not, check the supply jumper is on 5 V.
* Touch a chip. If it is **warm or hot**, power off at once.
* Check the reset pin (MCLR) reads **about 5 V** (not 0).

## Rung 4: Does the programmer connect?

In MPLAB X press **Make and Program Device**. Possible answers:

| Result                    | Meaning                                                                                              |
| ------------------------- | ---------------------------------------------------------------------------------------------------- |
| "Target device not found" | the chip is not powered or the programmer leads are wrong (rungs 1–3, then check the leads)          |
| Programs and verifies     | power, reset and leads are good; the problem is in the **program** or the **circuit after the chip** |

If it programs, **you are over the hardest hill.** Everything from here is about *what* the chip does.

## Rung 5: Prove the chip runs

Go back to the Blink build (Month 1 Build 1 or Month 2 Build 1) and program it. If the LED blinks, the chip, clock and programmer are fine.
If it does not, the problem is the LED circuit or configuration, not your new work.

## Rung 6: Prove the new part, alone

Disconnect everything you added in the failing build except what you are testing. Test one part at a time.

## Rung 7: Use the fault code (Month 2 onwards)

From Month 2 the heartbeat LED blinks a number of times when something fails, rather than staying silent.
See the table in [Month 2 Build 2](../month-02-workshop-command-centre/build-2-hello-expander.md#fault-codes-the-heartbeat-led-is-talking-to-you).

## Habits that save hours

* **Photograph** a working board before you change anything.
* **Change one thing at a time.**
* **Write down what you tried.** A list stops you repeating the same test.
* If it worked yesterday and not today, suspect **a loose wire** first and the software last.
* When you are tired, stop. Faults seem to vanish after a night's sleep because you stop making the same mistake.

## Special case: 3.3 V chips

If a 3.3 V board (Month 5) misbehaves: **measure the supply first**. Check it reads 3.2–3.4 V at the chip, that the **VCAP** capacitor is in place, and that nothing 5 V is connected to the board.
