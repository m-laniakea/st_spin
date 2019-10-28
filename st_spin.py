from time import sleep

import spidev
import RPi.GPIO as GPIO
from typing import (
        List,
        Optional,
        Tuple,
)

from typing_extensions import (
        Final,
)

class SpiStub:
    def xfer2(self, data: List[int]) -> None:
        pass

# {{{ Commands
CMD_RUN: Final          = 0x50
CMD_HIZ_HARD: Final     = 0xA8
CMD_HIZ_SOFT: Final     = 0xA0
# }}}

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

class StSpinChain:
    """Class for constructing a chain of SPIN devices"""
    def __init__(
            self, busy_pin: int, total_devices: int, spi_select: Tuple[int, int],
            chip_select_pin: Optional[int] = None) -> None:
        """
        :chip_select_pin: Chip select pin, if different from hardware SPI CS pin
        :busy_pin: Pin to read busy status from
        :total_devices: Total number of devices in chain
        :spi_select: A SPI bus, device pair, e.g. (0, 0)
        """
        assert(total_devices > 0)

        self._chip_select_pin: Final   = chip_select_pin
        self._busy_pin: Final          = busy_pin
        self._total_devices: Final     = total_devices

        # {{{ SPI setup
        self._spi: Final = spidev.SpiDev()

        bus, device = spi_select
        self._spi.open(bus, device)

        self._spi.mode = 3
        # Device expects MSB to be sent first
        self._spi.lsbfirst = False
        self._spi.max_speed_hz = 1000000
        # CS pin is active low
        self._spi.cshigh = False
        # }}}

    def create(self, position: int) -> StSpinDevice:
        """Create a new SPIN device at the specified chain location"""
        assert(position >= 0)
        assert(position < self._total_devices)

        return StSpinDevice(
                position,
                self._busy_pin,
                self._total_devices,
                self._spi,
                self._chip_select_pin,
            )


GPIO.setmode(GPIO.BCM)
RESET_PIN = 22

# Setup and pulse reset pin
GPIO.setup(RESET_PIN, GPIO.OUT, initial=GPIO.LOW)
sleep(0.22)
GPIO.output(RESET_PIN, GPIO.HIGH)

chain = StSpinChain(
            busy_pin = 27,
            total_devices = 2,
            spi_select = (0, 0),
            chip_select_pin = None,
        )

Pump_A = chain.create(1)
Pump_B = chain.create(0)

import time

while True:
    Pump_A._write_multiple([CMD_RUN, 0, 200, 0])
    time.sleep(3)

    Pump_A._write_multiple([CMD_RUN, 10, 200, 0])
    Pump_B._write_multiple([CMD_RUN, 0, 200, 0])
    time.sleep(2)

    Pump_A._write(CMD_HIZ_HARD)
    time.sleep(1)

    Pump_B._write(CMD_HIZ_SOFT)
    time.sleep(1)
