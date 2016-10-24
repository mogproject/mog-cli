import unittest
from mogcore import *
from tests.mogcore.state.gen_state import *


class TestGame(unittest.TestCase):

    def test_str(self):
        g1 = Game(SimpleState())
        self.assertEqual(str(g1), '\n'.join([
            'P1 *  *  *  *  *  *  *  *  * ',
            'P2 *  *  *  *  *  *  *  *  * ',
            'P3 *  *  *  *  *  *  *  *  * ',
            'P4 *  *  *  *  *  *  *  *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  *  *  *  *  *  *  *  * ',
            'P7 *  *  *  *  *  *  *  *  * ',
            'P8 *  *  *  *  *  *  *  *  * ',
            'P9 *  *  *  *  *  *  *  *  * ',
            'P+',
            'P-',
            '+'
        ]))

        g2 = Game(STATE_HIRATE)
        self.assertEqual(str(g2), '\n'.join([
            'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY',
            'P2 * -HI *  *  *  *  * -KA * ',
            'P3-FU-FU-FU-FU-FU-FU-FU-FU-FU',
            'P4 *  *  *  *  *  *  *  *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  *  *  *  *  *  *  *  * ',
            'P7+FU+FU+FU+FU+FU+FU+FU+FU+FU',
            'P8 * +KA *  *  *  *  * +HI * ',
            'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY',
            'P+',
            'P-',
            '+'
        ]))
        g2.move(Move(BLACK, P77, P76, PAWN, 10))
        g2.move(Move(WHITE, P33, P34, PAWN, 1))
        self.assertEqual(str(g2), '\n'.join([
            'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY',
            'P2 * -HI *  *  *  *  * -KA * ',
            'P3-FU-FU-FU-FU-FU-FU-FU-FU-FU',
            'P4 *  *  *  *  *  *  *  *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  *  *  *  *  *  *  *  * ',
            'P7+FU+FU+FU+FU+FU+FU+FU+FU+FU',
            'P8 * +KA *  *  *  *  * +HI * ',
            'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY',
            'P+',
            'P-',
            '+',
            '+7776FU,T10',
            '-3334FU,T1',
        ]))
        g2.move(Resign(123))
        self.assertEqual(str(g2), '\n'.join([
            'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY',
            'P2 * -HI *  *  *  *  * -KA * ',
            'P3-FU-FU-FU-FU-FU-FU-FU-FU-FU',
            'P4 *  *  *  *  *  *  *  *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  *  *  *  *  *  *  *  * ',
            'P7+FU+FU+FU+FU+FU+FU+FU+FU+FU',
            'P8 * +KA *  *  *  *  * +HI * ',
            'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY',
            'P+',
            'P-',
            '+',
            '+7776FU,T10',
            '-3334FU,T1',
            '%TORYO,T123',
        ]))

    def test_move(self):
        g1 = Game(STATE_HIRATE)
        self.assertEqual(len(g1.moves), 0)

        moves = [
            '+5958OU', '-5152OU', '+5859OU', '-5251OU',
            '+5958OU', '-5152OU', '+5859OU', '-5251OU',
            '+5958OU', '-5152OU', '+5859OU', '-5251OU',
        ]
        for m in moves:
            g1.move(Move.from_string(m))
        self.assertEqual(len(g1.moves), 13)
        self.assertEqual(Move.wrap(g1.moves[-1]), ThreefoldRepetition())
