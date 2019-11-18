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

    def testResizeToLength(self):
        self.assertEqual(
            resizeToLength([], 1),
            [0]
        )

        self.assertEqual(
            resizeToLength(['a'], 0),
            []
        )

        self.assertEqual(
            resizeToLength(['a', 'b', 'c'], 3),
            ['a', 'b', 'c']
        )

        self.assertEqual(
            resizeToLength([1, 2, 3], 1),
            [3]
        )

        self.assertEqual(
            resizeToLength([], 3),
            [0, 0, 0]
        )

        with self.assertRaises(AssertionError):
            resizeToLength([], -1)

    def testToByteArray(self):
        self.assertEqual(
            toByteArray(0),
            [0]
        )

        self.assertEqual(
            toByteArray(3),
            [3]
        )

        self.assertEqual(
            toByteArray(0x1FF),
            [1, 255]
        )

        self.assertEqual(
            toByteArray(0x100000000),
            [1, 0, 0, 0, 0]
        )


if __name__ == '__main__':
    unittest.main()
