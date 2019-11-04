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
)
from .utility import toByteArrayWithLength


class SpiStub:
    def xfer2(self, data: List[int]) -> None:
        pass


class StSpinDevice:
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

    def _write(self, data: int) -> None:
        """Write a single byte to the device.

        :data: A single byte representing a command or value
        """
        assert(data >= 0)
        assert(data <= 0xFF)

        buffer = [0] * self._total_devices
        buffer[self._position] = data

        # TODO: CS LOW
        self._spi.xfer2(buffer)
        # TODO: CS HIGH

    def _writeMultiple(self, data: List[int]) -> None:
        """Write each byte in list to device
        Used to combine calls to _write

        :data: List of single byte values to send
        """
        for data_byte in data:
            self._write(data_byte)

    def _writeCommand(
            self, command: int,
            payload: Optional[int] = None,
            payload_size: Optional[int] = None) -> None:
        """Write command to device with payload (if any)

        :command: Command to write
        :payload: Payload (if any)
        :payload_size: Payload size in bytes

        """
        self._write(command)

        if (payload_size is not None and payload is not None
                and payload_size > 0):
            self._writeMultiple(toByteArrayWithLength(payload, payload_size))

    def setRegister(self, register: int, value: int) -> None:
        """Set the specified register to the given value
        :register: The register location
        :value: Value register should be set to
        """
        RegisterSize = Register.getSize(register)
        set_command = Command.ParamSet | register

        self._writeCommand(set_command, value, RegisterSize)

    def run(self, steps_per_second: float, direction: int) -> None:
        """Run the motor at the given steps per second, in the
        given direction

        :steps_per_second: Steps per second up to 15625.
        0.015 step/s resolution
        :direction: Direction as declared in constant

        """
        assert(direction >= 0)
        assert(direction < Constant.DirMax)
        assert(steps_per_second >= 0)
        assert(steps_per_second <= Constant.MaxStepsPerSecond)

        speed = int(steps_per_second * Constant.SpsToSpeed)
        PayloadSize = Command.getPayloadSize(Command.Run)

        self._writeCommand(Command.Run | direction, speed, PayloadSize)

    def hiZHard(self) -> None:
        """Stop motors abruptly, release holding current

        """
        self._writeCommand(Command.HiZHard)

    def hiZSoft(self) -> None:
        """Stop motors, release holding current
        :returns: TODO

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
