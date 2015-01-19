import unittest
from cmogcore import Attack, BitBoard


class TestAttack(unittest.TestCase):
    def test_max_attack(self):
        self.assertEqual(Attack.xxx, BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
