import unittest
from mogcore import *
from .gen_pos import gen_pos


class TestPos(unittest.TestCase):
    def test_init(self):
        self.assertEqual(Pos(81), HAND)
        self.assertEqual(Pos(0), P11)
        self.assertEqual(Pos(49), P56)
        self.assertEqual(Pos(80), P99)

    def test_init_invalid(self):
        self.assertRaises(AssertionError, Pos, 82)
        self.assertRaises(AssertionError, Pos, -1)
        self.assertRaises(AssertionError, Pos, 'xxx')
        self.assertRaises(AssertionError, Pos, None)

    def test_value(self):
        self.assertEqual(HAND.value, 81)
        self.assertEqual(P11.value, 0)
        self.assertEqual(P56.value, 49)
        self.assertEqual(P99.value, 80)

    def test_str(self):
        self.assertEqual(str(HAND), '00')
        self.assertEqual(str(P11), '11')
        self.assertEqual(str(P56), '56')
        self.assertEqual(str(P99), '99')

    def test_from_string(self):
        self.assertEqual(Pos.from_string('00'), HAND)
        self.assertEqual(Pos.from_string('11'), P11)
        self.assertEqual(Pos.from_string('56'), P56)
        self.assertEqual(Pos.from_string('99'), P99)

    def test_from_string_invalid(self):
        self.assertRaises(ValueError, Pos.from_string, '')
        self.assertRaises(ValueError, Pos.from_string, ' ')
        self.assertRaises(ValueError, Pos.from_string, 'xxx')
        self.assertRaises(ValueError, Pos.from_string, 0)
        self.assertRaises(ValueError, Pos.from_string, None)

    def test_prop_file_rank_order(self):
        def f(a, b):
            if (a, b) == (HAND, HAND):
                return False
            elif a == HAND:
                return False
            elif b == HAND:
                return True
            return p.rank < q.rank or (p.rank == q.rank and p.file < q.file)

        for p in gen_pos(50):
            for q in gen_pos(50):
                self.assertEqual(p.value < q.value, f(p, q), 'p=%r, q=%r' % (p, q))
