from typing import (
    Dict,
)
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
    ParamGet: Final         = 0x20  # ORed with target register value
    ParamSet: Final         = 0x00  # ORed with target register value
    ReleaseSw: Final        = 0x92  # ORed with ACT, DIR
    ResetDevice: Final      = 0xC0
    ResetPos: Final         = 0xD8  # Clears ABS_POS
    Run: Final              = 0x50  # ORed with DIR
    StatusGet: Final        = 0xD0
    StepClock: Final        = 0x58  # ORed with DIR
    StopHard: Final         = 0xB8
    StopSoft: Final         = 0xB0

    @staticmethod
    def getPayloadSize(command: int) -> int:
        """return size of payload in bytes expected to follow command

        :command: command to query
        :returns: payload size in bytes

        """
        assert command in PayloadSize

        return PayloadSize[command]


PayloadSize: Final[Dict[int, int]] = {
    Command.GoHome:         0,
    Command.GoMark:         0,
    Command.GoTo:           3,
    Command.GoToDir:        3,
    Command.GoUntil:        3,
    Command.HiZHard:        0,
    Command.HiZSoft:        0,
    Command.Nop:            0,
    Command.Move:           3,
    Command.ReleaseSw:      0,
    Command.ResetDevice:    0,
    Command.ResetPos:       0,
    Command.Run:            3,
    Command.StepClock:      0,
    Command.StopHard:       0,
    Command.StopSoft:       0,
}
