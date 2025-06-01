import utils
import unittest

class TestUtils(unittest.TestCase):
    def test_as_bits(self):
        self.assertEqual(utils.as_bits(bytearray([1, 16])), [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0])

    def test_as_bytes(self):
        self.assertEqual(utils.as_bytes([1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]), bytearray([1, 16]))

    def test_bit_byte(self):
        self.assertEqual(utils.as_bytes(utils.as_bits(bytearray([1, 2, 200]))), bytearray([1, 2, 200]))

    def test_diff_encode(self):
        self.assertEqual(utils.diff_encode([1,1,0,0]), [0,1,0,0,0])

    def test_diff_decode(self):
        self.assertEqual(utils.diff_decode([0,1,0,0,0]), [1,1,0,0])

    def test_diff_diff(self):
        self.assertEqual(utils.diff_decode(utils.diff_encode([1,1,0,0,0,1,1,0,1,0])), [1,1,0,0,0,1,1,0,1,0])