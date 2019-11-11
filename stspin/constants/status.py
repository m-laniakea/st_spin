from typing_extensions import (
    Final,
)

class SwitchStatus:
    EventNone: Final        = 0
    EventFallingEdge: Final = Status.SwitchEvent  # Switch just closed

    Closed: Final           = 0
    Open: Final             = Status.SwitchFlag


class MotorStatus:
    Offset: Final           = 5
    Accelerating: Final     = 0b01 << Offset
    Decelerating: Final     = 0b10 << Offset
    ConstantSpeed: Final    = 0b11 << Offset
    Stopped: Final          = 0b00 << Offset


class Status:
    HiZ: Final              = 0x0001
    Busy: Final             = 0x0002
    SwitchFlag: Final       = 0x0004  # low on closed switch, high on open
    SwitchEvent: Final      = 0x0008  # high indicates falling edge detected
    Dir: Final              = 0x0010
    CmdNotPerformed: Final  = 0x0080
    CmdWrong: Final         = 0x0100
    Undervoltage: Final     = 0x0200  # active low
    ThermalWarning: Final   = 0x0400  # active low
    ThermalShutdown: Final  = 0x0800  # active low
    Overcurrent: Final      = 0x1000  # active low
    StepLossA: Final        = 0x2000  # low on stall detect
    StepLossB: Final        = 0x4000  # low on stall detect
    StepClockMode: Final    = 0x8000
