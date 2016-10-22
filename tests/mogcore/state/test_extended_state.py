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

    def test_move(self):
        self.maxDiff = None
        f = lambda s: Move.from_string(s)

        p1 = ExtendedState.from_string('PI\n+')
        e1 = [f(x) for x in [
            '+2818HI', '+2838HI', '+2848HI',
            '+2858HI', '+2868HI', '+2878HI',
            '+1918KY', '+9998KY',
            '+3938GI', '+3948GI', '+7968GI', '+7978GI',
            '+1716FU', '+2726FU', '+3736FU', '+4746FU', '+5756FU', '+6766FU', '+7776FU', '+8786FU', '+9796FU',
            '+4938KI', '+4948KI', '+4958KI', '+6958KI', '+6968KI', '+6978KI',
            '+5948OU', '+5958OU', '+5968OU',
        ]]
        self.assertEqual(p1.legal_moves(), e1)

        p2 = p1.move(f('+7776FU'))
        e2 = [f(x) for x in [
            '-8232HI', '-8242HI', '-8252HI', '-8262HI', '-8272HI', '-8292HI',
            '-1112KY', '-9192KY',
            '-3132GI', '-3142GI', '-7162GI', '-7172GI',
            '-1314FU', '-2324FU', '-3334FU', '-4344FU', '-5354FU', '-6364FU', '-7374FU', '-8384FU', '-9394FU',
            '-4132KI', '-4142KI', '-4152KI', '-6152KI', '-6162KI', '-6172KI',
            '-5142OU', '-5152OU', '-5162OU']]
        self.assertEqual(p2.legal_moves(), e2)

        p3 = p2.move(f('-3334FU'))
        e3 = [f(x) for x in [
            '+2818HI', '+2838HI', '+2848HI', '+2858HI', '+2868HI', '+2878HI',
            '+8822KA', '+8833KA', '+8844KA', '+8855KA', '+8866KA', '+8877KA',
            '+8822UM', '+8833UM',
            '+1918KY', '+9998KY',
            '+3938GI', '+3948GI', '+7968GI', '+7978GI',
            '+8977KE',
            '+1716FU', '+2726FU', '+3736FU', '+4746FU', '+5756FU', '+6766FU', '+7675FU', '+8786FU', '+9796FU',
            '+4938KI', '+4948KI', '+4958KI', '+6958KI', '+6968KI', '+6978KI',
            '+5948OU', '+5958OU', '+5968OU'
        ]]
        self.assertEqual(p3.legal_moves(), e3)

        p4 = p3.move(f('+8822UM'))
        e4 = [f(x) for x in [
            '-8222HI', '-8232HI', '-8242HI', '-8252HI', '-8262HI', '-8272HI', '-8292HI',
            '-1112KY', '-9192KY',
            '-3122GI', '-3132GI', '-3142GI', '-7162GI', '-7172GI',
            '-2133KE',
            '-1314FU', '-2324FU', '-3435FU', '-4344FU', '-5354FU', '-6364FU', '-7374FU', '-8384FU', '-9394FU',
            '-4132KI', '-4142KI', '-4152KI', '-6152KI', '-6162KI', '-6172KI',
            '-5142OU', '-5152OU', '-5162OU'
        ]]
        self.assertEqual(p4.legal_moves(), e4)

        p5 = p4.move(f('-8222HI'))
        e5 = [f(x) for x in [
            '+2818HI', '+2838HI', '+2848HI', '+2858HI', '+2868HI', '+2878HI', '+2888HI', '+2898HI',
            '+0012KA', '+0032KA', '+0042KA', '+0052KA', '+0062KA', '+0072KA', '+0082KA', '+0092KA',
            '+0033KA', '+0014KA', '+0024KA', '+0044KA', '+0054KA', '+0064KA', '+0074KA', '+0084KA',
            '+0094KA', '+0015KA', '+0025KA', '+0035KA', '+0045KA', '+0055KA', '+0065KA', '+0075KA',
            '+0085KA', '+0095KA', '+0016KA', '+0026KA', '+0036KA', '+0046KA', '+0056KA', '+0066KA',
            '+0086KA', '+0096KA', '+0077KA', '+0018KA', '+0038KA', '+0048KA', '+0058KA', '+0068KA',
            '+0078KA', '+0088KA', '+0098KA',
            '+1918KY', '+9998KY',
            '+3938GI', '+3948GI', '+7968GI', '+7978GI', '+7988GI',
            '+8977KE',
            '+1716FU', '+2726FU', '+3736FU', '+4746FU', '+5756FU', '+6766FU', '+7675FU', '+8786FU', '+9796FU',
            '+4938KI', '+4948KI', '+4958KI', '+6958KI', '+6968KI', '+6978KI',
            '+5948OU', '+5958OU', '+5968OU'
        ]]
        self.assertEqual(p5.legal_moves(), e5)

        p6 = p5.move(f('+0033KA'))
        e6 = [f(x) for x in [
            '-2212HI', '-2232HI', '-2242HI', '-2252HI', '-2262HI', '-2272HI', '-2282HI', '-2292HI',
            '-0012KA', '-0032KA', '-0042KA', '-0052KA', '-0062KA', '-0072KA', '-0082KA', '-0092KA',
            '-0014KA', '-0024KA', '-0044KA', '-0054KA', '-0064KA', '-0074KA', '-0084KA', '-0094KA',
            '-0015KA', '-0025KA', '-0035KA', '-0045KA', '-0055KA', '-0065KA', '-0075KA', '-0085KA',
            '-0095KA', '-0016KA', '-0026KA', '-0036KA', '-0046KA', '-0056KA', '-0066KA', '-0086KA',
            '-0096KA', '-0077KA', '-0018KA', '-0038KA', '-0048KA', '-0058KA', '-0068KA', '-0078KA',
            '-0088KA', '-0098KA',
            '-1112KY', '-9192KY',
            '-3132GI', '-3142GI', '-7162GI', '-7172GI', '-7182GI',
            '-2133KE',
            '-1314FU', '-2324FU', '-3435FU', '-4344FU', '-5354FU', '-6364FU', '-7374FU', '-8384FU', '-9394FU',
            '-4132KI', '-4142KI', '-4152KI', '-6152KI', '-6162KI', '-6172KI',
            '-5142OU', '-5152OU', '-5162OU'
        ]]
        self.assertEqual(p6.legal_moves(), e6)

        p7 = p6.move(f('-0095KA'))
        e7 = [f(x) for x in [
            '+2818HI', '+2838HI', '+2848HI', '+2858HI', '+2868HI', '+2878HI', '+2888HI', '+2898HI',
            '+3351KA', '+3322KA', '+3342KA', '+3324KA', '+3344KA', '+3315KA', '+3355KA', '+3366KA',
            '+3377KA', '+3388KA', '+3351UM', '+3322UM', '+3342UM', '+3324UM', '+3344UM', '+3315UM',
            '+3355UM', '+3366UM', '+3377UM', '+3388UM',
            '+1918KY', '+9998KY',
            '+3938GI', '+3948GI', '+7968GI', '+7978GI', '+7988GI',
            '+8977KE',
            '+1716FU', '+2726FU', '+3736FU', '+4746FU', '+5756FU', '+6766FU', '+7675FU', '+8786FU', '+9796FU',
            '+4938KI', '+4948KI', '+4958KI', '+6958KI', '+6968KI', '+6978KI',
            '+5948OU', '+5958OU', '+5968OU'
        ]]
        self.assertEqual(p7.legal_moves(), e7)

        p8 = p7.move(f('+3351UM'))
        e8 = [f(x) for x in [
            '-2212HI', '-2232HI', '-2242HI', '-2252HI', '-2262HI', '-2272HI', '-2282HI', '-2292HI',
            '-9584KA', '-9586KA', '-9577KA', '-9568KA', '-9559KA', '-9577UM', '-9568UM', '-9559UM',
            '-1112KY', '-9192KY',
            '-3132GI', '-3142GI', '-7162GI', '-7172GI', '-7182GI',
            '-2133KE',
            '-1314FU', '-2324FU', '-3435FU', '-4344FU', '-5354FU', '-6364FU', '-7374FU', '-8384FU', '-9394FU',
            '-4151KI', '-4132KI', '-4142KI', '-4152KI', '-6151KI', '-6152KI', '-6162KI', '-6172KI'
        ]]
        self.assertEqual(p8.legal_moves(), e8)

    def test_hash_value(self):
        self.maxDiff = None
        f = lambda s: Move.from_string(s)

        self.assertEqual(ExtendedState(State()).hash_value, 0)

        self.assertNotEqual(ExtendedState(State().set_turn(WHITE.value)).hash_value, 0)

        self.assertEqual(ExtendedState(State().set_turn(WHITE.value).set_turn(BLACK.value)).hash_value, 0)

        self.assertNotEqual(ExtendedState(STATE_TSUME_BLACK).hash_value, ExtendedState(STATE_TSUME_WHITE).hash_value)

        s1 = [
            ExtendedState.from_string(
                'P1 *  *  *  *  *  *  *  *  * \n' +
                'P2 *  *  *  *  *  *  *  *  * \n' +
                'P3 *  *  *  *  *  *  *  *  * \n' +
                'P4 *  *  *  *  *  *  *  *  * \n' +
                'P5 *  *  *  *  *  *  *  *  * \n' +
                'P6 *  *  *  *  *  *  *  *  * \n' +
                'P7 *  *  *  *  *  *  *  *  * \n' +
                'P8 *  *  *  *  *  *  *  *  * \n' +
                'P9 *  *  *  *  *  *  *  *  * \n' +
                '-').hash_value,
            ExtendedState.from_string(
                'P1 *  *  *  *  *  *  *  * +HI\n' +
                'P2 *  *  *  *  *  *  *  *  * \n' +
                'P3 *  *  *  *  *  *  *  *  * \n' +
                'P4 *  *  *  *  *  *  *  *  * \n' +
                'P5 *  *  *  *  *  *  *  *  * \n' +
                'P6 *  *  *  *  *  *  *  *  * \n' +
                'P7 *  *  *  *  *  *  *  *  * \n' +
                'P8 *  *  *  *  *  *  *  *  * \n' +
                'P9 *  *  *  *  *  *  *  *  * \n' +
                '+').hash_value,
            ExtendedState.from_string(
                'P1 *  *  *  *  *  *  *  *  * \n' +
                'P2 *  *  *  *  *  *  *  *  * \n' +
                'P3 *  *  *  *  *  *  *  *  * \n' +
                'P4 *  *  *  *  *  *  *  *  * \n' +
                'P5 *  *  *  *  *  *  *  *  * \n' +
                'P6 *  *  *  *  *  *  *  *  * \n' +
                'P7 *  *  *  *  *  *  *  *  * \n' +
                'P8 *  *  *  *  *  *  *  *  * \n' +
                'P9 *  *  *  *  *  *  *  *  * \n' +
                'P+00HI\n'
                '+').hash_value,
        ]
        self.assertEqual(len(set(s1)), 3)

        p1 = ExtendedState.from_string(
            'P1 *  *  *  *  *  *  *  *  * \n' +
            'P2 *  *  *  *  *  *  *  *  * \n' +
            'P3 *  *  *  * -KI *  *  *  * \n' +
            'P4 *  *  *  * -KI *  *  *  * \n' +
            'P5 *  *  *  * +KI *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7 *  *  *  *  *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9 *  *  *  *  *  *  *  *  * \n' +
            '+')
        p2 = p1.move(f('+5554KI')).move(f('-5354KI')).move(f('+0055KI')).move(f('-0053KI'))

        self.assertEqual(p1, p2)
        self.assertEqual(p1.hash_value, p2.hash_value)

        p3 = ExtendedState.from_string(
            'P1 *  *  *  *  *  *  *  *  * \n' +
            'P2 *  *  *  *  *  *  *  *  * \n' +
            'P3 *  *  *  *  *  *  *  *  * \n' +
            'P4 *  *  *  *  *  *  *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7 *  *  *  *  *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9 *  *  *  *  *  *  *  *  * \n' +
            'P+00FU\n'
            '+')

        p4 = ExtendedState.from_string(
            'P1 *  *  *  *  *  *  *  *  * \n' +
            'P2 *  *  *  *  *  *  *  *  * \n' +
            'P3 *  *  *  *  *  *  *  *  * \n' +
            'P4 *  *  *  *  *  *  *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7 *  *  *  *  *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9 *  *  *  *  *  *  *  *  * \n' +
            'P-00FU\n'
            '+')
        self.assertNotEqual(p3.hash_value, p4.hash_value)

        p5 = (ExtendedState.from_string(
            'P1+TO+TO+TO+TO+TO+TO+TO+TO+TO\n' +
            'P2+TO+TO+TO+TO+TO+TO+TO+TO+TO\n' +
            'P3 *  *  *  *  *  *  *  *  * \n' +
            'P4 *  *  *  *  *  *  *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7 *  *  *  *  *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9-HI *  *  *  *  *  *  * +OU\n' +
            '-')
            .move(f('-9992HI')).move(f('+1918OU')).move(f('-9291HI')).move(f('+1819OU'))
            .move(f('-9182HI')).move(f('+1918OU')).move(f('-8281HI')).move(f('+1819OU'))
            .move(f('-8172HI')).move(f('+1918OU')).move(f('-7271HI')).move(f('+1819OU'))
            .move(f('-7162HI')).move(f('+1918OU')).move(f('-6261HI')).move(f('+1819OU'))
            .move(f('-6152HI')).move(f('+1918OU')).move(f('-5251HI')).move(f('+1819OU'))
            .move(f('-5142HI')).move(f('+1918OU')).move(f('-4241HI')).move(f('+1819OU'))
            .move(f('-4132HI')).move(f('+1918OU')).move(f('-3231HI')).move(f('+1819OU'))
            .move(f('-3122HI')).move(f('+1918OU')).move(f('-2221HI')).move(f('+1819OU'))
            .move(f('-2112HI')).move(f('+1918OU')).move(f('-1211HI')).move(f('+1819OU'))
        )

        p6 = ExtendedState.from_string(
            'P1 *  *  *  *  *  *  *  * -HI\n' +
            'P2 *  *  *  *  *  *  *  *  * \n' +
            'P3 *  *  *  *  *  *  *  *  * \n' +
            'P4 *  *  *  *  *  *  *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7 *  *  *  *  *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9 *  *  *  *  *  *  *  * +OU\n' +
            'P-00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU\n'
            '-')
        self.assertEqual(p5.hash_value, p6.hash_value)

        s = []
        for st in gen_state(100):
            s.append(ExtendedState(st).hash_value)

        self.assertEqual(len(s), 100)
        self.assertEqual(len(set(s)), 100)

    def test_is_checked(self):
        self.assertFalse(ExtendedState(STATE_HIRATE).is_checked())
        s1 = ExtendedState.from_string(
            'P1 *  *  *  *  *  *  *  * -OU\n' +
            'P2+RY *  *  *  *  *  *  *  * \n' +
            'P3 *  *  *  *  *  *  *  *  * \n' +
            'P4 *  *  *  *  *  *  *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  * +UM *  *  *  *  *  * \n' +
            'P7 *  *  *  *  *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9+UM *  *  *  *  *  * +RY * \n' +
            '+')
        self.assertFalse(s1.is_checked())

        s2 = ExtendedState.from_string(
            'P1 *  *  *  *  *  *  *  * -OU\n' +
            'P2 *  *  *  *  *  *  *  *  * \n' +
            'P3 *  *  *  *  *  *  *  *  * \n' +
            'P4 *  *  *  *  *  *  *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7 *  *  *  *  *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9+KA *  *  *  *  *  *  *  * \n' +
            '-')
        self.assertTrue(s2.is_checked())

        s3 = ExtendedState.from_string(
            'P1 *  *  *  *  *  *  *  * -OU\n' +
            'P2 *  *  *  * +HI *  *  *  * \n' +
            'P3 *  *  *  *  *  *  *  *  * \n' +
            'P4 *  *  *  * -KY+FU *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7 *  *  * -KE *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9+KA *  *  * +OU *  *  *  * \n' +
            '+')
        self.assertTrue(s3.is_checked())

    def test_is_king_alive(self):
        self.assertFalse(ExtendedState(State()).is_king_alive(BLACK.value))
        self.assertFalse(ExtendedState(State()).is_king_alive(WHITE.value))
        self.assertTrue(ExtendedState(STATE_HIRATE).is_king_alive(BLACK.value))
        self.assertTrue(ExtendedState(STATE_HIRATE).is_king_alive(WHITE.value))
        self.assertFalse(ExtendedState(STATE_TSUME_BLACK).is_king_alive(BLACK.value))
        self.assertTrue(ExtendedState(STATE_TSUME_BLACK).is_king_alive(WHITE.value))
        self.assertTrue(ExtendedState(STATE_TSUME_WHITE).is_king_alive(BLACK.value))
        self.assertFalse(ExtendedState(STATE_TSUME_WHITE).is_king_alive(WHITE.value))
