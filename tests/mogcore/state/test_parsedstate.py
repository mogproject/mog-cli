import unittest
from mogcore import *


class TestParsedState(unittest.TestCase):
    def test_get_legal_moves(self):
        self.maxDiff = None

        s = SimpleState.from_string('PI\n+')
        p = ParsedState(s)
        self.assertEqual([BitBoard.wrap(bb) for bb in p.get_legal_moves()], [
            BitBoard(),  # king
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o070, 0o000),
            BitBoard(),  # rook
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o175, 0o000),
            BitBoard(),  # bishop
            BitBoard(),
            BitBoard(),  # lance
            BitBoard(),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o001, 0o000),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o400, 0o000),
            BitBoard(),  # gold
            BitBoard(),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o034, 0o000),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o160, 0o000),
            BitBoard(),  # silver
            BitBoard(),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o014, 0o000),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o140, 0o000),
            BitBoard(),  # knight
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),  # pawn
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o001, 0o000, 0o000, 0o000),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o002, 0o000, 0o000, 0o000),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o004, 0o000, 0o000, 0o000),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o010, 0o000, 0o000, 0o000),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o020, 0o000, 0o000, 0o000),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o040, 0o000, 0o000, 0o000),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o100, 0o000, 0o000, 0o000),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o200, 0o000, 0o000, 0o000),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o400, 0o000, 0o000, 0o000),
        ] + [BitBoard()] * 40)
