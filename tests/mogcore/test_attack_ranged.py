import unittest
from cmogcore import Attack, BitBoard
from mogcore.bitboard import full, empty


class TestAttackRanged(unittest.TestCase):
    def test_get_attack_rance_black(self):
        self.assertEqual(Attack.get_attack(0, 3, 0, empty), empty)
        self.assertEqual(Attack.get_attack(0, 3, 40, empty), BitBoard(0o020, 0o020, 0o020, 0o020, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 53, empty), BitBoard(0o400, 0o400, 0o400, 0o400, 0o400, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 54, empty),
                         BitBoard(0o001, 0o001, 0o001, 0o001, 0o001, 0o001, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 80, empty),
                         BitBoard(0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0))
        self.assertEqual(Attack.get_attack(0, 3, 0, full), empty)
        self.assertEqual(Attack.get_attack(0, 3, 40, full), BitBoard(0, 0, 0, 0o020, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 53, full), BitBoard(0, 0, 0, 0, 0o400, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 54, full), BitBoard(0, 0, 0, 0, 0, 0o001, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 80, full), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0))
