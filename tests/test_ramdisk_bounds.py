"""Reference model for the Linux 0.11 RAM-disk sector bounds check.

This tests arithmetic only; it is not a kernel integration or QEMU test.
"""
import unittest

SECTOR_SIZE = 512


def request_fits(length_bytes, sector, count):
    capacity = length_bytes // SECTOR_SIZE
    return (
        count > 0
        and sector <= capacity
        and count <= capacity - sector
    )


class RamdiskBoundsTests(unittest.TestCase):
    def setUp(self):
        self.length = 512 * 1024  # RAMDISK=512 in 1 KiB blocks

    def test_last_1k_block_fits(self):
        self.assertTrue(request_fits(self.length, 1022, 2))

    def test_request_crossing_end_fails(self):
        self.assertFalse(request_fits(self.length, 1023, 2))

    def test_request_starting_at_end_fails(self):
        self.assertFalse(request_fits(self.length, 1024, 1))

    def test_zero_count_fails(self):
        self.assertFalse(request_fits(self.length, 10, 0))

    def test_far_out_of_range_fails(self):
        self.assertFalse(request_fits(self.length, 0xffffffff, 1))


if __name__ == "__main__":
    unittest.main()
