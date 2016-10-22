import unittest
from mogcore import *
import cmogcore


class TestExtendedMove(unittest.TestCase):

    def test_init(self):
        m1 = ExtendedMove(BLACK, P77, P76, PAWN)
        self.assertEqual(m1.turn, BLACK)
        self.assertEqual(m1.from_, P77)
        self.assertEqual(m1.to, P76)
        self.assertEqual(m1.piece_type, PAWN)
        self.assertEqual(m1.elapsed_time, -1)

        m2 = ExtendedMove(WHITE, P33, P34, PAWN, 123)
        self.assertEqual(m2.turn, WHITE)
        self.assertEqual(m2.from_, P33)
        self.assertEqual(m2.to, P34)
        self.assertEqual(m2.piece_type, PAWN)
        self.assertEqual(m2.elapsed_time, 123)

    def test_str(self):
        self.assertEqual(str(ExtendedMove(BLACK, P77, P76, PAWN)), '+7776FU')
        self.assertEqual(str(ExtendedMove(BLACK, P77, P76, PAWN, 0)), '+7776FU,T0')
        self.assertEqual(str(ExtendedMove(BLACK, P77, P76, PAWN, 123)), '+7776FU,T123')


class TestResign(unittest.TestCase):

    def test_str(self):
        self.assertEqual(str(Resign()), '%TORYO')
        self.assertEqual(str(Resign(123)), '%TORYO,T123')
