from typing_extensions import (
    Final,
)


class SpinValue:
    """Class representing values sent to and from Spin Devices
    :Value: Exclusively unsigned integers representing one or more bytes

    """
    Value: Final[int]
    Type: Final = 'SpinValue'

    def __init__(self, value: int) -> None:
        assert(value >= 0)
        self.Value = value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.Value == other

        if not isinstance(other, SpinValue):
            return NotImplemented

        return self.Value == other.Value

    def __or__(self, other: object) -> object:
        if isinstance(other, int):
            return SpinValue(self.Value | other)

        if not isinstance(other, SpinValue):
            return NotImplemented

        return SpinValue(self.Value | other.Value)

    def __repr__(self) -> str:
        return f'{self.Value}'


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
