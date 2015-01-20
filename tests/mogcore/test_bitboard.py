import unittest
from mogcore.bitboard import BitBoard, full, empty


class TestBitBoard(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(empty), '\n'.join(['-' * 9] * 9))
        self.assertEqual(str(full), '\n'.join(['*' * 9] * 9))

    def test_get(self):
        self.assertFalse(any(empty.get(i) for i in range(81)))
        self.assertTrue(all(full.get(i) for i in range(81)))

    def test_get_invalid_range(self):
        self.assertFalse(empty.get(-1))
        self.assertFalse(empty.get(81))
        self.assertFalse(empty.get(10000))
        self.assertFalse(full.get(-1))
        self.assertFalse(full.get(81))
        self.assertFalse(full.get(10000))

    def test_set(self):
        self.assertEqual(empty.set(0), BitBoard(1, 0))
        self.assertEqual(empty.set(80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0o400))
        self.assertEqual(full.set(0), full)
        self.assertEqual(full.set(80), full)

    def test_set_invalid_range(self):
        self.assertEqual(empty.set(-1), empty)
        self.assertEqual(empty.set(81), empty)
        self.assertEqual(empty.set(10000), empty)
        self.assertEqual(full.set(-1), full)
        self.assertEqual(full.set(81), full)
        self.assertEqual(full.set(10000), full)

    def test_reset(self):
        self.assertEqual(empty.reset(0), empty)
        self.assertEqual(empty.reset(0), empty)
        self.assertEqual(full.reset(0), BitBoard(0o776, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.reset(80), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o377))

    def test_reset_invalid_range(self):
        self.assertEqual(empty.set(-1), empty)
        self.assertEqual(empty.set(81), empty)
        self.assertEqual(empty.set(10000), empty)
        self.assertEqual(full.set(-1), full)
        self.assertEqual(full.set(81), full)
        self.assertEqual(full.set(10000), full)

    def test_not(self):
        self.assertEqual(~empty, full)
        self.assertEqual(~full, empty)

    def test_and(self):
        self.assertEqual(empty & empty, empty)
        self.assertEqual(empty & full, empty)
        self.assertEqual(full & full, full)

    def test_or(self):
        self.assertEqual(empty | empty, empty)
        self.assertEqual(empty | full, full)
        self.assertEqual(full | full, full)

    def test_xor(self):
        self.assertEqual(empty ^ empty, empty)
        self.assertEqual(empty ^ full, full)
        self.assertEqual(full ^ full, empty)

    def test_shift_down(self):
        self.assertEqual(empty.shift_down(-2), empty)
        self.assertEqual(empty.shift_down(0), empty)
        self.assertEqual(empty.shift_down(2), empty)
        self.assertEqual(empty.shift_down(9), empty)
        self.assertEqual(empty.shift_down(64), empty)

        self.assertEqual(full.shift_down(9), empty)
        self.assertEqual(full.shift_down(8), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0o777))
        self.assertEqual(full.shift_down(7), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o777, 0o777))
        self.assertEqual(full.shift_down(6), BitBoard(0, 0, 0, 0, 0, 0, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_down(5), BitBoard(0, 0, 0, 0, 0, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_down(4), BitBoard(0, 0, 0, 0, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_down(3), BitBoard(0, 0, 0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_down(2), BitBoard(0, 0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_down(1), BitBoard(0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_down(0), full)
        self.assertEqual(full.shift_down(-1), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0))
        self.assertEqual(full.shift_down(-2), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0, 0))
        self.assertEqual(full.shift_down(-3), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0, 0, 0))
        self.assertEqual(full.shift_down(-4), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0, 0, 0, 0))
        self.assertEqual(full.shift_down(-5), BitBoard(0o777, 0o777, 0o777, 0o777, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_down(-6), BitBoard(0o777, 0o777, 0o777, 0, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_down(-7), BitBoard(0o777, 0o777, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_down(-8), BitBoard(0o777, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_down(-9), empty)
        self.assertEqual(full.shift_down(64), empty)
        self.assertEqual(full.shift_down(-2147483648), empty)
        self.assertEqual(full.shift_down(2147483647), empty)

    def test_shift_up(self):
        self.assertEqual(empty.shift_up(-2), empty)
        self.assertEqual(empty.shift_up(0), empty)
        self.assertEqual(empty.shift_up(2), empty)
        self.assertEqual(empty.shift_up(9), empty)
        self.assertEqual(empty.shift_up(64), empty)

        self.assertEqual(full.shift_up(-9), empty)
        self.assertEqual(full.shift_up(-8), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0o777))
        self.assertEqual(full.shift_up(-7), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o777, 0o777))
        self.assertEqual(full.shift_up(-6), BitBoard(0, 0, 0, 0, 0, 0, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_up(-5), BitBoard(0, 0, 0, 0, 0, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_up(-4), BitBoard(0, 0, 0, 0, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_up(-3), BitBoard(0, 0, 0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_up(-2), BitBoard(0, 0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_up(-1), BitBoard(0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_up(0), full)
        self.assertEqual(full.shift_up(1), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0))
        self.assertEqual(full.shift_up(2), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0, 0))
        self.assertEqual(full.shift_up(3), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0, 0, 0))
        self.assertEqual(full.shift_up(4), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0, 0, 0, 0))
        self.assertEqual(full.shift_up(5), BitBoard(0o777, 0o777, 0o777, 0o777, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_up(6), BitBoard(0o777, 0o777, 0o777, 0, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_up(7), BitBoard(0o777, 0o777, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_up(8), BitBoard(0o777, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_up(9), empty)
        self.assertEqual(full.shift_up(64), empty)
        self.assertEqual(full.shift_up(-2147483648), empty)
        self.assertEqual(full.shift_up(2147483647), empty)
