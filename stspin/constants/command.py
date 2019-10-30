from typing_extensions import (
    Final,
)


class Command:
    GoHome: Final           = 0x70
    GoMark: Final           = 0x78
    GoTo: Final             = 0x60
    GoToDir: Final          = 0x68  # ORed with DIR
    GoUntil: Final          = 0x82  # ORed with ACT, DIR
    HiZHard: Final          = 0xA8
    HiZSoft: Final          = 0xA0
    Nop: Final              = 0x00
    Move: Final             = 0x40  # ORed with DIR. Unuseable while running
    ParamGet: Final         = 0x80  # ORed with target register value
    ParamSet: Final         = 0x00  # ORed with target register value
    ReleaseSw: Final        = 0x92  # ORed with ACT, DIR
    ResetDevice: Final      = 0xC0
    ResetPos: Final         = 0xD8  # Clears ABS_POS
    Run: Final              = 0x50  # ORed with DIR
    StatusGet: Final        = 0xD0
    StepClock: Final        = 0x58  # ORed with DIR
    StopHard:  Final        = 0xB8
    StopSoft: Final         = 0xB0
