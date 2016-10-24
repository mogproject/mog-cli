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

    def test_wrap(self):
        r01 = cmogcore.ExtendedMove(BLACK.value, P77.value, P76.value, PAWN.value, -1, 0, 0)
        r02 = cmogcore.ExtendedMove(BLACK.value, P77.value, P76.value, PAWN.value, 123, 0, 0)
        r03 = cmogcore.ExtendedMove(BLACK.value, P77.value, P76.value, PAWN.value, 0x7fffffff, 0, 0)

        r11 = cmogcore.ExtendedMove(0, 0, 0, 0, -1, 1, 3)
        r12 = cmogcore.ExtendedMove(0, 0, 0, 0, 123, 1, 3)
        r13 = cmogcore.ExtendedMove(0, 0, 0, 0, 0x7fffffff, 1, 3)

        r21 = cmogcore.ExtendedMove(0, 0, 0, 0, -1, 2, 3)
        r22 = cmogcore.ExtendedMove(0, 0, 0, 0, 123, 2, 3)
        r23 = cmogcore.ExtendedMove(0, 0, 0, 0, 0x7fffffff, 2, 3)

        r31 = cmogcore.ExtendedMove(0, 0, 0, 0, -1, 3, 3)
        r32 = cmogcore.ExtendedMove(0, 0, 0, 0, 123, 3, 3)
        r33 = cmogcore.ExtendedMove(0, 0, 0, 0, 0x7fffffff, 3, 3)

        r41 = cmogcore.ExtendedMove(0, 0, 0, 0, -1, 4, 3)

        r51 = cmogcore.ExtendedMove(0, 0, 0, 0, -1, 5, 2)
        r52 = cmogcore.ExtendedMove(0, 0, 0, 0, 123, 5, 2)
        r53 = cmogcore.ExtendedMove(0, 0, 0, 0, 0x7fffffff, 5, 2)

        r61 = cmogcore.ExtendedMove(0, 0, 0, 0, -1, 6, 1)

        self.assertEqual(ExtendedMove.wrap(r01), ExtendedMove(BLACK, P77, P76, PAWN))
        self.assertEqual(ExtendedMove.wrap(r02), ExtendedMove(BLACK, P77, P76, PAWN, 123))
        self.assertEqual(ExtendedMove.wrap(r03), ExtendedMove(BLACK, P77, P76, PAWN, 0x7fffffff))

        self.assertEqual(ExtendedMove.wrap(r11), Resign())
        self.assertEqual(ExtendedMove.wrap(r12), Resign(123))
        self.assertEqual(ExtendedMove.wrap(r13), Resign(0x7fffffff))

        self.assertEqual(ExtendedMove.wrap(r21), TimeUp())
        self.assertEqual(ExtendedMove.wrap(r22), TimeUp(123))
        self.assertEqual(ExtendedMove.wrap(r23), TimeUp(0x7fffffff))

        self.assertEqual(ExtendedMove.wrap(r31), IllegalMove())
        self.assertEqual(ExtendedMove.wrap(r32), IllegalMove(123))
        self.assertEqual(ExtendedMove.wrap(r33), IllegalMove(0x7fffffff))

        self.assertEqual(ExtendedMove.wrap(r41), PerpetualCheck())

        self.assertEqual(ExtendedMove.wrap(r51), DeclareWin())
        self.assertEqual(ExtendedMove.wrap(r52), DeclareWin(123))
        self.assertEqual(ExtendedMove.wrap(r53), DeclareWin(0x7fffffff))

        self.assertEqual(ExtendedMove.wrap(r61), ThreefoldRepetition())

    def test_from_string(self):
        self.assertEqual(ExtendedMove.from_string('+7776FU'), ExtendedMove(BLACK, P77, P76, PAWN))
        self.assertEqual(ExtendedMove.from_string('+7776FU,T0'), ExtendedMove(BLACK, P77, P76, PAWN, 0))
        self.assertEqual(ExtendedMove.from_string('+7776FU,T123'), ExtendedMove(BLACK, P77, P76, PAWN, 123))
        self.assertEqual(ExtendedMove.from_string('+7776FU,T9'), ExtendedMove(BLACK, P77, P76, PAWN, 9))
        self.assertEqual(ExtendedMove.from_string('+7776FU,T99'), ExtendedMove(BLACK, P77, P76, PAWN, 99))
        self.assertEqual(ExtendedMove.from_string('+7776FU,T999'), ExtendedMove(BLACK, P77, P76, PAWN, 999))
        self.assertEqual(ExtendedMove.from_string('+7776FU,T9999'), ExtendedMove(BLACK, P77, P76, PAWN, 9999))
        self.assertEqual(ExtendedMove.from_string('+7776FU,T99999'), ExtendedMove(BLACK, P77, P76, PAWN, 99999))
        self.assertEqual(ExtendedMove.from_string('%TORYO'), Resign())
        self.assertEqual(ExtendedMove.from_string('%TORYO,T123'), Resign(123))
        self.assertEqual(ExtendedMove.from_string('#TIME_UP'), TimeUp())
        self.assertEqual(ExtendedMove.from_string('#TIME_UP,T123'), TimeUp(123))
        self.assertEqual(ExtendedMove.from_string('#ILLEGAL_MOVE'), IllegalMove())
        self.assertEqual(ExtendedMove.from_string('#ILLEGAL_MOVE,T123'), IllegalMove(123))
        self.assertEqual(ExtendedMove.from_string('#OUTE_SENNICHITE'), PerpetualCheck())
        self.assertEqual(ExtendedMove.from_string('%KACHI'), DeclareWin())
        self.assertEqual(ExtendedMove.from_string('%KACHI,T123'), DeclareWin(123))
        self.assertEqual(ExtendedMove.from_string('#SENNICHITE'), ThreefoldRepetition())

    def test_from_string_error(self):
        expected = '^Mal-formed CSA string for ExtendedMove: '

        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '')
        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '+')
        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '+7776FU,')
        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '+7776FU,T')
        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '+7776FU,T-1')
        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '+7776FU,T1,T1')
        self.assertRaisesRegex(AssertionError, 'from_ and to must not be same', ExtendedMove.from_string, '+7777FU')
        self.assertRaisesRegex(AssertionError, 'from_ and to must not be same', ExtendedMove.from_string, '+7777FU,T1')
        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '+7776FU,T100000')
        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '+7776FU,T2147483647')
        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '%')
        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '%A')
        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '%A,T0')
        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '#A')
        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '#A,T0')
        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '#OUTE_SENNICHITE,T123')
        self.assertRaisesRegex(ValueError, expected, ExtendedMove.from_string, '#SENNICHITE,T123')


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
