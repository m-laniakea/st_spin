from typing_extensions import (
        Final,
)

# {{{ Misc
DIR_FWD = 1
DIR_REV = 0

ACT_RESET_POS = 0
ACT_SET_MARK = 1
# }}}

# {{{ Commands
CMD_GO_HOME: Final      = 0x70
CMD_GO_MARK: Final      = 0x78
CMD_GO_TO: Final        = 0x60
CMD_GO_TO_DIR: Final    = 0x68 # ORed with DIR
CMD_GO_UNTIL: Final     = 0x82 # ORed with ACT, DIR
CMD_HIZ_HARD: Final     = 0xA8
CMD_HIZ_SOFT: Final     = 0xA0
CMD_NOP: Final          = 0x00
CMD_MOVE: Final         = 0x40 # ORed with DIR. Unuseable while running
CMD_PARAM_GET: Final    = 0x80 # ORed with target register value
CMD_PARAM_SET: Final    = 0x00 # ORed with target register value
CMD_RELEASE_SW: Final   = 0x92 # ORed with ACT, DIR
CMD_RESET_DEVICE: Final = 0xC0
CMD_RESET_POS: Final    = 0xD8 # Clears ABS_POS
CMD_RUN: Final          = 0x50 # ORed with DIR
CMD_STATUS_GET: Final   = 0xD0
CMD_STEP_CLOCK: Final   = 0x58 # ORed with DIR
CMD_STOP_HARD:  Final   = 0xB8
CMD_STOP_SOFT: Final    = 0xB0
# }}}

# {{{ Registers
# }}}
