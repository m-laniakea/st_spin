from typing import (
    List,
)


def getByteCount(value: int) -> int:
    """Calculate the number of bytes required to represent value

    :value: value to check. Non-negative
    :returns: number of bytes to represent the number

    """

    assert(value >= 0)

    if 0 == value:
        return 1

    return (value.bit_length() + 7) // 8


def resizeToLength(array: List[int], length: int) -> List[int]:
    """Resizes array, 0-extending the first positions,
    or truncating the first positions

    :array: Array to resize (if at all)
    :length: Desired length of array
    :returns: Resized array or original array

    """
    assert(length >= 0)
    difference = abs(len(array) - length)

    if len(array) > length:
        return array[difference:]

    return ([0] * difference) + array


def toByteArray(value: int) -> List[int]:
    """Splits an integer into a list of bytes

    :value: Value to convert. Must be non-negative
    :returns: List of bytes, with MSB at entry 0

    """
    byte_count = getByteCount(value)
    return list(value.to_bytes(byte_count, byteorder='big'))


def toByteArrayWithLength(value: int, length: int) -> List[int]:
    """Splits an integer into a list of bytes
    First bytes will be truncated or padded with 0 as
    required by length

    :value: Value to convert. Must be non-negative
    :length: Desired length in bytes
    :returns: List of bytes, with MSB at entry 0

    """
    return resizeToLength(toByteArray(value), length)


def toInt(byte_array: List[int]) -> int:
    """Convert a byte array to an integer

    :byte_array: Byte array with MSB first
    :returns: Single integer equivalent to given byte array

    """
    multiplier = 256 ** len(byte_array)
    result = 0

    for byte in byte_array:
        multiplier //= 256
        result += byte * multiplier

    return result
