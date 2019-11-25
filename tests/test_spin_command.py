import unittest

import stspin

from stspin.constants import (
    SpinCommand
)

from stspin.constants.command import (
    SpinCommand,
)


class TestUtility(unittest.TestCase):

    def testSpinCommand(self) -> None:
        with self.assertRaises(AssertionError):
            SpinCommand(-1, 1)

        with self.assertRaises(TypeError):
            SpinCommand(1)

        self.assertEqual(SpinCommand(1, 2), SpinCommand(1, 2))
        self.assertEqual(SpinCommand(8, 2), SpinCommand(0, 2) | SpinCommand(8, 2))
        self.assertEqual(SpinCommand(0xFF, 2), SpinCommand(0xF0, 2) | SpinCommand(0x0F, 2))

        self.assertEqual(SpinCommand(22, 2) == SpinCommand(22, 0o26), True)

        self.assertEqual(f'{SpinCommand(22, 2)}', '22')

        self.assertEqual(SpinCommand(22, 2), 22)
        self.assertEqual(SpinCommand(16, 2) | 6, 22)

        self.assertEqual(SpinCommand(1, 2) == '1', False)
        self.assertEqual('1' == SpinCommand(1, 2), False)

        self.assertEqual(SpinCommand(1, 2) == 1, True)
        self.assertEqual(1 == SpinCommand(1, 2), True)

        self.assertEqual(SpinCommand(2, 2), SpinCommand(2, 4))


if __name__ == '__main__':
    unittest.main()
