from typing_extensions import (
    Final,
)


class Constant:
    DirReverse: Final           = 0
    DirForward: Final           = 1
    DirMax: Final               = 2

    ActResetPos: Final          = (0 << 3)
    ActSetMark: Final           = (1 << 3)
