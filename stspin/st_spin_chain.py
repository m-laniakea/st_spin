from typing import (
        List,
        Optional,
        Tuple,
)
from typing_extensions import (
        Final,
)

from . import StSpinDevice

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
