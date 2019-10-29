from typing_extensions import (
        Final,
)

class Register:
    Mark: Final         = 0x03 # 22 bits
    PosAbs: Final       = 0x01 # 22 bits
    PosEl: Final        = 0x02 # 9 bits
    Speed: Final        = 0x04 # 20 bits
