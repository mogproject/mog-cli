import unittest
from mogcore import *
from tests.mogcore.state.gen_state import *


class TestState(unittest.TestCase):

    def test_constructor(self):
        s = State()
        self.assertEqual(s.turn, BLACK)
        self.assertEqual(s.owner_bits, 0)
        self.assertEqual(s.hand_bits, 0)
        self.assertEqual(s.promoted_bits, 0)
        self.assertEqual(s.unused_bits, 0x000000ffffffffff)
        self.assertEqual(s.board, BitBoard())
        self.assertEqual(s.position, [0xffffffffffffffff] * 5)

        s = State(WHITE)
        self.assertEqual(s.turn, WHITE)

    def test_constructor_error(self):
        self.assertRaises(ValueError, State, BLACK, 0, 0, 0, 0x000000ffffffffff, BitBoard(), [])
        self.assertRaises(ValueError, State, BLACK, 1, 0, 0, 0x000000ffffffffff, BitBoard())

    def test_set_turn(self):
        self.assertEqual(State().set_turn(WHITE.value), State(WHITE))

    def test_from_string(self):
        self.maxDiff = None

        # initiated expression
        e1 = State(BLACK, 0x0000008c01ff3335, 0, 0, 0, BitBoard(0o777202777, 0o777202777),
                   [0x50480800460a4010, 0x4f4907014e4a0602, 0x1918171615141312, 0x3c3b3a393837361a, 0x044c4d4b05033e3d])

        self.assertEqual(State.from_string('PI\n+'), e1)

        self.assertEqual(str(State.from_string('PI\n+')), '\n'.join([
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
        self.assertEqual(str(State.from_string('PI\n-')), '\n'.join([
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
        self.assertEqual(str(State.from_string('PI82HI22KA19KY\n-')), '\n'.join([
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
        self.assertEqual(str(State.from_string(
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

        self.assertEqual(str(State.from_string(
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

        # single expression
        self.assertEqual(str(State.from_string(
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

        self.assertEqual(str(State.from_string(
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

        self.assertEqual(str(State.from_string(
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

        self.assertEqual(str(State.from_string("P+00AL\n-")), '\n'.join([
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
        self.assertEqual(str(State.from_string("P-00AL\n-")), '\n'.join([
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
        self.assertEqual(str(State.from_string(
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
        self.assertEqual(str(State.from_string(
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

        self.assertEqual(str(State.from_string(STR_TSUME_BLACK)), STR_TSUME_BLACK)
        self.assertEqual(str(State.from_string(STR_TSUME_WHITE)), STR_TSUME_WHITE)
        self.assertEqual(str(State.from_string(STR_MAX_LEGAL_MOVES)), STR_MAX_LEGAL_MOVES)

    def test_from_string_error(self):
        self.assertRaisesRegexp(ValueError, '^Mal-formed state string', State.from_string, '')
        self.assertRaisesRegexp(ValueError, '^Mal-formed CSA string for Turn', State.from_string, 'PI')
        self.assertRaisesRegexp(ValueError, '^Mal-formed bundle expression', State.from_string, 'P1\n+')

        self.assertRaisesRegexp(ValueError, '^Unmatched piece type in initiated expression',
                                State.from_string, 'PI82KA\n+')
        self.assertRaisesRegexp(ValueError, '^Position to remove is already empty', State.from_string, 'PI82HI82HI\n+')
        self.assertRaisesRegexp(ValueError, '^Position to remove is already empty',
                                State.from_string, 'PI55KA\nP-00AL55KA\n+')
        self.assertRaisesRegexp(ValueError, '^Position to remove is already empty',
                                State.from_string, 'PI55KA\nP-00AL\nP-55KA\n+')

        self.assertRaisesRegexp(ValueError, '^Mal-formed CSA string for Pos', State.from_string, 'PI8\n+')
        self.assertRaisesRegexp(ValueError, '^Mal-formed CSA string for PieceType', State.from_string, 'PI82\n+')
        self.assertRaisesRegexp(ValueError, '^Mal-formed CSA string for PieceType', State.from_string, 'PI82H\n+')
        self.assertRaisesRegexp(ValueError, '^Mal-formed CSA string for PieceType',
                                State.from_string, 'P+00AL\nP-00AL\n+')

        # C++ errors
        self.assertRaisesRegexp(ValueError, '^no left for the piece', State.from_string, 'P+11OU12OU\n+')
        self.assertRaisesRegexp(ValueError, '^king in hand', State.from_string, 'P+00OU\n+')
        self.assertRaisesRegexp(ValueError, '^promoted piece in hand', State.from_string, 'P+00TO\n+')
        self.assertRaisesRegexp(ValueError, '^position already taken', State.from_string, 'P+55FU55KA\n+')
        self.assertRaisesRegexp(ValueError, '^two pawns in the same file', State.from_string, 'P+12FU13FU\n+')
        self.assertRaisesRegexp(ValueError, '^unmovable piece', State.from_string, 'P+11FU\n+')
        self.assertRaisesRegexp(ValueError, '^unmovable piece', State.from_string, 'P+11KY\n+')
        self.assertRaisesRegexp(ValueError, '^unmovable piece', State.from_string, 'P+12KE\n+')
        self.assertRaisesRegexp(ValueError, '^unmovable piece', State.from_string, 'P-19FU\n+')
        self.assertRaisesRegexp(ValueError, '^unmovable piece', State.from_string, 'P-19KY\n+')
        self.assertRaisesRegexp(ValueError, '^unmovable piece', State.from_string, 'P-18KE\n+')
