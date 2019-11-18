import unittest

import stspin

from stspin.utility import (
    getByteCount,
    resizeToLength,
    toByteArray,
    toInt,
)

class TestUtility(unittest.TestCase):

    def testGetByteCount(self):
        self.assertEqual(getByteCount(0), 1)
        self.assertEqual(getByteCount(1), 1)

        self.assertEqual(getByteCount(2), 1)
        self.assertEqual(getByteCount(0xF), 1)

        self.assertEqual(getByteCount(0xFF), 1)
        self.assertEqual(getByteCount(0x100), 2)

        self.assertEqual(getByteCount(0xF0F0F0F0F0), 5)

        with self.assertRaises(AssertionError):
            getByteCount(-1)

if __name__ == '__main__':
    unittest.main()
