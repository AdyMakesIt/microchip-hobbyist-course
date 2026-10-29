# Authoring guide: how to write a new month

## The rules

1. **One folder per month**, named `month-NN-short-name`. Pages, `images/` and `code/` all inside it.
2. **One page per build**, with the same eight sections as every other build (goal, what you are building, build it, check before power, program it, pass check, if it does not work, try this).
3. **A build is one small step** that ends in something visible. Aim for 3 or 4 builds a month.
4. **Plain C first.** No generated code (MCC) in the early months. One `main.c` per build, complete on its own.
5. **One new idea per month.** Do not introduce a new chip family and a new peripheral in the same month if you can avoid it.
6. **Isolate fragile things.** Compiler-specific names (the `#pragma config` block) are in one marked block at the top of every file, with a documented fallback.
7. **Every build must have a fault indicator** where a silent failure is likely (a blink code, an LED, a serial message).
8. **Never put a version number in a file name.** Versions go in `CHANGELOG.md` and git tags.
9. **State your confidence.** A page says what has been checked ([levels](VERIFICATION_LOG.md)). Do not call a build tested until it has been on a bench.
10. **Do not copy boilerplate.** Anything true for every month lives once in `start-here/` and is linked.

## Steps

1. Add the month's chips and circuit to `tools/circuits.py` (schematic chains, then breadboard holes, with a `build` number for each item).
2. Run `python3 maintainer/tools/make_all.py`. If the checker complains, the layout does not match the schematic: fix it before going on.
3. Write each `main.c` in `code/build-N-name/`.
4. Add logic tests in `sim/` (copy the nearest existing month). **Break the code on purpose** and make sure the tests notice.
5. Copy a build page as a template. Put the markers `<!-- code:... -->`, `<!-- placement:N -->`, `<!-- connections:N -->`, `<!-- bom -->` where the generated content belongs.
6. Run `python3 maintainer/tools/check_all.py`.
7. Update [VERIFICATION_LOG.md](VERIFICATION_LOG.md) and the `README.md` month table.
8. Bench-test. Fix. Change the status line on each page to **bench tested** only then.

## Page template (build)

```markdown
# Month N · Build K – Title

[← previous](...) · [Month N](README.md) · [Next →](...)

**Goal:** one sentence.
**Status:** logic tested in simulation · compile and bench test pending

## 1. What you are building      (schematic image + what each part does)
## 2. Build it                   (breadboard image + <!-- placement:K --> + <!-- connections:K -->)
## 3. Check before you power it  (3-5 multimeter checks)
## 4. Program it                 (<!-- code:... --> + how it works)
## 5. Pass check                 (tick boxes)
## 6. If it does not work        (table: what you see | likely cause | what to do)
## 7. Try this                   (optional)
```

## Style

* Short sentences. Say what each part is *for* the first time it appears.
* Use hole names (**16b**) and pin numbers, never "next to the chip".
* Explain **why** a rule exists once (decoupling capacitor, pull-up), then link back.
* Tables for lists of facts, prose for reasons.
