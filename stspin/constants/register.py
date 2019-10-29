from typing_extensions import (
        Final,
)

class Register:
    Acc: Final              = 0x05
    AdcOut: Final           = 0x12
    AlarmEn: Final          = 0x17
    Dec: Final              = 0x06
    Config: Final           = 0x18
    KTherm: Final           = 0x11
    KvalAcc: Final          = 0x0B
    KvalDec: Final          = 0x0C
    KvalHold: Final         = 0x09
    KvalRun: Final          = 0x0A
    Mark: Final             = 0x03
    PosAbs: Final           = 0x01
    PosEl: Final            = 0x02
    SlpFnAcc: Final         = 0x0F
    SlpFnDec: Final         = 0x10
    SlpSt: Final            = 0x0E
    Speed: Final            = 0x04
    SpeedFS: Final          = 0x15
    SpeedInt: Final         = 0x0D
    SpeedMax: Final         = 0x07
    SpeedMin: Final         = 0x08
    Status: Final           = 0x19
    StepMode: Final         = 0x16
    ThOcd: Final            = 0x13
    ThStl: Final            = 0x14
