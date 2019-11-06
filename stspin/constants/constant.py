from typing_extensions import (
    Final,
)


class Constant:
    DirReverse: Final           = 0
    DirForward: Final           = 1
    DirMax: Final               = 2

    ActResetPos: Final          = (0 << 3)
    ActSetMark: Final           = (1 << 3)

    MaxStepsPerSecond: Final[float]     = 15625.0
    MaxSteps: Final                     = int(2 ** 22)

    TickSeconds: Final[float]           = 250 * (10 ** -9)
    SpsToSpeed: Final[float]            = TickSeconds / (2 ** -28)
