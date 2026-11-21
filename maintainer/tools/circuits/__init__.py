from .month01_pic import month1_pic, PIC1_BUILDS
from .month01_avr import month1_avr, AVR1_BUILDS
from .month01_isp import month1_isp, ISP1_BUILDS
from .month02 import month2, M2_BUILDS
from .month03 import month3, M3_BUILDS
from .month04 import month4, M4_BUILDS
from .month05 import month5, M5_BUILDS

__all__ = [
    "month1", "month1_avr", "month1_isp",
    "month2", "month3", "month4", "month5",
    "PIC1_BUILDS", "AVR1_BUILDS", "ISP1_BUILDS",
    "M2_BUILDS", "M3_BUILDS", "M4_BUILDS", "M5_BUILDS",
    "CIRCUITS",
]

CIRCUITS = [
    {
        "id": "m1pic",
        "month": 1,
        "folder": "month-01-electronic-dice",
        "prefix": "pic",
        "title": "Month 1 (PIC)",
        "hw_title": "Month 1, PIC track",
        "builds": PIC1_BUILDS,
        "fn": month1_pic,
    },
    {
        "id": "m1avr",
        "month": 1,
        "folder": "month-01-electronic-dice",
        "prefix": "avr",
        "title": "Month 1 (ATmega328P)",
        "hw_title": "Month 1, ATmega328P track",
        "builds": AVR1_BUILDS,
        "fn": month1_avr,
    },
    {
        "id": "m1isp",
        "month": 1,
        "folder": "month-01-electronic-dice/avr-programmer",
        "prefix": "programmer",
        "img_prefix": "build",
        "title": "Month 1 Part B",
        "hw_title": "Month 1 Part B, AVR programmer",
        "builds": ISP1_BUILDS,
        "fn": month1_isp,
    },
    {
        "id": "m2",
        "month": 2,
        "folder": "month-02-workshop-command-centre",
        "prefix": "month2",
        "img_prefix": "build",
        "title": "Month 2",
        "hw_title": "Month 2",
        "builds": M2_BUILDS,
        "fn": month2,
    },
    {
        "id": "m3",
        "month": 3,
        "folder": "month-03-analogue-in-out",
        "prefix": "month3",
        "img_prefix": "build",
        "title": "Month 3",
        "hw_title": "Month 3",
        "builds": M3_BUILDS,
        "fn": month3,
    },
    {
        "id": "m4",
        "month": 4,
        "folder": "month-04-binary-clock",
        "prefix": "month4",
        "img_prefix": "build",
        "title": "Month 4",
        "hw_title": "Month 4",
        "builds": M4_BUILDS,
        "fn": month4,
    },
    {
        "id": "m5",
        "month": 5,
        "folder": "month-05-sixteen-bit-and-memory",
        "prefix": "month5",
        "img_prefix": "build",
        "title": "Month 5",
        "hw_title": "Month 5",
        "builds": M5_BUILDS,
        "fn": month5,
    },
]