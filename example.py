import time

from stspin import (
    SpinChain,
    SpinDevice,
    Constant as StConstant,
    Register as StRegister,
    utility,
)

def print_visual_status(device: SpinDevice) -> None:
    status = device.getStatus()
    print(utility.getPrettyStatus(status))

if '__main__' == __name__:
    # {{{ Setup devices
    stChain = SpinChain(
        total_devices=2,
        spi_select=(0, 0),
        chip_select_pin=None, # Not implemented, relies on spidev for CS pin
    )

    motorMain = stChain.create(1)
    motorAux = stChain.create(0)

    # Warning: These ICs start in holding mode by default,
    # which means MAXIMUM CURRENT is going through your stepper motors
    motorMain.hiZHard()
    motorAux.hiZHard()
    # }}}

    # If the motor doesn't seem to run, try changing the overcurrent threshold
    # Also check device.getStatus output for further info
    # Do NOT exceed your motor's current rating
    # Do NOT rely on the chip's Thermal Shutdown protection
    #motorMain.setRegister(StRegister.ThOcd, 0xF)
    #motorAux.setRegister(StRegister.ThOcd, 0xF)

    motorMain.setRegister(StRegister.SpeedMax, 0x22)

    #print(f'Status: 0x{motorMain.getStatus():02X}')
    print_visual_status(motorMain)

    # {{{ Simple run test
    motorMain.run(100)
    time.sleep(3)

    print_visual_status(motorMain)
    time.sleep(3)

    motorMain.hiZSoft()
    time.sleep(1)
    # }}}

    # {{{ Set some registers
    motorMain.setRegister(StRegister.Acc, 0x5)
    motorMain.setRegister(StRegister.Dec, 0x10)
    motorAux.setRegister(StRegister.Acc, 0x20)
    # }}}

    # {{{ Go n steps with both motors
    print('Accelerating')
    motorMain.move(steps=420000)
    motorAux.move(steps=420000)
    print('Still running...')
    while motorMain.isBusy():
        time.sleep(0.2)

    print('Motor done moving')
    # }}}

    # {{{ Go back to original position with main motor
    # Alternatively use GoMark and GoHome commands
    motorMain.setDirection(StConstant.DirReverse)
    motorMain.move(steps=420000)

    while motorMain.isBusy():
        # Watch motor acceleration
        print(f'Speed: {motorMain.getRegister(StRegister.Speed)} uStep/s')
        time.sleep(0.2)
    # }}}

    motorMain.hiZHard()
