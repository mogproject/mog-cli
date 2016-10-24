import unittest
from mogcore import *
from tests.mogcore.state.gen_state import *


class TestSimpleState(unittest.TestCase):

    def test_constructor(self):
        s = SimpleState()
        self.assertEqual(s.turn, BLACK)
        self.assertEqual(s.owner_bits, 0)
        self.assertEqual(s.hand_bits, 0)
        self.assertEqual(s.promoted_bits, 0)
        self.assertEqual(s.unused_bits, 0x000000ffffffffff)
        self.assertEqual(s.board, BitBoard())
        self.assertEqual(s.position, [0xffffffffffffffff] * 5)

        s = SimpleState(WHITE)
        self.assertEqual(s.turn, WHITE)

    def test_constructor_error(self):
        self.assertRaisesRegex(ValueError, '^position must have 5 elements', SimpleState,
                               BLACK, 0, 0, 0, 0x000000ffffffffff, BitBoard(), [])
        self.assertRaisesRegex(ValueError, '^invalid state: conflict between owner bits and unused bits',
                               SimpleState, BLACK, 1, 0, 0, 0x000000ffffffffff, BitBoard())
        self.assertRaisesRegex(ValueError, '^invalid state: conflict between hand bits and unused bits',
                               SimpleState, BLACK, 0, 1, 0, 0x000000ffffffffff, BitBoard())
        self.assertRaisesRegex(ValueError, '^invalid state: conflict between promoted bits and unused bits',
                               SimpleState, BLACK, 0, 0, 1, 0x000000ffffffffff, BitBoard())
        self.assertRaisesRegex(ValueError, '^invalid state: conflict between hand bits and promoted bits',
                               SimpleState, BLACK, 0, 1, 1, 0x000000fffffffffe, BitBoard(1, 0), [
                                   0xffffffffffffff00, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff
                               ])
        self.assertRaisesRegex(ValueError, '^invalid state: position must be in hand or unused',
                               SimpleState, BLACK, 0, 0, 0, 0x000000fffffffffe, BitBoard(1, 0), [
                                   0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff
                               ])
        self.assertRaisesRegex(ValueError, '^invalid state: position must not be in hand or unused',
                               SimpleState, BLACK, 0, 1, 0, 0x000000fffffffffe, BitBoard(1, 0), [
                                   0xffffffffffffff00, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff
                               ])
        self.assertRaisesRegex(ValueError, '^invalid state: position must not be in hand or unused',
                               SimpleState, BLACK, 0, 0, 0, 0x000000ffffffffff, BitBoard(1, 0), [
                                   0xffffffffffffff00, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff
                               ])
        self.assertRaisesRegex(ValueError, '^invalid state: invalid position value',
                               SimpleState, BLACK, 0, 0, 0, 0x000000fffffffffe, BitBoard(1, 0), [
                                   0xffffffffffffff51, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff
                               ])
        self.assertRaisesRegex(ValueError, '^invalid state: invalid position value',
                               SimpleState, BLACK, 0, 0, 0, 0x000000fffffffffe, BitBoard(1, 0), [
                                   0xfffffffffffffffe, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff
                               ])
        self.assertRaisesRegex(ValueError, '^invalid state: position already taken',
                               SimpleState, BLACK, 0, 0, 0, 0x000000fffffffffc, BitBoard(1, 0), [
                                   0xffffffffffff0000, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff
                               ])
        self.assertRaisesRegex(ValueError, '^invalid state: inconsistent board bitboard',
                               SimpleState, BLACK, 0, 0, 0, 0x000000fffffffffe, BitBoard(1, 0), [
                                   0xffffffffffffff01, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff
                               ])

    def test_equals(self):
        x = SimpleState.from_string(
            'P1 *  *  *  *  *  *  *  *  * \n' +
            'P2 *  *  *  *  *  *  *  *  * \n' +
            'P3 *  *  *  *  *  *  *  *  * \n' +
            'P4 *  *  *  * +TO+FU *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7 *  *  *  *  *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9 *  *  *  *  *  *  *  *  * \n' +
            '+'
        )
        y = SimpleState.from_string(
            'P1 *  *  *  *  *  *  *  *  * \n' +
            'P2 *  *  *  *  *  *  *  *  * \n' +
            'P3 *  *  *  *  *  *  *  *  * \n' +
            'P4 *  *  *  * +FU+TO *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7 *  *  *  *  *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9 *  *  *  *  *  *  *  *  * \n' +
            '+'
        )
        self.assertFalse(x == y)

    def test_repr(self):
        expect = ''.join([
            'SimpleState(turn=Turn(value=0), ',
            'owner_bits=0x0000000000000000, hand_bits=0x0000000000000000, promoted_bits=0x0000000000000000, ',
            'unused_bits=0x000000ffffffffff, board=BitBoard(000.000.000,000.000.000,000.000.000), ',
            'position=[0xffffffffffffffff,0xffffffffffffffff,0xffffffffffffffff,0xffffffffffffffff,0xffffffffffffffff])'
        ])
        self.assertEqual(repr(SimpleState()), expect)

    def test_set_turn(self):
        self.assertEqual(SimpleState().set_turn(WHITE.value), SimpleState(WHITE))

    def test_from_string(self):
        self.maxDiff = None

        # initiated expression
        e1 = SimpleState(BLACK, 0x0000008c01ff3335, 0, 0, 0, BitBoard(0o777202777, 0o777202777),
                         [0x50480800460a4010, 0x4f4907014e4a0602, 0x1918171615141312, 0x3c3b3a393837361a, 0x044c4d4b05033e3d])

        self.assertEqual(SimpleState.from_string('PI\n+'), e1)

        self.assertEqual(str(SimpleState.from_string('PI\n+')), '\n'.join([
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
        self.assertEqual(str(SimpleState.from_string('PI\n-')), '\n'.join([
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
            '-'
        ]))
        self.assertEqual(str(SimpleState.from_string('PI82HI22KA19KY\n-')), '\n'.join([
            'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY',
            'P2 *  *  *  *  *  *  *  *  * ',
            'P3-FU-FU-FU-FU-FU-FU-FU-FU-FU',
            'P4 *  *  *  *  *  *  *  *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  *  *  *  *  *  *  *  * ',
            'P7+FU+FU+FU+FU+FU+FU+FU+FU+FU',
            'P8 * +KA *  *  *  *  * +HI * ',
            'P9+KY+KE+GI+KI+OU+KI+GI+KE * ',
            'P+',
            'P-',
            '-'
        ]))

        # bundle expression
        self.assertEqual(str(SimpleState.from_string(
            'P1 *  *  *  *  *  *  *  *  * \n' +
            'P2 *  *  *  *  *  *  *  *  * \n' +
            'P3 *  *  *  *  *  *  *  *  * \n' +
            'P4 *  *  *  *  *  *  *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7 *  *  *  *  *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9 *  *  *  *  *  *  *  *  * \n' +
            '+'
        )),
            'P1 *  *  *  *  *  *  *  *  * \n' +
            'P2 *  *  *  *  *  *  *  *  * \n' +
            'P3 *  *  *  *  *  *  *  *  * \n' +
            'P4 *  *  *  *  *  *  *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7 *  *  *  *  *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9 *  *  *  *  *  *  *  *  * \n' +
            'P+\n' +
            'P-\n' +
            '+')

        self.assertEqual(str(SimpleState.from_string(
            'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY\n' +
            'P2 * -HI *  *  *  *  * -KA * \n' +
            'P3-FU-FU-FU-FU-FU-FU-FU-FU-FU\n' +
            'P4 *  *  *  *  *  *  *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7+FU+FU+FU+FU+FU+FU+FU+FU+FU\n' +
            'P8 * +KA *  *  *  *  * +HI * \n' +
            'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY\n' +
            '+'
        )),
            'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY\n' +
            'P2 * -HI *  *  *  *  * -KA * \n' +
            'P3-FU-FU-FU-FU-FU-FU-FU-FU-FU\n' +
            'P4 *  *  *  *  *  *  *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7+FU+FU+FU+FU+FU+FU+FU+FU+FU\n' +
            'P8 * +KA *  *  *  *  * +HI * \n' +
            'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY\n' +
            'P+\n' +
            'P-\n' +
            '+')

        self.assertEqual(str(SimpleState.from_string(
            'P1-TO *  *  *  *  *  *  * +TO\n' +
            'P2+TO *  *  *  *  *  *  * +FU\n' +
            'P3+TO *  *  *  *  *  *  * +TO\n' +
            'P4+TO *  *  *  *  *  *  * +TO\n' +
            'P5+TO *  *  *  *  *  *  * +TO\n' +
            'P6+TO *  *  *  *  *  *  * +TO\n' +
            'P7+TO *  *  *  *  *  *  * +TO\n' +
            'P8-FU *  *  *  *  *  *  * +TO\n' +
            'P9-TO *  *  *  *  *  *  * +TO\n' +
            '+'
        )),
            'P1-TO *  *  *  *  *  *  * +TO\n' +
            'P2+TO *  *  *  *  *  *  * +FU\n' +
            'P3+TO *  *  *  *  *  *  * +TO\n' +
            'P4+TO *  *  *  *  *  *  * +TO\n' +
            'P5+TO *  *  *  *  *  *  * +TO\n' +
            'P6+TO *  *  *  *  *  *  * +TO\n' +
            'P7+TO *  *  *  *  *  *  * +TO\n' +
            'P8-FU *  *  *  *  *  *  * +TO\n' +
            'P9-TO *  *  *  *  *  *  * +TO\n' +
            'P+\n' +
            'P-\n' +
            '+')

        # single expression
        self.assertEqual(str(SimpleState.from_string(
            'PI82HI22KA\nP+82HI22KA\n+'
        )), '\n'.join([
            'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY',
            'P2 * +HI *  *  *  *  * +KA * ',
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

        self.assertEqual(str(SimpleState.from_string(
            'P1 *  *  *  *  *  *  *  *  * \n' +
            'P2 *  *  *  *  *  *  *  *  * \n' +
            'P3 *  *  *  *  *  *  *  *  * \n' +
            'P4 *  *  *  *  *  *  *  *  * \n' +
            'P5 *  *  *  *  *  *  *  *  * \n' +
            'P6 *  *  *  *  *  *  *  *  * \n' +
            'P7 *  *  *  *  *  *  *  *  * \n' +
            'P8 *  *  *  *  *  *  *  *  * \n' +
            'P9 *  *  *  *  *  *  *  *  * \n' +
            'P+99KY\nP+89KE\nP+79GI\nP+69KI\nP+59OU\nP+49KI\nP+39GI\nP+29KE\nP+19KY\nP+88KA\nP+28HI\n' +
            'P+97FU\nP+87FU\nP+77FU\nP+67FU\nP+57FU\nP+47FU\nP+37FU\nP+27FU\nP+17FU\n' +
            'P-93FU\nP-83FU\nP-73FU\nP-63FU\nP-53FU\nP-43FU\nP-33FU\nP-23FU\nP-13FU\nP-82HI\nP-22KA\n' +
            'P-91KY\nP-81KE\nP-71GI\nP-61KI\nP-51OU\nP-41KI\nP-31GI\nP-21KE\nP-11KY\n' +
            '+'
        )), '\n'.join([
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

        self.assertEqual(str(SimpleState.from_string(
            "P+59OU00FU\nP-51OU\nP+00FU\nP+11UM\nP-12TO\nP-00AL\n-"
        )), '\n'.join([
            'P1 *  *  *  * -OU *  *  * +UM',
            'P2 *  *  *  *  *  *  *  * -TO',
            'P3 *  *  *  *  *  *  *  *  * ',
            'P4 *  *  *  *  *  *  *  *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  *  *  *  *  *  *  *  * ',
            'P7 *  *  *  *  *  *  *  *  * ',
            'P8 *  *  *  *  *  *  *  *  * ',
            'P9 *  *  *  * +OU *  *  *  * ',
            'P+00FU00FU',
            'P-00HI00HI00KA00KI00KI00KI00KI00GI00GI00GI00GI00KE00KE00KE00KE00KY00KY00KY00KY'
            '00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU',
            '-'
        ]))

        self.assertEqual(str(SimpleState.from_string("P+00AL\n-")), '\n'.join([
            'P1 *  *  *  *  *  *  *  *  * ',
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
            '-'
        ]))
        self.assertEqual(str(SimpleState.from_string("P-00AL\n-")), '\n'.join([
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
            'P-00HI00HI00KA00KA00KI00KI00KI00KI00GI00GI00GI00GI00KE00KE00KE00KE00KY00KY00KY00KY'
            '00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU',
            '-'
        ]))
        self.assertEqual(str(SimpleState.from_string(
            "P+51OU00AL\n+"
        )), '\n'.join([
            'P1 *  *  *  * +OU *  *  *  * ',
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
        self.assertEqual(str(SimpleState.from_string(
            "P+51OU\nP-00AL\n+"
        )), '\n'.join([
            'P1 *  *  *  * +OU *  *  *  * ',
            'P2 *  *  *  *  *  *  *  *  * ',
            'P3 *  *  *  *  *  *  *  *  * ',
            'P4 *  *  *  *  *  *  *  *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  *  *  *  *  *  *  *  * ',
            'P7 *  *  *  *  *  *  *  *  * ',
            'P8 *  *  *  *  *  *  *  *  * ',
            'P9 *  *  *  *  *  *  *  *  * ',
            'P+',
            'P-00HI00HI00KA00KA00KI00KI00KI00KI00GI00GI00GI00GI00KE00KE00KE00KE00KY00KY00KY00KY'
            '00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU',
            '+'
        ]))

        self.assertEqual(str(SimpleState.from_string(STR_TSUME_BLACK)), STR_TSUME_BLACK)
        self.assertEqual(str(SimpleState.from_string(STR_TSUME_WHITE)), STR_TSUME_WHITE)
        self.assertEqual(str(SimpleState.from_string(STR_MAX_LEGAL_MOVES)), STR_MAX_LEGAL_MOVES)

    def test_from_string_error(self):
        self.assertRaisesRegex(ValueError, '^Mal-formed state string', SimpleState.from_string, '')
        self.assertRaisesRegex(ValueError, '^Mal-formed CSA string for Turn', SimpleState.from_string, 'PI')
        self.assertRaisesRegex(ValueError, '^Mal-formed bundle expression', SimpleState.from_string, 'P1\n+')
        self.assertRaisesRegex(ValueError, '^Mal-formed bundle expression', SimpleState.from_string, '\n'.join([
            'P1 *  *  *  *  *  *  *  *  * ',
            'P2 *  *  *  *  *  *  *  *  * ',
            'P3 *  *  *  *  *  *  *  *  * ',
            'P4 *  *  *  *  *  *  *  *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  *  *  *  *  *  *  *  * ',
            'P7 *  *  *  *  *  *  *  *  * ',
            'P8 *  *  *  *  *  *  *  *  * ',
            'P9 *  *  *  *  *  *  *  *  *',
            'P+',
            '+']))
        self.assertRaisesRegex(ValueError, '^Mal-formed bundle expression', SimpleState.from_string, '\n'.join([
            'P1 *  *  *  *  *  *  *  *  * ',
            'P2 *  *  *  *  *  *  *  *  * ',
            'P3 *  *  *  *  *  *  *  *  * ',
            'P4 *  *  *  *  *  *  *  *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  *  *  *  *  *  *  *  * ',
            'P7 *  *  *  *  *  *  *  *  * ',
            'P8 *  *  *  *  *  *  *  *  * ',
            'P8 *  *  *  *  *  *  *  *  * ',
            'P+',
            '+']))
        self.assertRaisesRegex(ValueError, '^Unmatched piece type in initiated expression',
                               SimpleState.from_string, 'PI82KA\n+')
        self.assertRaisesRegex(ValueError, '^Position to remove is already empty',
                               SimpleState.from_string, 'PI82HI82HI\n+')
        self.assertRaisesRegex(ValueError, '^Position to remove is already empty',
                               SimpleState.from_string, 'PI55KA\nP-00AL55KA\n+')
        self.assertRaisesRegex(ValueError, '^Position to remove is already empty',
                               SimpleState.from_string, 'PI55KA\nP-00AL\nP-55KA\n+')

        self.assertRaisesRegex(ValueError, '^Mal-formed CSA string for Pos', SimpleState.from_string, 'PI8\n+')
        self.assertRaisesRegex(ValueError, '^Mal-formed CSA string for PieceType', SimpleState.from_string, 'PI82\n+')
        self.assertRaisesRegex(ValueError, '^Mal-formed CSA string for PieceType', SimpleState.from_string, 'PI82H\n+')
        self.assertRaisesRegex(ValueError, '^Mal-formed CSA string for PieceType',
                               SimpleState.from_string, 'P+00AL\nP-00AL\n+')

        # C++ errors
        self.assertRaisesRegex(ValueError, '^no left for the piece', SimpleState.from_string, 'P+11OU12OU\n+')
        self.assertRaisesRegex(ValueError, '^king in hand', SimpleState.from_string, 'P+00OU\n+')
        self.assertRaisesRegex(ValueError, '^promoted piece in hand', SimpleState.from_string, 'P+00TO\n+')
        self.assertRaisesRegex(ValueError, '^position already taken', SimpleState.from_string, 'P+55FU55KA\n+')
        self.assertRaisesRegex(ValueError, '^two pawns in the same file', SimpleState.from_string, 'P+12FU13FU\n+')
        self.assertRaisesRegex(ValueError, '^unmovable piece', SimpleState.from_string, 'P+11FU\n+')
        self.assertRaisesRegex(ValueError, '^unmovable piece', SimpleState.from_string, 'P+11KY\n+')
        self.assertRaisesRegex(ValueError, '^unmovable piece', SimpleState.from_string, 'P+12KE\n+')
        self.assertRaisesRegex(ValueError, '^unmovable piece', SimpleState.from_string, 'P-19FU\n+')
        self.assertRaisesRegex(ValueError, '^unmovable piece', SimpleState.from_string, 'P-19KY\n+')
        self.assertRaisesRegex(ValueError, '^unmovable piece', SimpleState.from_string, 'P-18KE\n+')

    def test_move(self):
        t = {}
        s = STATE_HIRATE
        for i in range(40):
            t[Pos(s.get_position(i))] = i

        s = s.move(t[P77], P76.value, False, -1)
        t[P76] = t[P77]
        del t[P77]
        self.assertEqual(str(SimpleState.wrap(s)), '\n'.join([
            'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY',
            'P2 * -HI *  *  *  *  * -KA * ',
            'P3-FU-FU-FU-FU-FU-FU-FU-FU-FU',
            'P4 *  *  *  *  *  *  *  *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  * +FU *  *  *  *  *  * ',
            'P7+FU+FU * +FU+FU+FU+FU+FU+FU',
            'P8 * +KA *  *  *  *  * +HI * ',
            'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY',
            'P+',
            'P-',
            '-'
        ]))

        s = s.move(t[P33], P34.value, False, -1)
        t[P34] = t[P33]
        del t[P33]
        self.assertEqual(str(SimpleState.wrap(s)), '\n'.join([
            'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY',
            'P2 * -HI *  *  *  *  * -KA * ',
            'P3-FU-FU-FU-FU-FU-FU * -FU-FU',
            'P4 *  *  *  *  *  * -FU *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  * +FU *  *  *  *  *  * ',
            'P7+FU+FU * +FU+FU+FU+FU+FU+FU',
            'P8 * +KA *  *  *  *  * +HI * ',
            'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY',
            'P+',
            'P-',
            '+'
        ]))

        s = s.move(t[P88], P22.value, True, t[P22])
        k1 = t[P22]
        t[P22] = t[P88]
        del t[P88]
        self.assertEqual(str(SimpleState.wrap(s)), '\n'.join([
            'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY',
            'P2 * -HI *  *  *  *  * +UM * ',
            'P3-FU-FU-FU-FU-FU-FU * -FU-FU',
            'P4 *  *  *  *  *  * -FU *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  * +FU *  *  *  *  *  * ',
            'P7+FU+FU * +FU+FU+FU+FU+FU+FU',
            'P8 *  *  *  *  *  *  * +HI * ',
            'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY',
            'P+00KA',
            'P-',
            '-'
        ]))

        s = s.move(t[P82], P22.value, False, t[P22])
        k2 = t[P22]
        t[P22] = t[P82]
        del t[P82]
        self.assertEqual(str(SimpleState.wrap(s)), '\n'.join([
            'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY',
            'P2 *  *  *  *  *  *  * -HI * ',
            'P3-FU-FU-FU-FU-FU-FU * -FU-FU',
            'P4 *  *  *  *  *  * -FU *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  * +FU *  *  *  *  *  * ',
            'P7+FU+FU * +FU+FU+FU+FU+FU+FU',
            'P8 *  *  *  *  *  *  * +HI * ',
            'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY',
            'P+00KA',
            'P-00KA',
            '+'
        ]))

        s = s.move(k1, P33.value, False, -1)
        t[P33] = k1
        self.assertEqual(str(SimpleState.wrap(s)), '\n'.join([
            'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY',
            'P2 *  *  *  *  *  *  * -HI * ',
            'P3-FU-FU-FU-FU-FU-FU+KA-FU-FU',
            'P4 *  *  *  *  *  * -FU *  * ',
            'P5 *  *  *  *  *  *  *  *  * ',
            'P6 *  * +FU *  *  *  *  *  * ',
            'P7+FU+FU * +FU+FU+FU+FU+FU+FU',
            'P8 *  *  *  *  *  *  * +HI * ',
            'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY',
            'P+',
            'P-00KA',
            '-'
        ]))

        s = s.move(k2, P95.value, False, -1)
        t[P95] = k2
        self.assertEqual(str(SimpleState.wrap(s)), '\n'.join([
            'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY',
            'P2 *  *  *  *  *  *  * -HI * ',
            'P3-FU-FU-FU-FU-FU-FU+KA-FU-FU',
            'P4 *  *  *  *  *  * -FU *  * ',
            'P5-KA *  *  *  *  *  *  *  * ',
            'P6 *  * +FU *  *  *  *  *  * ',
            'P7+FU+FU * +FU+FU+FU+FU+FU+FU',
            'P8 *  *  *  *  *  *  * +HI * ',
            'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY',
            'P+',
            'P-',
            '+'
        ]))

        s = s.move(t[P33], P51.value, True, t[P51])
        self.assertEqual(str(SimpleState.wrap(s)), '\n'.join([
            'P1-KY-KE-GI-KI+UM-KI-GI-KE-KY',
            'P2 *  *  *  *  *  *  * -HI * ',
            'P3-FU-FU-FU-FU-FU-FU * -FU-FU',
            'P4 *  *  *  *  *  * -FU *  * ',
            'P5-KA *  *  *  *  *  *  *  * ',
            'P6 *  * +FU *  *  *  *  *  * ',
            'P7+FU+FU * +FU+FU+FU+FU+FU+FU',
            'P8 *  *  *  *  *  *  * +HI * ',
            'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY',
            'P+',
            'P-',
            '-'
        ]))

    def test_from_string_prop(self):
        self.maxDiff = None
        for st in gen_state(100):
            result = SimpleState.from_string(str(st))
            self.assertEqual(result, st, '====\n%s\n==== is not equal to ====\n%s\n====' % (result, st))

    def test_get_num_hand(self):
        result1 = [STATE_HIRATE.get_num_hand(i, j) for i in range(2) for j in range(7)]
        self.assertEqual(result1, [0] * 14)

        result2 = [STATE_TSUME_BLACK.get_num_hand(i, j) for i in range(2) for j in range(7)]
        self.assertEqual(result2, [2, 2, 4, 4, 4, 18, 4] + [0] * 7)

        result3 = [STATE_TSUME_WHITE.get_num_hand(i, j) for i in range(2) for j in range(7)]
        self.assertEqual(result3, [0] * 7 + [2, 2, 4, 4, 4, 18, 4])

        result4 = [STATE_MAX_LEGAL_MOVES.get_num_hand(i, j) for i in range(2) for j in range(7)]
        self.assertEqual(result4, [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 3, 17, 3])
