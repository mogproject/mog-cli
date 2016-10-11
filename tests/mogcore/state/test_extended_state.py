import unittest
from mogcore import *
from tests.mogcore.state.gen_state import *


class TestExtendedState(unittest.TestCase):

    def test_get_legal_moves(self):
        self.maxDiff = None

        p1 = ExtendedState.from_string('PI\n+')
        self.assertEqual([BitBoard.wrap(bb) for bb in p1.get_legal_moves()], [
            BitBoard(),  # rook
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o175, 0o000),
            BitBoard(),  # bishop
            BitBoard(),
            BitBoard(),  # lance
            BitBoard(),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o001, 0o000),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o400, 0o000),
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
            BitBoard(),  # gold
            BitBoard(),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o034, 0o000),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o160, 0o000),
            BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o070, 0o000),  # king
            BitBoard(),
        ] + [BitBoard()] * 40)

        p2 = ExtendedState.from_string(
            'P1 *  *  *  *  *  *  *  *  * \n' +
            'P2 *  *  *  *  *  *  *  *  * \n' +
            'P3 *  *  *  *  *  *  *  *  * \n' +
            'P4 *  *  *  *  *  *  *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7 *  *  *  *  *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9 *  *  *  *  *  *  *  *  * \n' +
            '-')
        self.assertEqual([BitBoard.wrap(bb) for bb in p2.get_legal_moves()], [BitBoard()] * 80)

        p3 = ExtendedState.from_string('\n'.join([
            'P1 *  *  *  * -OU *  *  *  * ',
            'P2 *  *  *  *  *  *  *  *  * ',
            'P3 *  *  *  *  *  *  *  *  * ',
            'P4 *  *  *  *  *  *  *  *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  *  *  *  *  *  *  *  * ',
            'P7 *  *  *  *  *  *  *  *  * ',
            'P8 *  *  *  *  *  *  *  *  * ',
            'P9 *  *  *  *  *  *  *  *  * ',
            'P+00HI00HI00KA00KA00KI00KI00KI00KI00GI00GI00GI00GI00KE00KE00KE00KE00KY00KY00KY00KY'
            '00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU',
            'P-',
            '+'
        ]))
        self.assertEqual([BitBoard.wrap(bb) for bb in p3.get_legal_moves()], [
            BitBoard(0o757, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777),  # rook
            BitBoard(),
            BitBoard(0o757, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777),  # bishop
            BitBoard(),
            BitBoard(0o000, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777),  # lance
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(0o757, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777),  # silver
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(0o000, 0o000, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777),  # knight
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(0o000, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777),  # pawn
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(0o757, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777),  # gold
            BitBoard(),
            BitBoard(),
            BitBoard(),
            BitBoard(),  # king
            BitBoard(),
        ] + [BitBoard()] * 40)

    def test_legal_moves(self):
        self.maxDiff = None
        f = lambda s: Move.from_string(s)

        p1 = ExtendedState.from_string('PI\n+')
        self.assertEqual(p1.legal_moves(), [
            f('+2818HI'), f('+2838HI'), f('+2848HI'),
            f('+2858HI'), f('+2868HI'), f('+2878HI'),
            f('+1918KY'), f('+9998KY'),
            f('+3938GI'), f('+3948GI'),
            f('+7968GI'), f('+7978GI'),
            f('+1716FU'), f('+2726FU'), f('+3736FU'),
            f('+4746FU'), f('+5756FU'), f('+6766FU'),
            f('+7776FU'), f('+8786FU'), f('+9796FU'),
            f('+4938KI'), f('+4948KI'), f('+4958KI'),
            f('+6958KI'), f('+6968KI'), f('+6978KI'),
            f('+5948OU'), f('+5958OU'), f('+5968OU'),
        ])

        p2 = ExtendedState.from_string(
            'P1 *  *  *  *  *  *  *  *  * \n' +
            'P2 *  *  *  *  *  *  *  *  * \n' +
            'P3 *  *  *  *  *  *  *  *  * \n' +
            'P4 *  *  *  *  *  *  *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7 *  *  *  *  *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9 *  *  *  *  *  *  *  *  * \n' +
            '-')
        self.assertEqual(p2.legal_moves(), [])

        p3 = ExtendedState.from_string('\n'.join([
            'P1 *  *  *  * -OU *  *  *  * ',
            'P2 *  *  *  *  *  *  *  *  * ',
            'P3 *  *  *  *  *  *  *  *  * ',
            'P4 *  *  *  *  *  *  *  *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  *  *  *  *  *  *  *  * ',
            'P7 *  *  *  *  *  *  *  *  * ',
            'P8 *  *  *  *  *  *  *  *  * ',
            'P9 *  *  *  *  *  *  *  *  * ',
            'P+00HI00HI00KA00KA00KI00KI00KI00KI00GI00GI00GI00GI00KE00KE00KE00KE00KY00KY00KY00KY'
            '00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU',
            'P-',
            '+'
        ]))
        self.assertEqual(p3.legal_moves(),
                         [Move(BLACK, HAND, Pos(i), ROOK) for i in range(81) if i != 4] +
                         [Move(BLACK, HAND, Pos(i), BISHOP) for i in range(81) if i != 4] +
                         [Move(BLACK, HAND, Pos(i), LANCE) for i in range(9, 81)] +
                         [Move(BLACK, HAND, Pos(i), SILVER) for i in range(81) if i != 4] +
                         [Move(BLACK, HAND, Pos(i), KNIGHT) for i in range(18, 81)] +
                         [Move(BLACK, HAND, Pos(i), PAWN) for i in range(9, 81)] +
                         [Move(BLACK, HAND, Pos(i), GOLD) for i in range(81) if i != 4]
                         )

        p4 = ExtendedState.from_string('\n'.join([
            'P1 *  *  *  *  *  *  *  *  * ',
            'P2 *  *  *  *  *  *  *  *  * ',
            'P3 *  *  *  *  *  *  *  *  * ',
            'P4 *  *  * -KE * -OU *  *  * ',
            'P5 *  * -KE-FU *  *  *  *  * ',
            'P6 * -KE-FU *  *  *  * -KA * ',
            'P7-KE-FU *  *  * -GI * -KI * ',
            'P8-FU *  *  *  *  *  * -KA * ',
            'P9 *  * -TO *  *  *  *  *  * ',
            '-'
        ]))
        e4 = [f(x) for x in ''.join(
            '-2615KA -2635KA -2617KA -2637KA -2648KA -2659KA '
            '-2617UM -2637UM -2648UM -2659UM '
            '-2855KA -2846KA -2817KA -2837KA -2819KA -2839KA '
            '-2855UM -2846UM -2817UM -2837UM -2819UM -2839UM '
            '-4736GI -4756GI -4738GI -4748GI -4758GI '
            '-4736NG -4756NG -4738NG -4748NG -4758NG '
            '-6456KE '
            '-7567KE -7567NK '
            '-8678NK -9789NK '
            '-6566FU -7677FU -7677TO '
            '-8788FU -8788TO -9899TO -7978TO -7969TO -7989TO '
            '-2717KI -2737KI -2718KI -2738KI '
            '-4433OU -4443OU -4453OU -4434OU -4454OU -4435OU -4445OU -4455OU'
        ).split()]
        self.assertEqual(p4.legal_moves(), e4)

        self.assertEqual(len(ExtendedState(STATE_MAX_LEGAL_MOVES).legal_moves()), 593)
