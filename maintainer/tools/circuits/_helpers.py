from mhc_draw import Circuit, Board

def add_standard_rails(b: Board, build: int = 1, vcc_holes=("TP2", "BP2"), gnd_holes=("TN1", "BN1")) -> None:
    """Connect top and bottom +5V and GND power rails."""
    b.wire(vcc_holes[0], vcc_holes[1], build, "+5V")
    b.wire(gnd_holes[0], gnd_holes[1], build, "GND")

def add_decoupling_cap(
    c: Circuit,
    b: Board,
    cap_name: str,
    vcc_pin_hole: str,
    gnd_pin_hole: str,
    rail_vcc: str,
    rail_gnd: str,
    cap_hole_a: str,
    cap_hole_b: str,
    value: str = "100nF",
    build: int = 1,
) -> None:
    """Add schematic decoupling and breadboard placement for a bypass capacitor."""
    c.chain(("NET", "+5V"), [f"C:{cap_name}:{value}", "GND"], build)
    b.wire(vcc_pin_hole, rail_vcc, build, "+5V")
    b.wire(gnd_pin_hole, rail_gnd, build, "GND")
    b.two(cap_name, cap_hole_a, cap_hole_b, build)

def add_isp_5pin(
    c: Circuit,
    b: Board,
    ic_ref: str = "U1",
    pins: tuple[int, int, int, int] = (18, 19, 17, 1),
    holes: dict[str, str] | None = None,
    build: int = 1,
) -> None:
    """Wire a standard 5-pin ISP header (MISO, SCK, MOSI, RESET, GND) to the target IC."""
    if holes is None:
        holes = {
            "RESET": "8j",
            "MISO": "18c",
            "SCK": "17c",
            "MOSI": "19c",
            "GND": "TN6",
        }
    miso_pin, sck_pin, mosi_pin, rst_pin = pins

    c.ic("J1", "ISP programmer", 5, "skinny", {1: "MISO", 2: "SCK", 3: "MOSI", 4: "RESET", 5: "GND"}, at=(20, 60),
         sides={1: "R", 2: "R", 3: "R", 4: "R", 5: "R"}, connector=True, named_only=True)
    c.chain(("U1", rst_pin), ["NET:RESET"], build)
    c.chain(("NET", "RESET"), ["R:R1:10k", "+5V"], build)
    c.chain(("J1", 4), ["NET:RESET"], build)
    for jp, up, nm in ((1, miso_pin, "MISO"), (2, sck_pin, "SCK"), (3, mosi_pin, "MOSI")):
        c.chain(("J1", jp), [f"NET:{nm}"], build)
        c.chain((ic_ref, up), [f"NET:{nm}"], build)
    c.chain(("J1", 5), ["GND"], build)

    b.two("R1", "8i", "BP8", build)
    b.lead("J1", 4, holes["RESET"], build, "RESET")
    b.lead("J1", 1, holes["MISO"], build, "MISO")
    b.lead("J1", 2, holes["SCK"], build, "SCK")
    b.lead("J1", 3, holes["MOSI"], build, "MOSI")
    b.lead("J1", 5, holes["GND"], build, "GND")

def add_external_power(
    b,
    mode="mb102",
    build=1,
    voltage="5 V",
    top_voltage=None,
    bottom_voltage=None,
    label=None,
    pos_hole=None,
    neg_hole=None,
):
    """Add either an MB102 module or a battery pack to the breadboard."""
    if mode == "mb102":
        b.mb102(build=build, col=1, voltage=voltage, top_voltage=top_voltage, bottom_voltage=bottom_voltage)
    elif mode == "battery":
        kw = dict(
            build=build,
            pos_hole="BP1" if pos_hole is None else pos_hole,
            neg_hole="BN1" if neg_hole is None else neg_hole,
        )
        if label is not None:
            kw["label"] = label
        if voltage is not None:
            kw["voltage"] = voltage
        b.battery_pack(**kw)
                                        
def _unit(b, src_hole, uc, r, d, build, label):
    """An LED unit: wire from a chip pin to (uc,a); resistor across the centre channel; LED to the bottom GND rail."""
    b.wire(src_hole, f"{uc}a", build, label)
    b.two(r, f"{uc}d", f"{uc}g", build)
    b.two(d, f"{uc}h", f"BN{uc}", build)

def _picks(c, conn_at=(20, 60)):
    c.ic("J1", "PICkit 3 ICSP", 5, "skinny", {1: "MCLR", 2: "VDD", 3: "VSS", 4: "PGD", 5: "PGC"}, at=conn_at,
         sides={1: "R", 2: "R", 3: "R", 4: "R", 5: "R"}, connector=True)

def _rail_bridges(b, build, left=True, right=True):
    if left:
        b.wire("TP2", "BP2", build, "+5V"); b.wire("TN1", "BN1", build, "GND")
    if right:
        for r in ("TP", "BP", "TN", "BN"):
            b.wire(f"{r}31", f"{r}32", build, "+5V" if r in ("TP", "BP") else "GND")

