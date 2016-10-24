import unittest
from mogcore import *
import cmogcore


class TestMove(unittest.TestCase):

    def test_init(self):
        m1 = Move(BLACK, P77, P76, PAWN)
        self.assertEqual(m1.turn, BLACK)
        self.assertEqual(m1.from_, P77)
        self.assertEqual(m1.to, P76)
        self.assertEqual(m1.piece_type, PAWN)
        self.assertEqual(m1.elapsed_time, -1)

        m2 = Move(WHITE, P33, P34, PAWN, 123)
        self.assertEqual(m2.turn, WHITE)
        self.assertEqual(m2.from_, P33)
        self.assertEqual(m2.to, P34)
        self.assertEqual(m2.piece_type, PAWN)
        self.assertEqual(m2.elapsed_time, 123)

    def test_str(self):
        self.assertEqual(str(Move(BLACK, P77, P76, PAWN)), '+7776FU')
        self.assertEqual(str(Move(BLACK, P77, P76, PAWN, 0)), '+7776FU,T0')
        self.assertEqual(str(Move(BLACK, P77, P76, PAWN, 123)), '+7776FU,T123')

    def test_wrap(self):
        r01 = cmogcore.Move(BLACK.value, P77.value, P76.value, PAWN.value, -1, 0, 0)
        r02 = cmogcore.Move(BLACK.value, P77.value, P76.value, PAWN.value, 123, 0, 0)
        r03 = cmogcore.Move(BLACK.value, P77.value, P76.value, PAWN.value, 0x7fffffff, 0, 0)

        r11 = cmogcore.Move(0, 0, 0, 0, -1, 1, 3)
        r12 = cmogcore.Move(0, 0, 0, 0, 123, 1, 3)
        r13 = cmogcore.Move(0, 0, 0, 0, 0x7fffffff, 1, 3)

        r21 = cmogcore.Move(0, 0, 0, 0, -1, 2, 3)
        r22 = cmogcore.Move(0, 0, 0, 0, 123, 2, 3)
        r23 = cmogcore.Move(0, 0, 0, 0, 0x7fffffff, 2, 3)

        r31 = cmogcore.Move(0, 0, 0, 0, -1, 3, 3)
        r32 = cmogcore.Move(0, 0, 0, 0, 123, 3, 3)
        r33 = cmogcore.Move(0, 0, 0, 0, 0x7fffffff, 3, 3)

        r41 = cmogcore.Move(0, 0, 0, 0, -1, 4, 3)

        r51 = cmogcore.Move(0, 0, 0, 0, -1, 5, 2)
        r52 = cmogcore.Move(0, 0, 0, 0, 123, 5, 2)
        r53 = cmogcore.Move(0, 0, 0, 0, 0x7fffffff, 5, 2)

        r61 = cmogcore.Move(0, 0, 0, 0, -1, 6, 1)

        self.assertEqual(Move.wrap(r01), Move(BLACK, P77, P76, PAWN))
        self.assertEqual(Move.wrap(r02), Move(BLACK, P77, P76, PAWN, 123))
        self.assertEqual(Move.wrap(r03), Move(BLACK, P77, P76, PAWN, 0x7fffffff))

        self.assertEqual(Move.wrap(r11), Resign())
        self.assertEqual(Move.wrap(r12), Resign(123))
        self.assertEqual(Move.wrap(r13), Resign(0x7fffffff))

        self.assertEqual(Move.wrap(r21), TimeUp())
        self.assertEqual(Move.wrap(r22), TimeUp(123))
        self.assertEqual(Move.wrap(r23), TimeUp(0x7fffffff))

        self.assertEqual(Move.wrap(r31), IllegalMove())
        self.assertEqual(Move.wrap(r32), IllegalMove(123))
        self.assertEqual(Move.wrap(r33), IllegalMove(0x7fffffff))

        self.assertEqual(Move.wrap(r41), PerpetualCheck())

        self.assertEqual(Move.wrap(r51), DeclareWin())
        self.assertEqual(Move.wrap(r52), DeclareWin(123))
        self.assertEqual(Move.wrap(r53), DeclareWin(0x7fffffff))

        self.assertEqual(Move.wrap(r61), ThreefoldRepetition())

    def test_from_string(self):
        self.assertEqual(Move.from_string('+7776FU'), Move(BLACK, P77, P76, PAWN))
        self.assertEqual(Move.from_string('+7776FU,T0'), Move(BLACK, P77, P76, PAWN, 0))
        self.assertEqual(Move.from_string('+7776FU,T123'), Move(BLACK, P77, P76, PAWN, 123))
        self.assertEqual(Move.from_string('+7776FU,T9'), Move(BLACK, P77, P76, PAWN, 9))
        self.assertEqual(Move.from_string('+7776FU,T99'), Move(BLACK, P77, P76, PAWN, 99))
        self.assertEqual(Move.from_string('+7776FU,T999'), Move(BLACK, P77, P76, PAWN, 999))
        self.assertEqual(Move.from_string('+7776FU,T9999'), Move(BLACK, P77, P76, PAWN, 9999))
        self.assertEqual(Move.from_string('+7776FU,T99999'), Move(BLACK, P77, P76, PAWN, 99999))
        self.assertEqual(Move.from_string('%TORYO'), Resign())
        self.assertEqual(Move.from_string('%TORYO,T123'), Resign(123))
        self.assertEqual(Move.from_string('#TIME_UP'), TimeUp())
        self.assertEqual(Move.from_string('#TIME_UP,T123'), TimeUp(123))
        self.assertEqual(Move.from_string('#ILLEGAL_MOVE'), IllegalMove())
        self.assertEqual(Move.from_string('#ILLEGAL_MOVE,T123'), IllegalMove(123))
        self.assertEqual(Move.from_string('#OUTE_SENNICHITE'), PerpetualCheck())
        self.assertEqual(Move.from_string('%KACHI'), DeclareWin())
        self.assertEqual(Move.from_string('%KACHI,T123'), DeclareWin(123))
        self.assertEqual(Move.from_string('#SENNICHITE'), ThreefoldRepetition())

    def test_from_string_error(self):
        expected = '^Mal-formed CSA string for Move: '

        self.assertRaisesRegex(ValueError, expected, Move.from_string, '')
        self.assertRaisesRegex(ValueError, expected, Move.from_string, '+')
        self.assertRaisesRegex(ValueError, expected, Move.from_string, '+7776FU,')
        self.assertRaisesRegex(ValueError, expected, Move.from_string, '+7776FU,T')
        self.assertRaisesRegex(ValueError, expected, Move.from_string, '+7776FU,T-1')
        self.assertRaisesRegex(ValueError, expected, Move.from_string, '+7776FU,T1,T1')
        self.assertRaisesRegex(AssertionError, 'from_ and to must not be same', Move.from_string, '+7777FU')
        self.assertRaisesRegex(AssertionError, 'from_ and to must not be same', Move.from_string, '+7777FU,T1')
        self.assertRaisesRegex(ValueError, expected, Move.from_string, '+7776FU,T100000')
        self.assertRaisesRegex(ValueError, expected, Move.from_string, '+7776FU,T2147483647')
        self.assertRaisesRegex(ValueError, expected, Move.from_string, '%')
        self.assertRaisesRegex(ValueError, expected, Move.from_string, '%A')
        self.assertRaisesRegex(ValueError, expected, Move.from_string, '%A,T0')
        self.assertRaisesRegex(ValueError, expected, Move.from_string, '#A')
        self.assertRaisesRegex(ValueError, expected, Move.from_string, '#A,T0')
        self.assertRaisesRegex(ValueError, expected, Move.from_string, '#OUTE_SENNICHITE,T123')
        self.assertRaisesRegex(ValueError, expected, Move.from_string, '#SENNICHITE,T123')


class TestResign(unittest.TestCase):

    def test_str(self):
        self.assertEqual(str(Resign()), '%TORYO')
        self.assertEqual(str(Resign(123)), '%TORYO,T123')


class TestTimeUp(unittest.TestCase):

    def test_str(self):
        self.assertEqual(str(TimeUp()), '#TIME_UP')
        self.assertEqual(str(TimeUp(123)), '#TIME_UP,T123')


class TestIllegalMove(unittest.TestCase):

    def test_str(self):
        self.assertEqual(str(IllegalMove()), '#ILLEGAL_MOVE')
        self.assertEqual(str(IllegalMove(123)), '#ILLEGAL_MOVE,T123')


class TestPerpetualCheck(unittest.TestCase):

    def test_str(self):
        self.assertEqual(str(PerpetualCheck()), '#OUTE_SENNICHITE')


class TestDeclareWin(unittest.TestCase):

    def test_str(self):
        self.assertEqual(str(DeclareWin()), '%KACHI')
        self.assertEqual(str(DeclareWin(123)), '%KACHI,T123')


class TestThreefoldRepetition(unittest.TestCase):

    def test_str(self):
        self.assertEqual(str(ThreefoldRepetition()), '#SENNICHITE')
