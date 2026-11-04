# AVR software and programmer setup (ATmega328P)

**Do this once.** About 30–45 minutes. This page is for the **AVR track** of Month 1 and any later month that uses an AVR chip.
The PIC chips have their own set-up: [PIC software and programmer setup](04-pic-setup.md).

## The idea: what the Arduino IDE was hiding

If you have used an Arduino, you have already used two tools without knowing it:

| Job                               | The tool that does it     | In the Arduino IDE you pressed... |
| --------------------------------- | ------------------------- | --------------------------------- |
| turn your C/C++ into machine code | **avr-gcc** (a compiler)  | Verify                            |
| send that code into the chip      | **avrdude** (an uploader) | Upload                            |

Here you will run the **same two tools** yourself, through buttons in VS Code. The ATmega328P chip is the same chip that is
on an Arduino Uno. What changes is that you write plain C, you decide the settings, and you can see every step.

### What you already know, in plain C

| Arduino                       | Plain C on the ATmega328P                                 |
| ----------------------------- | --------------------------------------------------------- |
| `setup()` and `loop()`        | `main()` with a `while (1)` loop                          |
| `pinMode(pin, OUTPUT);`       | set a bit in the **DDR** register: `DDRD \|= (1 << PD0);` |
| `digitalWrite(pin, HIGH);`    | set a bit in **PORT**: `PORTD \|= (1 << PD0);`            |
| `digitalWrite(pin, LOW);`     | clear it: `PORTD &= ~(1 << PD0);`                         |
| `digitalRead(pin)`            | read the **PIN** register: `PINC & (1 << PC0)`            |
| `pinMode(pin, INPUT_PULLUP);` | `DDRC &= ~(1 << PC0);` then `PORTC \|= (1 << PC0);`       |
| `delay(500);`                 | `_delay_ms(500);` (needs `F_CPU`, the clock speed)        |

Pins are grouped in **ports** of up to eight: **PB**0 to 7, **PC**0 to 5 and **PD**0 to 7 on the ATmega328P. The Arduino pin numbers
(D0 to D13, A0 to A5) are just names for these.

## What you need

| Item                      | What                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------ |
| Computer editor           | **VS Code** (you have it)                                                            |
| Build and upload tools    | **PlatformIO** (a free VS Code extension that installs avr-gcc and avrdude for you)  |
| **A programmer, one of:** | a **USBasp**, or an **Arduino Uno R3** acting as a programmer (both explained below) |
| Chip                      | ATmega328P-PU on the breadboard                                                      |

You need only **one** of the two programmers. Choose with this table:

|                   | **USBasp**                       | **Arduino Uno R3 as programmer**              |
| ----------------- | -------------------------------- | --------------------------------------------- |
| Cost              | about £2–5                       | free if you already own an Uno                |
| One-off set-up    | none (Windows may need a driver) | load a free example program onto the Uno once |
| Wires to the chip | 5                                | 5                                             |
| Speed             | fast                             | slower (still fine for this course)           |
| Good when         | you want it to "just work"       | you already have an Uno and Arduino IDE       |

## Step 1: Install PlatformIO in VS Code

1. Open VS Code. Open the **Extensions** panel (the four-squares icon).
2. Search for **PlatformIO IDE** and click **Install**. The first install takes several minutes: it downloads tools in the background.
3. When it asks, **reload VS Code**. A small ant-head icon and a blue bar with new buttons appear at the bottom.

## Step 2: Make an AVR project

1. Make a folder for the build, for example `Month1_AVR_Build1`, and open it in VS Code (**File → Open Folder**).
2. Inside it create a folder called `src` and, in `src`, a file called `main.c`. Paste the build's code into it.
3. In the project folder (next to `src`) create a file called `platformio.ini` with the contents for your programmer (below).

**If you use a USBasp:**

```ini
[env:atmega328p]
platform = atmelavr
board = ATmega328P
board_build.f_cpu = 1000000L
upload_protocol = usbasp
upload_flags =
    -Pusb
    -B10
```

