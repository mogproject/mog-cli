import unittest
from mogcore import *
import cmogcore


class TestSimpleMove(unittest.TestCase):

    def test_init(self):
        m1 = SimpleMove(BLACK, P77, P76, PAWN)
        self.assertEqual(m1.turn, BLACK)
        self.assertEqual(m1.from_, P77)
        self.assertEqual(m1.to, P76)
        self.assertEqual(m1.piece_type, PAWN)

        m2 = SimpleMove(WHITE, HAND, P11, BISHOP)
        self.assertEqual(m2.turn, WHITE)
        self.assertEqual(m2.from_, HAND)
        self.assertEqual(m2.to, P11)
        self.assertEqual(m2.piece_type, BISHOP)

    def test_init_invalid(self):
        self.assertRaises(AssertionError, SimpleMove, 1, 2, 3, 4)
        self.assertRaises(AssertionError, SimpleMove, None, None, None, None)
        self.assertRaises(AssertionError, SimpleMove, BLACK, None, None, None)
        self.assertRaises(AssertionError, SimpleMove, BLACK, P77, None, None)
        self.assertRaises(AssertionError, SimpleMove, BLACK, P77, P76, None)
        self.assertRaises(AssertionError, SimpleMove, BLACK, P77, P77, PAWN)
        self.assertRaises(AssertionError, SimpleMove, BLACK, P77, HAND, PAWN)

    def test_eq(self):
        self.assertEqual(SimpleMove(BLACK, P77, P76, PAWN) == 1, False)
        self.assertEqual(SimpleMove(BLACK, P77, P76, PAWN) == SimpleMove(WHITE, P77, P76, PAWN), False)
        self.assertEqual(SimpleMove(BLACK, P77, P76, PAWN) == SimpleMove(BLACK, P77, P76, PAWN), True)

    def test_str(self):
        self.assertEqual(str(SimpleMove(BLACK, P77, P76, PAWN)), '+7776FU')

    def test_repr(self):
        exp = 'SimpleMove(turn=Turn(value=0), from_=Pos(value=60), to=Pos(value=51), piece_type=PieceType(value=5))'
        self.assertEqual(repr(SimpleMove(BLACK, P77, P76, PAWN)), exp)

    def test_wrap(self):
        self.assertEqual(SimpleMove.wrap(cmogcore.SimpleMove(0, 60, 51, 5)), SimpleMove(BLACK, P77, P76, PAWN))
        self.assertEqual(SimpleMove.wrap(SimpleMove(BLACK, P77, P76, PAWN)), SimpleMove(BLACK, P77, P76, PAWN))

    def test_from_string(self):
        self.assertEqual(SimpleMove.from_string('+7776FU'), SimpleMove(BLACK, P77, P76, PAWN))

    def test_from_string_invalid(self):
        self.assertRaises(ValueError, SimpleMove.from_string, '')
        self.assertRaises(ValueError, SimpleMove.from_string, '+')
        self.assertRaises(ValueError, SimpleMove.from_string, '+77')
        self.assertRaises(ValueError, SimpleMove.from_string, '+7776')
        self.assertRaises(ValueError, SimpleMove.from_string, '+7776FU ')
        self.assertRaises(ValueError, SimpleMove.from_string, 0)
        self.assertRaises(ValueError, SimpleMove.from_string, None)
