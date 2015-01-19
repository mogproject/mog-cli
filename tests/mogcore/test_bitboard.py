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
