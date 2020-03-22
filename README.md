# ST Spin Family Interface
A Python library for interfacing with [ST Spin Family devices](https://www.digikey.fi/en/product-highlight/s/stmicroelectronics/motor-control-easyspin "ST Spin Family devices"),
specifically the ST Micro **L6470**, **L6472**, **L6474**, and **L6480** ICs.
Can be used nearly without modification with similar ICs.

If you do not specify your own spi_transfer function when creating a SpinChain, this project relies on [spidev's](https://pypi.org/project/spidev/ "spidev") SPI transfer function.

Python 3.6 or greater recommended.

## Getting Started
`pip install st-spin` or

`pip install st-spin[spidev]` if you intend to use /dev/spi and spidev's spi transfer function

**Add imports**
```python
import time  # Used in our example

from stspin import (
    SpinChain,
    SpinDevice,
    Constant as StConstant,
    Register as StRegister,
    utility,
)
```
**Create a device chain**
```python
stChain = SpinChain(
    total_devices=2,
    spi_select=(0, 0),
)
```
This assumes the spi device is at 0, 0.

**Create devices**
```python
motorMain = stChain.create(1)
motorAux = stChain.create(0)

# Unless you absolutely need holding current,
# it is good practice to disable the power bridges
motorMain.hiZHard()
motorAux.hiZHard()
```
**Run basic commands**
```
motorMain.setRegister(StRegister.SpeedMax, 0x22)

motorMain.run(100)
time.sleep(3)
motorMain.hiZSoft()
time.sleep(1)

# {{{ Set some registers
motorMain.setRegister(StRegister.Acc, 0x5)
motorMain.setRegister(StRegister.Dec, 0x10)
motorAux.setRegister(StRegister.Acc, 0x20)
# }}}

# {{{ Go n steps with both motors
motorMain.move(steps=420000)
motorAux.move(steps=420000)
while motorMain.isBusy():
    time.sleep(0.2)
# }}}

# {{{ Head back
motorMain.setDirection(StConstant.DirReverse)
motorMain.move(steps=420000)
while motorMain.isBusy():
    time.sleep(0.2)
# }}}

# Release holding current
motorAux.hiZHard()
motorMain.hiZHard()
```
### More details
For details on the SPI setup, see [create()](https://github.com/m-laniakea/st_spin/blob/dev/stspin/spin_chain.py#L47) in spin_chain.py.

See [example.py](https://github.com/m-laniakea/st_spin/blob/dev/example.py "example.py").

Check available [registers](https://github.com/m-laniakea/st_spin/blob/dev/stspin/constants/register.py) and [commands](https://github.com/m-laniakea/st_spin/blob/dev/stspin/constants/command.py).

**More commands**

All commands are defined, but some are not implemented, e.g. `GoToDir`. 
Currently you would use Command.getPayloadSize(GoToDir) and device._writeCommand() to run it.

**Creating your own spi_transfer function**

You may use your own spi transfer function in place of spidev's xfer2.
```
def custom_spi_transfer(buffer: List[int]) -> List[int]:
    # TODO: Implement me
    pass
    
stChain = SpinChain(
    total_devices=2,
    spi_transfer=custom_spi_transfer,
)
```
`custom_spi_transfer()` must take a list of bytes as int,
and return a same-length list of bytes as int from the MISO pin.

It should handle latching using the Chip Select pin, and transfer data with MSB first in
SPI Mode 3 (sample on rising edge, shift out on falling edge).

On these devices, Chip Select is active low.
### Troubleshooting
getStatus() is your friend. Feel free to use getPrettyStatus() under utility.py.
The manual is also your friend.

**Q: Why is my motor stalling, loud, or both?**
Most likely the Back-EMF compensation is not configured properly.
The correction parameters depend heavily on your motor's ke value (V/Hz), inductance, and phase resistance.

After calculating the parameters using the manufacturer's tool, set KvalAcc, SpeedInt, SlpSt, etc. using setRegister().
