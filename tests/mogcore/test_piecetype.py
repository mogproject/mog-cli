import unittest
from mogcore import *
from .gen_piecetype import gen_piecetype


class TestPieceType(unittest.TestCase):
    def test_init(self):
        self.assertEqual(PieceType(0), ROOK)
        self.assertEqual(PieceType(1), BISHOP)
        self.assertEqual(PieceType(2), LANCE)

    def test_init_invalid(self):
        self.assertRaises(AssertionError, PieceType, 14)
        self.assertRaises(AssertionError, PieceType, 15)
        self.assertRaises(AssertionError, PieceType, -1)
        self.assertRaises(AssertionError, PieceType, 'xxx')

    def test_value(self):
        self.assertEqual(KING.value, 7)
        self.assertEqual(ROOK.value, 0)
        self.assertEqual(PPAWN.value, 13)

    def test_str(self):
        self.assertEqual(str(PAWN), 'FU')
        self.assertEqual(str(LANCE), 'KY')

    def test_promoted(self):
        self.assertEqual(PAWN.promoted(), PPAWN)
        self.assertEqual(PPAWN.promoted(), PPAWN)
        self.assertEqual(KING.promoted(), KING)
        self.assertEqual(GOLD.promoted(), GOLD)

    def test_demoted(self):
        self.assertEqual(PAWN.demoted(), PAWN)
        self.assertEqual(PPAWN.demoted(), PAWN)
        self.assertEqual(KING.demoted(), KING)
        self.assertEqual(GOLD.demoted(), GOLD)

    def test_from_string(self):
        self.assertEqual(PieceType.from_string('FU'), PAWN)
        self.assertEqual(PieceType.from_string('KY'), LANCE)

    def test_from_string_invalid(self):
        self.assertRaises(ValueError, PieceType.from_string, '')
        self.assertRaises(ValueError, PieceType.from_string, ' ')
        self.assertRaises(ValueError, PieceType.from_string, 'xxx')
        self.assertRaises(ValueError, PieceType.from_string, 0)
        self.assertRaises(ValueError, PieceType.from_string, None)

    def test_prop_promote_then_demote(self):
        for pt in gen_piecetype(100):
            self.assertEqual(pt.promoted().demoted(), pt.demoted())