**If you use an Arduino Uno R3 as a programmer** (change `COM3` to your Uno's port; on Linux or macOS it looks like `/dev/ttyACM0`):

```ini
[env:atmega328p]
platform = atmelavr
board = ATmega328P
board_build.f_cpu = 1000000L
upload_protocol = stk500v1
upload_port = COM3
upload_speed = 19200
upload_flags =
    -P$UPLOAD_PORT
    -b$UPLOAD_SPEED
```

What the lines mean:

* `board = ATmega328P` is the bare chip (not an Arduino board).
* `board_build.f_cpu = 1000000L` tells the compiler the chip runs at **1 MHz**: that is the chip's factory setting.
* `upload_protocol` picks the uploader's language for your programmer.
* `-Pusb` tells avrdude to look for the USBasp on USB; `-B10` slows the programming clock (explained in the next section).

## Step 3: Build and upload

Use the buttons in the blue bar at the bottom of VS Code:

| Button    | What it does                                | Arduino equivalent |
| --------- | ------------------------------------------- | ------------------ |
| ✓ (tick)  | **Build**: compile with avr-gcc             | Verify             |
| → (arrow) | **Upload**: compile, then send with avrdude | Upload             |

A good result ends with **SUCCESS** in the terminal. For an upload you will also see avrdude's lines, including *"avrdude: 1234 bytes of flash verified"*.

### What PlatformIO is really running

You can do the same three steps by hand in any terminal, which is exactly what the Arduino IDE did for you:

```text
avr-gcc -mmcu=atmega328p -DF_CPU=1000000UL -Os -Wall -o main.elf main.c
avr-objcopy -O ihex -R .eeprom main.elf main.hex
avrdude -c usbasp -p m328p -B 10 -U flash:w:main.hex:i
```

1. **Compile and link** `main.c` into `main.elf`.
2. **Convert** it into a `.hex` file, the plain-text format of the chip's program.
3. **Upload** the `.hex` through the programmer into the chip's flash memory.

## Programmer A: the USBasp

**Wiring.** Power the chip from your breadboard supply, **not** from the USBasp. Connect only the signal wires and ground:

| Chip pin          | Signal | USBasp 6-pin header pin |
| :---------------: | ------ | :---------------------: |
|        18         | MISO   |            1            |
| *(not connected)* | VCC    |            2            |
|        19         | SCK    |            3            |
|        17         | MOSI   |            4            |
|         1         | RESET  |            5            |
|     GND rail      | GND    |            6            |

The 6-pin header numbering above is the standard AVR ISP one: pin 1 is marked on the board (often by a dot or square). Some USBasp boards have a 10-pin
header instead; the signals are the same, and a printed pinout is usually on the board or in the seller's page.

**Do not connect the VCC pin.** If the USBasp supplies 5 V while your breadboard supply is also on, the two supplies fight.

**Slow clock.** A brand-new ATmega328P runs at 1 MHz, and the programming clock must be slower than **one quarter** of the chip's clock (under 250 kHz).
Many USBasps default to a faster clock, which makes a fresh chip look "dead". The `-B10` flag in the file (and the avrdude lines) slows it down to about 100 kHz. Some USBasp boards also have a **slow SCK** jumper that does the same.

**Windows driver.** If Windows does not recognise the USBasp, a driver such as *libusb-win32* or *WinUSB* can be assigned to it with the free **Zadig** tool.
Linux sometimes needs a small "udev rule" to let a normal user access the USBasp. macOS usually just works.

## Programmer B: an Arduino Uno R3 as programmer

An Uno can become an AVR programmer by loading a standard example program called **ArduinoISP**. You do this **once**, with the Arduino IDE.

**Prepare the Uno (once)**

1. Open the Arduino IDE. **File → Examples → 11.ArduinoISP → ArduinoISP.**
2. **Tools → Board → Arduino Uno.** **Tools → Port →** your Uno.
3. **Sketch → Upload.** Wait for **Done uploading.** The Uno is now a programmer.

**Wiring** (the chip stays powered by your breadboard supply; connect the Uno's **GND** to the breadboard's GND, and leave the Uno's 5 V pin unconnected):

| Uno pin | Chip pin | Signal |
| :-----: | :------: | ------ |
|   D13   |    19    | SCK    |
|   D12   |    18    | MISO   |
|   D11   |    17    | MOSI   |
|   D10   |    1     | RESET  |
|   GND   | GND rail | ground |

**Using it.** Put the Uno's COM port in `upload_port` in `platformio.ini` (the second file above), and press **Upload** in VS Code.

**If you get "not in sync" or "programmer is not responding":** when avrdude opens the Uno's port, the Uno resets itself (that is its auto-reset). Fit a **10 µF electrolytic capacitor**
between the Uno's **RESET** pin (long leg, +) and **GND** (short leg, −) while programming. Remove it before you next upload to the Uno from the Arduino IDE.

## Check the connection before anything else

With the chip wired, powered and the programmer attached, ask the chip to identify itself. This proves the wiring and the programmer before you involve any program:

```text
avrdude -c usbasp -p m328p -B 10
```

For the Uno programmer use `-c stk500v1 -P COM3 -b 19200 -p m328p`. A good answer includes:

```text
avrdude: Device signature = 0x1e950f
```

(`0x1e950f` is the ATmega328P's identity.) If you instead see a signature of `0x000000` or `0xffffff`, or an "initialization failed" error, the programmer is not talking to the chip: go to the table below.

Where is avrdude? PlatformIO installs its own copy in its `packages` folder. The simplest test is to press **Upload** and read the first lines of its output; a signature error shows
up there. If you prefer, install avrdude separately (Linux: `sudo apt install avrdude`; macOS: Homebrew; Windows: from the AVRDUDE releases page).

## Leave the fuses alone

An AVR chip stores a few settings called **fuses**: which clock to use, whether the reset pin works, and so on. The chip leaves the factory using its **internal 8 MHz oscillator divided by 8, which is 1 MHz**.
That is what this course uses, so **you never need to touch the fuses in Month 1.**

Do not experiment with fuse values yet. Choosing the wrong clock source (for example, an external crystal that is not there) can make the chip unreachable until a clock is supplied. Fuses are explained properly in [Month 1 Part B](../month-01-electronic-dice/avr-programmer/README.md).

## Troubleshooting

| What you see                                         | Most likely cause                                                 | What to do                                                                              |
| ---------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `Device signature = 0x000000` or `0xffffff`          | no power, or a wire is wrong                                      | measure 5 V on pin 7 and 20; check MISO, MOSI, SCK, RESET each go to the right chip pin |
| `initialization failed, rc=-1` (USBasp)              | USBasp not seen, or fresh chip too slow for the programming clock | another USB port; driver (Zadig); keep `-B10`; slow-SCK jumper                          |
| `could not find USB device`                          | driver missing                                                    | Zadig on Windows; udev rule on Linux                                                    |
| `not in sync` (Uno programmer)                       | the Uno auto-reset                                                | 10 µF capacitor from the Uno's RESET (+) to GND (−)                                     |
| Programming works, nothing happens                   | LED backwards, wrong pin, or old program                          | check the build's wiring table; re-upload                                               |
| LED blinks, but at the wrong speed                   | `F_CPU` does not match the real clock                             | keep the factory fuses; check `board_build.f_cpu = 1000000L`                            |
| `main.c: undefined reference to main` or "no source" | `main.c` is not in the `src` folder                               | the file must be `src/main.c`                                                           |
| Build works but upload is very slow                  | normal for the Uno programmer                                     | wait: a small program takes a few seconds                                               |

Next: [PIC software and programmer setup](04-pic-setup.md) (needed for the PIC track), or go straight to [Month 1](../month-01-electronic-dice/README.md).
