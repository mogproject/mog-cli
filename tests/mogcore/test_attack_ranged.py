import unittest
from cmogcore import Attack, BitBoard
from mogcore.bitboard import full, empty


class TestAttackRanged(unittest.TestCase):
    def test_get_attack_lance_black(self):
        self.assertEqual(Attack.get_attack(0, 3, 0, empty), empty)
        self.assertEqual(Attack.get_attack(0, 3, 40, empty), BitBoard(0o020, 0o020, 0o020, 0o020, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 53, empty), BitBoard(0o400, 0o400, 0o400, 0o400, 0o400, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 54, empty),
                         BitBoard(0o001, 0o001, 0o001, 0o001, 0o001, 0o001, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 80, empty),
                         BitBoard(0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0))
        self.assertEqual(Attack.get_attack(0, 3, 0, full), empty)
        self.assertEqual(Attack.get_attack(0, 3, 18, empty), BitBoard(0o001, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 18, BitBoard(0o001, 0, 0, 0, 0, 0, 0, 0, 0)),
                         BitBoard(0o001, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 18, BitBoard(0, 0o001, 0, 0, 0, 0, 0, 0, 0)),
                         BitBoard(0o000, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 18, BitBoard(0o001, 0o001, 0, 0, 0, 0, 0, 0, 0)),
                         BitBoard(0o000, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 40, full), BitBoard(0, 0, 0, 0o020, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 8, full), empty)
        self.assertEqual(Attack.get_attack(0, 3, 17, full), BitBoard(0o400, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 26, full), BitBoard(0, 0o400, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 35, full), BitBoard(0, 0, 0o400, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 44, full), BitBoard(0, 0, 0, 0o400, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 53, full), BitBoard(0, 0, 0, 0, 0o400, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 62, full), BitBoard(0, 0, 0, 0, 0, 0o400, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 71, full), BitBoard(0, 0, 0, 0, 0, 0, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 54, full), BitBoard(0, 0, 0, 0, 0, 0o001, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 3, 80, full), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0))
