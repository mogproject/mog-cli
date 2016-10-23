import unittest
from mogcore import *
from tests.mogcore.state.gen_state import *


class TestGame(unittest.TestCase):

    def test_str(self):
        g1 = Game(State())
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
        g2.move(ExtendedMove(BLACK, P77, P76, PAWN, 10))
        g2.move(ExtendedMove(WHITE, P33, P34, PAWN, 1))
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
