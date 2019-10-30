from typing import (
    Dict,
)
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

    @staticmethod
    def getSize(register: int) -> int:
        """get the register size in bytes

        :register: Register to check
        :returns: Register size in bytes

        """
        assert(register in RegisterSize)

        return RegisterSize[register]


RegisterSize: Final[Dict[int, int]] = {
    Register.Acc:       2,
    Register.AdcOut:    1,
    Register.AlarmEn:   1,
    Register.Dec:       2,
    Register.Config:    2,
    Register.KTherm:    1,
    Register.KvalAcc:   1,
    Register.KvalDec:   1,
    Register.KvalHold:  1,
    Register.KvalRun:   1,
    Register.Mark:      3,
    Register.PosAbs:    3,
    Register.PosEl:     2,
    Register.SlpFnAcc:  1,
    Register.SlpFnDec:  1,
    Register.SlpSt:     1,
    Register.Speed:     3,
    Register.SpeedFS:   2,
    Register.SpeedInt:  2,
    Register.SpeedMax:  2,
    Register.SpeedMin:  2,
    Register.Status:    2,
    Register.StepMode:  1,
    Register.ThOcd:     1,
    Register.ThStl:     1,
}
