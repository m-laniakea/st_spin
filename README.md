# ST Spin Family Interface
A Python library for interfacing with [ST Spin Family devices](https://www.digikey.fi/en/product-highlight/s/stmicroelectronics/motor-control-easyspin "ST Spin Family devices"),
specifically the ST Micro **L6470**, **L6472**, **L6474**, and **L6480** ICs.

Currently this project has a single dependency: [spidev](https://pypi.org/project/spidev/ "spidev").

## Getting Started
Add `stspin` to your list of requirements and install.

**Create a device chain**
```
import time  # Used in our example

from stspin import (
	SpinChain,
	StCommand,
	StRegister,
	StConstant,
)

device_chain = SpinChain(
	total_devices=3,
	spi_select=(0, 0)
)
```
This assumes the spi device is at 0, 0.

**Create devices**
```
motor_main = device_chain.create_device(0)
motor_secondary = device_chain.create_device(1)
```
In our example, there are three devices in the chain, and **device 0** is furthest along the chain
from the controlling IC's MOSI pin.

**Run basic commands**
```
motor_main.hiZHard()  # It is good practice to set device into HiZ-State before setting parameters
motor_main.setRegister(StRegister.SpeedMax, 0x022)
motor_main.move(steps=2200)

while motor_main.isBusy():
	pass

motor_main.setDirection(StConstant.DirReverse)

motor_main.run(220)
time.sleep(3)
motor_main.stopSoft()
```
