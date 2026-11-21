from .month01_avr import month01_avr, M01_AVR_BUILDS
from .month01_pic import month01_pic, M01_PIC_BUILDS
from .month01_isp import month01_isp, M01_ISP_BUILDS
from .month02 import month02, M02_BUILDS
from .month03 import month03, M03_BUILDS
from .month04 import month04, M04_BUILDS
from .month05 import month05, M05_BUILDS

__all__ = [
    "month01_avr", "month01_pic", "month01_isp",
    "month02", "month03", "month04", "month05",
    "M01_PIC_BUILDS", "M01_AVR_BUILDS", "M01_ISP_BUILDS",
    "M02_BUILDS", "M03_BUILDS", "M04_BUILDS", "M05_BUILDS",
    "CIRCUITS",
]

CIRCUITS = [
    {
        "id": "m01avr",
        "month": 1,
        "folder": "month-01-electronic-dice",
        "prefix": "avr",
        "title": "Month 1 (ATmega328P)",
        "hw_title": "Month 1, ATmega328P track",
        "builds": M01_AVR_BUILDS,
        "fn": month01_avr,
    },
    {
        "id": "m01pic",
        "month": 1,
        "folder": "month-01-electronic-dice",
        "prefix": "pic",
        "title": "Month 1 (PIC)",
        "hw_title": "Month 1, PIC track",
        "builds": M01_PIC_BUILDS,
        "fn": month01_pic,
    },
    {
        "id": "m01isp",
        "month": 1,
        "folder": "month-01B-avr-programmer",
        "prefix": "programmer",
        "img_prefix": "build",
        "title": "Month 1 Part B",
        "hw_title": "Month 1 Part B, AVR programmer",
        "builds": M01_ISP_BUILDS,
        "fn": month01_isp,
    },
    {
        "id": "m02",
        "month": 2,
        "folder": "month-02-workshop-command-centre",
        "prefix": "month02",
        "img_prefix": "build",
        "title": "Month 2",
        "hw_title": "Month 2",
        "builds": M02_BUILDS,
        "fn": month02,
    },
    {
        "id": "m03",
        "month": 3,
        "folder": "month-03-analogue-in-out",
        "prefix": "month03",
        "img_prefix": "build",
        "title": "Month 3",
        "hw_title": "Month 3",
        "builds": M03_BUILDS,
        "fn": month03,
    },
    {
        "id": "m04",
        "month": 4,
        "folder": "month-04-binary-clock",
        "prefix": "month04",
        "img_prefix": "build",
        "title": "Month 4",
        "hw_title": "Month 4",
        "builds": M04_BUILDS,
        "fn": month04,
    },
    {
        "id": "m05",
        "month": 5,
        "folder": "month-05-sixteen-bit-and-memory",
        "prefix": "month05",
        "img_prefix": "build",
        "title": "Month 5",
        "hw_title": "Month 5",
        "builds": M05_BUILDS,
        "fn": month05,
    },
]