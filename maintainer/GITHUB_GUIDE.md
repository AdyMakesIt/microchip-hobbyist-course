# GitHub guide

How to publish the course, keep each month's bundle together, and let other people help. Written for someone who has not used Git much.

## The short answer

* **One repository** for the whole course (call it `microchip-hobbyist-course` or similar).
* **One folder per month** inside it, exactly as in this package. That folder *is* the monthly bundle: pages, pictures, code.
* GitHub shows `.md` files as nicely formatted pages, with images, tables and links working as they do here. Nothing needs converting.
* For people who want a download rather than a website, attach a **ZIP of each month** to a **GitHub Release**.

## Setting it up (one time)

1. Create a free account at github.com.
2. Install **GitHub Desktop** (a friendly app, no command line needed), or Git if you prefer.
3. In GitHub Desktop: **File → New repository**, name it, and choose a local folder. Tick **Add .gitignore: none** (this package already has one) and choose a licence later (see below).
4. Copy the contents of this package into that folder.
5. In GitHub Desktop you will see the files listed. Write a summary such as "Months 1 and 2" and press **Commit to main**, then **Publish repository**.

Make the repository **public** when you are ready to share, or **private** while you test.

## Day-to-day routine

```text
change something  ->  python3 maintainer/tools/check_all.py  ->  commit in GitHub Desktop  ->  Push origin
```

Commit small and often. Each commit message should say what and why ("Month 2: fix SDA hole in build 2 table").

## Keeping each month together

Because every month already has its own folder, this is automatic. Three ways to give people a monthly bundle:

| Method                                                         | Effort       | Good for                                    |
| -------------------------------------------------------------- | ------------ | ------------------------------------------- |
| **Browse the folder** on GitHub                                | none         | reading online; Markdown renders everywhere |
| **Download ZIP** of the whole repository (green *Code* button) | none         | getting everything                          |
| **Release with one ZIP per month**                             | a few clicks | people who only want Month 3                |

**To make monthly ZIPs:** run `python3 maintainer/tools/make_month_zips.py`. It writes `dist/month-NN-....zip`, `dist/start-here.zip` (each also contains the root `README.md`).
Then on GitHub: **Releases → Draft a new release → choose a tag (`month-02-v1.0`) → drag the ZIP in → Publish**.
`dist/` is ignored by Git on purpose: the ZIPs belong on the Release page, not in the repository.

*Optional, later:* GitHub Actions can build the ZIPs automatically when you create a tag. That is a nice-to-have; do it by hand until the course settles.

## Where do the MPLAB X projects go?

Right now each build has a single `main.c` and the learner creates the MPLAB project themselves ([setup guide](../start-here/03-software-setup.md#create-a-project)).
That is deliberate: a project file written by hand and never opened in MPLAB can fail in ways nobody can diagnose.

**Once a build has compiled and run on your bench**, you can add the real project:

1. In MPLAB X, make the project inside the build's code folder, for example `month-02-.../code/build-2-hello-expander/Month2_Build2.X`.
2. Commit the **`.X` folder** (the `.gitignore` already leaves out `build/`, `dist/` and `debug/`).
3. Note in [the verification log](VERIFICATION_LOG.md) the MPLAB X, XC8 and device-pack versions it was built with.

A learner can then open the `.X` folder directly. This is how a build graduates from "draft" to "tested".

## Releasing and versions

* Do **not** put versions in file names. Use **tags** and the [changelog](../CHANGELOG.md).
* Tag a month when it has been bench-tested: `month-02-v1.0`. After later corrections: `month-02-v1.1`.
* A suggestion for the repository as a whole: `v0.x` while months are drafts, `v1.0` when the first six months are bench-tested.

## Letting people report problems

* Turn on **Issues**. The `.github/ISSUE_TEMPLATE/bench-report.md` template asks for the month, build, tool versions and exact message.
* Ask people to **attach a photo** of their breadboard. It is the quickest way to see a wiring slip.
* Label reports `bench-report`, `typo`, `wiring`, `code`. Turn each confirmed bench report into an edit to the page *and* a line in the verification log.

## Showing it as a website (optional)

GitHub can host the Markdown as a website with **GitHub Pages**. The simplest route is to do nothing: the repository's own pages already look good.
If you later want a searchable site with a left-hand menu, tools such as MkDocs read this same folder structure without changes to the pages.
Do not do this until the content is stable.

## Licence

Public repositories without a licence are, in law, *all rights reserved*: others may read but not reuse. Choose deliberately:

| For                             | Common choice                  | Meaning in one line                                |
| ------------------------------- | ------------------------------ | -------------------------------------------------- |
| the text, pictures and diagrams | **Creative Commons BY-SA 4.0** | share and adapt, with credit, under the same terms |
| the `main.c` code               | **MIT**                        | do what you like with it, keep the notice          |

GitHub can add the licence file for you (**Add file → Create new file**, name it `LICENSE`, and click *Choose a license template*).
Decide this before sharing widely. It is your call; get legal advice if it matters commercially.

## Things to avoid

* Do **not** commit Microchip's datasheets or software installers; link to them instead (their licence terms differ).
* Do **not** commit your computer's `build/` and `dist/` folders (they are in `.gitignore`).
* Do **not** copy text from Microchip's documentation into pages; summarise it in your own words and link.
