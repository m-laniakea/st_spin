from typing import (
        List,
        Optional,
        Tuple,
)
from typing_extensions import (
        Final,
)
import spidev

class SpiStub:
    def xfer2(self, data: List[int]) -> None:
        pass

class StSpinDevice:
    """Class providing access to a single SPIN device"""

    def __init__(
            self, position: int, busy_pin: int,
            total_devices: int, spi: SpiStub, chip_select_pin: Optional[int] = None):
        """
        :position: Position in chain, where 0 is the last device in chain
        :chip_select_pin: Chip select pin, if different from hardware SPI CS pin
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

    def _write_multiple(self, data: List[int]) -> None:
        """Write each byte in list to device
        Used to combine calls to _write

        :data: List of single byte values to send
        """
        for data_byte in data:
            self._write(data_byte)
