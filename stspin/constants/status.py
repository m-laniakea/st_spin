from typing_extensions import (
    Final,
)


class Status:
    HiZ: Final                  = 0x0001
    NotBusy: Final              = 0x0002  # active low
    SwitchFlag: Final           = 0x0004  # low on closed switch, high on open
    SwitchEvent: Final          = 0x0008  # high on falling edge
    Dir: Final                  = 0x0010
    CmdNotPerformed: Final      = 0x0080
    CmdWrong: Final             = 0x0100
    NotUndervoltage: Final      = 0x0200  # active low
    NotThermalWarning: Final    = 0x0400  # active low
    NotThermalShutdown: Final   = 0x0800  # active low
    NotOvercurrent: Final       = 0x1000  # active low
    NotStepLossA: Final         = 0x2000  # low on stall detect
    NotStepLossB: Final         = 0x4000  # low on stall detect
    StepClockMode: Final        = 0x8000


class MotorStatus:
    Offset: Final           = 5
    Accelerating: Final     = 0b01 << Offset
    Decelerating: Final     = 0b10 << Offset
    ConstantSpeed: Final    = 0b11 << Offset
    Stopped: Final          = 0b00 << Offset


class SwitchStatus:
    EventNone: Final        = 0
    EventFallingEdge: Final = Status.SwitchEvent  # Switch just closed

    Closed: Final           = 0
    Open: Final             = Status.SwitchFlag
