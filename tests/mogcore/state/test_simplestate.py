import unittest
from mogcore import SimpleState


class TestSimpleState(unittest.TestCase):
    def test_constructor(self):
        s = SimpleState(0, [])
        self.assertEqual(s.turn, 0)
        self.assertEqual(s.pieces(), [-1] * 40)

        s = SimpleState(0, list(range(20)))
        self.assertEqual(s.turn, 0)
        self.assertEqual(s.pieces(), list(range(20)) + [-1] * 20)

        s = SimpleState(1, list(range(40)))
        self.assertEqual(s.turn, 1)
        self.assertEqual(s.pieces(), list(range(40)))

    def test_eq(self):
        s = SimpleState(0, [
            0, 257, 2, 259, 4, 261, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383,
            127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, -1, 127, 383,
        ])
        t = SimpleState(0, [
            257, 0, 259, 2, 261, 4, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127,
            383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, -1, 127, 383, 127, 383, 127,
        ])
        u = SimpleState(1, [
            257, 0, 259, 2, 261, 4, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127,
            383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, -1, 127, 383, 127, 383, 127,
        ])
        v = SimpleState(1, [
            257, 0, 259, 2, 261, 4, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 383,
            127, 127, 383, 127, 383, 127, 383, 127, 383, 127, 383, 127, -1, 127, 383, 127, 383, 127,
        ])
        self.assertEqual(s, t)
        self.assertEqual(s != t, False)
        self.assertNotEqual(t, u)
        self.assertNotEqual(u, v)
