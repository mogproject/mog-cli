import unittest
import util


class TestListUtil(unittest.TestCase):
    def test_grouped(self):
        self.assertEqual(util.grouped([], 4), [])
        self.assertEqual(util.grouped([10], 4), [[10]])
        self.assertEqual(util.grouped([10, 20], 4), [[10, 20]])
        self.assertEqual(util.grouped([10, 20, 30], 4), [[10, 20, 30]])
        self.assertEqual(util.grouped([10, 20, 30, 40], 4), [[10, 20, 30, 40]])
        self.assertEqual(util.grouped([10, 20, 30, 40, 50], 4), [[10, 20, 30, 40], [50]])

        self.assertEqual(util.grouped('', 4), [])
        self.assertEqual(util.grouped('a', 4), ['a'])
        self.assertEqual(util.grouped('ab', 4), ['ab'])
        self.assertEqual(util.grouped('abc', 4), ['abc'])
        self.assertEqual(util.grouped('abcd', 4), ['abcd'])
        self.assertEqual(util.grouped('abcde', 4), ['abcd', 'e'])

        self.assertRaises(ValueError, util.grouped, 'abc', -1)
        self.assertRaises(ValueError, util.grouped, 'abc', 0)
