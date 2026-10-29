# Ordering and budget

**Goal:** get your starter kit, and know how to order the free chip samples each month.

## 1. One-time starter kit

Buy this once. Prices are **rough hobby-market guides, not quotes**; they vary by supplier and change often.

| Item                     | What to look for                                                | Rough cost   |
| ------------------------ | --------------------------------------------------------------- | -----------: |
| Solderless breadboard    | 830 tie-points (the full-size kind with 63 columns)             |         £3–6 |
| Breadboard power supply  | MB102 style, with a jumper for 5 V / 3.3 V, USB or barrel input |         £2–4 |
| Jumper wires             | male-to-male, mixed lengths, at least 65                        |         £3–6 |
| Dupont leads             | **female-to-male**, at least 10 (for the PICkit 3 leads)        |         £2–4 |
| Resistor assortment      | ¼ W, E12 range. It will contain 100 Ω, 680 Ω, 4.7 kΩ, 10 kΩ     |         £4–8 |
| LEDs                     | 5 mm red, at least 20                                           |         £2–4 |
| Ceramic capacitors       | assortment that includes 100 nF (0.1 µF)                        |         £3–6 |
| Push buttons             | 6 mm, 4-leg tact switches, at least 10                          |         £2–4 |
| Piezo discs              | **passive** discs (no oscillator inside), at least 2            |         £1–3 |
| Multimeter               | any basic one with continuity beep and DC volts                 |       £10–20 |
| **Programmer: PICkit 3** | an original or a clone, with USB cable                          |       £10–25 |
| USB cables / chargers    | for the PICkit and the breadboard supply                        | have already |

*Optional extras for the Month 1 AVR programmer (Part B) are listed in that part's own page.*

A realistic one-off total is **about £45–£95**, and almost all of it is reusable for all 24 months.

**On clone programmers:** quality varies. A PICkit 3 clone is fine for this course, but if yours is unreliable,
suspect it early (see the [troubleshooting](05-troubleshooting.md)). A clone that works for Month 1 will keep working as the course goes on.

## 2. Free samples

Each month's `README.md` tells you **which two chips to order that month**, with the exact part number and package.
The same rules apply every time:

* **Order three of each chip.** Chips are easy to damage while learning (wrong supply, backwards in the breadboard), and a spare saves waiting a month.
* **Choose the through-hole package** (named SPDIP, PDIP or DIP in the part number's suffix). Surface-mount packages cannot be used on a breadboard.
* **Use the exact part number** from the month's page. Near-identical part numbers can be a different package or a different supply voltage.
* **Check Microchip's current sample rules** (limits per part, per order and per account, and which countries and email addresses qualify) before you order. They change over time.
* **If a chip is out of stock or your order is declined,** report it. The month's page can be changed to suit.

Order the chips for a month **a few weeks before you need them**, since delivery times vary.

## 3. Buying the small parts

* **Resistors, LEDs, capacitors, switches, wire:** assortment kits from a marketplace are fine, and cost less than buying each value separately.
* **If you prefer to buy exactly what you need:** a general electronics distributor works, but postage often costs more than the parts. The assortments are better value.
* **Chips:** the free samples come from Microchip itself. **Avoid buying microcontrollers from marketplace sellers** (counterfeit and remarked chips exist).

## 4. What each month needs

Each month's `README.md` has a **parts list counted automatically from that month's circuit**, with a margin
("Buy at least"). Buy the larger number so you always have spares.

Next: [Software and programmer setup](03-software-setup.md)
