from typing import (
    List,
    Optional,
    Tuple,
)
from typing_extensions import (
    Final,
)

from .constants import (
    Command,
    Constant,
    Register,
    Status,
)
from .utility import (
    toInt,
)


class SpiStub:
    def xfer2(self, data: List[int]) -> List[int]:
        pass


class SpinDevice:
    """Class providing access to a single SPIN device"""

    def __init__(
            self, position: int, busy_pin: int,
            total_devices: int, spi: SpiStub,
            chip_select_pin: Optional[int] = None):
        """
        :position: Position in chain, where 0 is the last device in chain
        :chip_select_pin: Chip select pin,
        if different from hardware SPI CS pin
        :busy_pin: Pin to read busy status from
        :total_devices: Total number of devices in chain
        :spi: SPI object used for serial communication
        """
        self._position: Final           = position
        self._chip_select_pin: Final    = chip_select_pin
        self._busy_pin: Final           = busy_pin
        self._total_devices: Final      = total_devices
        self._spi: Final                = spi

        self._direction                 = Constant.DirForward

    def _writeByte(self, byte_value: int) -> int:
        """Write a single byte to the device.

        :byte_value: A single byte to send to the device
        :return: Returns response byte
        """
        assert(byte_value >= 0)
        assert(byte_value <= 0xFF)

        buffer = [0] * self._total_devices
        buffer[self._position] = byte_value

        response = self._spi.xfer2(buffer)

        return response[self._position]

    def _write(self, value: SpinValue) -> List[int]:
        """Write each byte in data to device
        Used to combine calls to _writeByte

        :value: SpinValue containing Bytes to send
        :return: Response as a list of bytes
        """
        response = []

        for byte_value in value.Bytes:
            response.append(self._writeByte(byte_value))

        return response

    def _writeCommand(self, command: SpinCommand) -> SpinValue:
        """Write command to device with payload (if any)

        :command: Command to write
        :payload: Payload (if any)
        :return: Response as SpinValue
        """
        response = self._write(command)

        if command.payload is not None:
            response += self._write(command.payload)

        return SpinValue(response)

    def setRegister(self, register: int, value: int) -> SpinValue:
        """Set the specified register to the given value
        :register: The register location
        :value: Value register should be set to
        """
        _value = SpinValue(value, Register.getSize(register))
        set_command = (Command.ParamSet | register).setPayload(_value)

        return self._writeCommand(set_command)

    def getRegister(self, register: int) -> SpinValue:
        """Fetches a register's contents and returns the current value

        :register: Register location to be accessed
        :returns: Value of specified register

        """
        RegisterSize = Register.getSize(register)
        self._writeCommand(Command.ParamGet | register)

        response_bytes = self._write(SpinValue([Command.Nop] * RegisterSize))
        return SpinValue(response_bytes)

    def move(self, steps: int) -> None:
        """Move motor n steps

        :steps: Number of (micro)steps to take

        """
        assert(steps >= 0)
        assert(steps <= Constant.MaxSteps)

        command = (Command.Move | self._direction).setPayload(steps)
        self._writeCommand(command)

    def run(self, steps_per_second: float) -> None:
        """Run the motor at the given steps per second

        :steps_per_second: Full steps per second up to 15625.
        0.015 step/s resolution

        """
        assert(steps_per_second >= 0)
        assert(steps_per_second <= Constant.MaxStepsPerSecond)

        speed = int(steps_per_second * Constant.SpsToSpeed)
        command = (Command.Run | self._direction).setPayload(speed)

        self._writeCommand(command)

    def setDirection(self, direction: int) -> None:
        """Set motor direction. Does not affect active movement

        :direction: Direction as declared in Constant

        """
        assert(direction >= 0)
        assert(direction < Constant.DirMax)

        self._direction = direction

    def hiZHard(self) -> None:
        """Stop motors abruptly, release holding current

        """
        self._writeCommand(Command.HiZHard)

    def hiZSoft(self) -> None:
        """Stop motors, release holding current

        """
        self._writeCommand(Command.HiZSoft)

    def stopHard(self) -> None:
        """Stop motors abruptly, maintain holding current

        """
        self._writeCommand(Command.StopHard)

    def stopSoft(self) -> None:
        """Stop motors, maintain holding current

        """
        self._writeCommand(Command.StopSoft)

    def getStatus(self) -> SpinValue:
        """Get status register
        Resets alarm flags. Does not reset HiZ
        :returns: 2 bytes status as SpinValue

        """
        self._writeCommand(Command.Status)
        response_bytes = self._write(SpinValue([Command.Nop] * 2))

        return SpinValue(response_bytes)

    def isBusy(self) -> bool:
        """Checks busy status of the device
        :returns: True if device is busy, else False

        """
        # We use getRegister instead of getStatus
        # So as not to clear any warning flags
        status = self.getRegister(Register.Status)

        return False if (status & Status.NotBusy) else True
