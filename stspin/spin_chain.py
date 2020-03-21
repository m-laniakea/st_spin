from typing import (
    Callable,
    List,
    Optional,
    Tuple,
)
from typing_extensions import (
    Final,
)

from . import SpinDevice

class SpinChain:
    """Class for constructing a chain of SPIN devices"""
    def __init__(
            self, total_devices: int,
            spi_select: Optional[Tuple[int, int]] = None,
            spi_transfer: Optional[
                Callable[[List[int]], List[int]]
            ] = None,
        ) -> None:
        """
        if different from hardware SPI CS pin
        :total_devices: Total number of devices in chain
        :spi_select: A SPI bus, device pair, e.g. (0, 0)
        :spi_transfer: A SPI transfer function that behaves like
            spidev.xfer2.
            It should write a list of bytes as ints with MSB first,
            while correctly latching using the chip select pins
            Then return an equal-length list of bytes as ints from MISO

        """
        assert total_devices > 0
        assert (spi_select is None) != (spi_transfer is None), \
            'Either supply a SPI transfer function or use spidev\'s'

        self._total_devices: Final = total_devices

        # {{{ SPI setup
        if spi_transfer is not None:
            self._spi_transfer = spi_transfer

        elif spi_select is not None:
            import spidev
            self._spi: Final = spidev.SpiDev()

            bus, device = spi_select
            self._spi.open(bus, device)

            self._spi.mode = 3
            # Device expects MSB to be sent first
            self._spi.lsbfirst = False
            self._spi.max_speed_hz = 1000000
            # CS pin is active low
            self._spi.cshigh = False

            self._spi_transfer = self._spi.xfer2
        # }}}

    def create(self, position: int) -> SpinDevice:
        """
                   +----------+
              MOSI |   MCU    | MISO
       +-----------+          +---------------+
       |           +----------+               |
       |                                      |
       |                                      |
       |             SPIN ICs                 |
       |   +-----+     +-----+     +-----+    |
       |SDI|     |     |     |     |     |SDO |
       +---+  2  +-----+  1  +-----+  0  +----+
           |     |     |     |     |     |
           |     |     |     |     |     |
           +-----+     +-----+     +-----+
        Create a new SPIN device at the specified chain location
        :position: Device position in chain
        :return: A newly-instantiated SpinDevice

        """
        assert position >= 0
        assert position < self._total_devices

        return SpinDevice(
            position,
            self._total_devices,
            self._spi_transfer,
        )
