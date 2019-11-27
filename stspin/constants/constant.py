from typing import (
    Callable,
    List,
    Optional,
    Union,
)

from typing_extensions import (
    Final,
)

from ..utility import (
    toInt,
    getByteCount,
    toByteArrayWithLength,
)


class SpinValue:
    """Class representing values sent to and from Spin Devices
    :Value: Exclusively unsigned integers representing one or more bytes

    """
    Value: Final[int]
    Bytes: Final[List[int]]

    def __init__(
            self,
            value: Union[int, List[int]],
            total_bytes: Optional[int] = None) -> None:

        if isinstance(value, list):
            bytes = value
            value = toInt(value)

        else:
            if total_bytes is None:
                # No desired number of bytes, just use exact number of bytes
                total_bytes = getByteCount(value)

            assert(total_bytes >= 1)

            bytes = toByteArrayWithLength(value, total_bytes)

        assert(value >= 0)

        self.Value = value
        self.Bytes = bytes

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

    def __lt__(self, other: object) -> bool:
        return self._compare(other, int.__lt__)

    def __gt__(self, other: object) -> bool:
        return self._compare(other, int.__gt__)

    def __le__(self, other: object) -> bool:
        return self._compare(other, int.__le__)

    def __ge__(self, other: object) -> bool:
        return self._compare(other, int.__ge__)

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
