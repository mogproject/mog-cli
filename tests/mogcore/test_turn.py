import unittest
from mogcore import Turn, BLACK, WHITE
from .gen_turn import gen_turn


class TestTurn(unittest.TestCase):
    def test_init(self):
        self.assertEqual(Turn(), Turn(0))
        self.assertEqual(Turn(1), WHITE)

    def test_init_invalid(self):
        self.assertRaises(AssertionError, Turn, 2)
        self.assertRaises(AssertionError, Turn, 'xxx')

    def test_value(self):
        self.assertEqual(BLACK.value, 0)
        self.assertEqual(WHITE.value, 1)

    def test_str(self):
        self.assertEqual(str(BLACK), '+')
        self.assertEqual(str(WHITE), '-')

    def test_invert(self):
        self.assertEqual(~BLACK, WHITE)
        self.assertEqual(~WHITE, BLACK)

    def test_from_string(self):
        self.assertEqual(Turn.from_string('+'), BLACK)
        self.assertEqual(Turn.from_string('-'), WHITE)

    def test_from_string_invalid(self):
        self.assertIsNone(Turn.from_string(''))
        self.assertIsNone(Turn.from_string(0))

    def test_prop_double_invert(self):
        for t in gen_turn(100):
            self.assertEqual(~~t, t)
