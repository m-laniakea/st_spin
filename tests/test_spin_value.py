import unittest

import stspin

from stspin.constants import (
    SpinValue
)


class TestUtility(unittest.TestCase):

    def testSpinValue(self) -> None:
        with self.assertRaises(AssertionError):
            SpinValue(-1)

        self.assertEqual(SpinValue(1), SpinValue(1))
        self.assertEqual(SpinValue(8), SpinValue(0) | SpinValue(8))
        self.assertEqual(SpinValue(0xFF), SpinValue(0xF0) | SpinValue(0x0F))

        self.assertEqual(SpinValue(22) == SpinValue(0o26), True)

        self.assertEqual(f'{SpinValue(22)}', '22')

        self.assertEqual(SpinValue(22), 22)
        self.assertEqual(SpinValue(16) | 6, 22)

        self.assertEqual(SpinValue(1) == '1', False)
        self.assertEqual('1' == SpinValue(1), False)

        self.assertEqual(SpinValue(1) == 1, True)
        self.assertEqual(1 == SpinValue(1), True)

        self.assertEqual(SpinValue(2) > SpinValue(1), True)
        self.assertEqual(SpinValue(2) > SpinValue(2), False)
        self.assertEqual(SpinValue(2) > SpinValue(3), False)
        self.assertEqual(SpinValue(2) > (1), True)
        self.assertEqual(SpinValue(2) > (2), False)
        self.assertEqual(SpinValue(2) > (3), False)

        with self.assertRaises(TypeError):
            SpinValue(2) > '1'

        self.assertEqual(SpinValue(2) >= SpinValue(1), True)
        self.assertEqual(SpinValue(2) >= SpinValue(2), True)
        self.assertEqual(SpinValue(2) >= SpinValue(3), False)
        self.assertEqual(SpinValue(2) >= (1), True)
        self.assertEqual(SpinValue(2) >= (2), True)
        self.assertEqual(SpinValue(2) >= (3), False)

        with self.assertRaises(TypeError):
            SpinValue(2) >= '1'

        self.assertEqual(SpinValue(2) < SpinValue(1), False)
        self.assertEqual(SpinValue(2) < SpinValue(2), False)
        self.assertEqual(SpinValue(2) < SpinValue(3), True)
        self.assertEqual(SpinValue(2) < (1), False)
        self.assertEqual(SpinValue(2) < (2), False)
        self.assertEqual(SpinValue(2) < (3), True)

        with self.assertRaises(TypeError):
            SpinValue(2) < '1'

        self.assertEqual(SpinValue(2) <= SpinValue(1), False)
        self.assertEqual(SpinValue(2) <= SpinValue(2), True)
        self.assertEqual(SpinValue(2) <= SpinValue(3), True)
        self.assertEqual(SpinValue(2) <= (1), False)
        self.assertEqual(SpinValue(2) <= (2), True)
        self.assertEqual(SpinValue(2) <= (3), True)

        with self.assertRaises(TypeError):
            SpinValue(2) <= '1'


if __name__ == '__main__':
    unittest.main()
