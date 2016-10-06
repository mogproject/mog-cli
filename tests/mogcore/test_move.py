import unittest
from mogcore import *


class TestMove(unittest.TestCase):
    def test_init(self):
        m1 = Move(BLACK, P77, P76, PAWN)
        self.assertEqual(m1.turn, BLACK)
        self.assertEqual(m1.from_, P77)
        self.assertEqual(m1.to, P76)
        self.assertEqual(m1.piece_type, PAWN)

        m2 = Move(WHITE, HAND, P11, BISHOP)
        self.assertEqual(m2.turn, WHITE)
        self.assertEqual(m2.from_, HAND)
        self.assertEqual(m2.to, P11)
        self.assertEqual(m2.piece_type, BISHOP)

    def test_init_invalid(self):
        self.assertRaises(AssertionError, Move, 1, 2, 3, 4)
        self.assertRaises(AssertionError, Move, None, None, None, None)
        self.assertRaises(AssertionError, Move, BLACK, None, None, None)
        self.assertRaises(AssertionError, Move, BLACK, P77, None, None)
        self.assertRaises(AssertionError, Move, BLACK, P77, P76, None)
        self.assertRaises(AssertionError, Move, BLACK, P77, P77, PAWN)
        self.assertRaises(AssertionError, Move, BLACK, P77, HAND, PAWN)

    def test_str(self):
        self.assertEqual(str(Move(BLACK, P77, P76, PAWN)), '+7776FU')

    def test_from_string(self):
        self.assertEqual(Move.from_string('+7776FU'), Move(BLACK, P77, P76, PAWN))

    def test_from_string_invalid(self):
        self.assertRaises(ValueError, Move.from_string, '')
        self.assertRaises(ValueError, Move.from_string, '+')
        self.assertRaises(ValueError, Move.from_string, '+77')
        self.assertRaises(ValueError, Move.from_string, '+7776')
        self.assertRaises(ValueError, Move.from_string, '+7776FU ')
        self.assertRaises(ValueError, Move.from_string, 0)
        self.assertRaises(ValueError, Move.from_string, None)
