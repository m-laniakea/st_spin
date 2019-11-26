from typing import (
    Callable,
    Union,
)

from typing_extensions import (
    Final,
)


class SpinValue:
    """Class representing values sent to and from Spin Devices
    :Value: Exclusively unsigned integers representing one or more bytes

    """
    Value: Final[int]

    def __init__(self, value: int) -> None:
        assert(value >= 0)
        self.Value = value

    def _compare(self, other: object, comparator: Callable[[int, int], bool]) \
            -> Union[bool, 'NotImplemented']:

        if isinstance(other, int):
            return comparator(self.Value, other)

        if isinstance(other, SpinValue):
            return comparator(self.Value, other.Value)

        return NotImplemented

    def __eq__(self, other: object) -> bool:
        return self._compare(other, int.__eq__)

    def __or__(self, other: object) -> object:
        if isinstance(other, int):
            return SpinValue(self.Value | other)

        if not isinstance(other, SpinValue):
            return NotImplemented

        return SpinValue(self.Value | other.Value)

    def __repr__(self) -> str:
        return f'{self.Value}'


class Constant:
    DirReverse: Final           = SpinValue(0)
    DirForward: Final           = SpinValue(1)
    DirMax: Final               = SpinValue(2)

    ActResetPos: Final          = SpinValue(0 << 3)
    ActSetMark: Final           = SpinValue(1 << 3)

    MaxStepsPerSecond: Final[float]     = 15625.0
    MaxSteps: Final                     = int(2 ** 22)

    TickSeconds: Final[float]           = 250 * (10 ** -9)
    SpsToSpeed: Final[float]            = TickSeconds / (2 ** -28)
