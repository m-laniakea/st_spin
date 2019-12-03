from typing import (
    Optional,
    Union,
)
from typing_extensions import (
    Final,
)


from .constant import SpinValue


class SpinCommand(SpinValue):
    PayloadSize: Final[Optional[int]]
    payload: Optional[SpinValue]

    def __init__(
            self,
            value: int,
            payload_size: Optional[int],
            total_bytes: Optional[int] = None) -> None:

        super().__init__(value, total_bytes)
        self.PayloadSize = payload_size

    def setPayload(self, payload: Union[int, SpinValue]) -> None:
        """Set a payload to add to this command

        :payload: A SpinValue to accompany the system command

        """
        if isinstance(payload, int):
            assert(self.PayloadSize is not None)
            payload = SpinValue(payload, self.PayloadSize)

        self.payload = payload


class Command:
    GoHome: Final           = SpinCommand(0x70, 0)
    GoMark: Final           = SpinCommand(0x78, 0)
    GoTo: Final             = SpinCommand(0x60, 3)
    GoToDir: Final          = SpinCommand(0x68, 3)  # ORed with DIR
    GoUntil: Final          = SpinCommand(0x82, 3)  # ORed with ACT, DIR
    HiZHard: Final          = SpinCommand(0xA8, 0)
    HiZSoft: Final          = SpinCommand(0xA0, 0)
    Nop: Final              = SpinCommand(0x00, 0)

    # ORed with DIR. Unuseable while running
    Move: Final             = SpinCommand(0x40, 3)

    # ORed with target register value
    ParamGet: Final         = SpinCommand(0x20, None)
    # ORed with target register value
    ParamSet: Final         = SpinCommand(0x00, None)
    ReleaseSw: Final        = SpinCommand(0x92, 0)  # ORed with ACT, DIR
    ResetDevice: Final      = SpinCommand(0xC0, 0)
    ResetPos: Final         = SpinCommand(0xD8, 0)  # Clears ABS_POS
    Run: Final              = SpinCommand(0x50, 3)  # ORed with DIR
    StatusGet: Final        = SpinCommand(0xD0, None)
    StepClock: Final        = SpinCommand(0x58, 0)  # ORed with DIR
    StopHard:  Final        = SpinCommand(0xB8, 0)
    StopSoft: Final         = SpinCommand(0xB0, 0)
