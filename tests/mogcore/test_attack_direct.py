import unittest
from cmogcore import Attack, BitBoard


class TestAttackDirect(unittest.TestCase):
    def test_get_attack_king(self):
        self.assertEqual(Attack.get_attack(0, 0, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 0, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 0, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(0, 0, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(0, 0, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(1, 0, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 0, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 0, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(1, 0, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(1, 0, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

    def test_get_attack_gold(self):
        self.assertEqual(Attack.get_attack(0, 4, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 4, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 4, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(0, 4, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(0, 4, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(1, 4, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 4, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 4, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(1, 4, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(1, 4, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))

    def test_get_attack_silver(self):
        self.assertEqual(Attack.get_attack(0, 5, 0), BitBoard(0, 0o002, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 5, 40), BitBoard(0, 0, 0, 0o070, 0, 0o050, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 5, 53), BitBoard(0, 0, 0, 0, 0o600, 0, 0o200, 0, 0))
        self.assertEqual(Attack.get_attack(0, 5, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0, 0o002, 0))
        self.assertEqual(Attack.get_attack(0, 5, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0))

        self.assertEqual(Attack.get_attack(1, 5, 0), BitBoard(0, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 5, 40), BitBoard(0, 0, 0, 0o050, 0, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 5, 53), BitBoard(0, 0, 0, 0, 0o200, 0, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(1, 5, 54), BitBoard(0, 0, 0, 0, 0, 0o002, 0, 0o003, 0))
        self.assertEqual(Attack.get_attack(1, 5, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o200, 0))

    def test_get_attack_knight(self):
        self.assertEqual(Attack.get_attack(0, 6, 0), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 6, 40), BitBoard(0, 0, 0o050, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 6, 53), BitBoard(0, 0, 0, 0o200, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 6, 54), BitBoard(0, 0, 0, 0, 0o002, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 6, 80), BitBoard(0, 0, 0, 0, 0, 0, 0o200, 0, 0))

        self.assertEqual(Attack.get_attack(1, 6, 0), BitBoard(0, 0, 0o002, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 6, 40), BitBoard(0, 0, 0, 0, 0, 0, 0o050, 0, 0))
        self.assertEqual(Attack.get_attack(1, 6, 53), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o200, 0))
        self.assertEqual(Attack.get_attack(1, 6, 54), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0o002))
        self.assertEqual(Attack.get_attack(1, 6, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0))

    def test_get_attack_pawn(self):
        self.assertEqual(Attack.get_attack(0, 7, 0), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 7, 40), BitBoard(0, 0, 0, 0o020, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 7, 53), BitBoard(0, 0, 0, 0, 0o400, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 7, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 7, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0))

        self.assertEqual(Attack.get_attack(1, 7, 0), BitBoard(0, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 7, 40), BitBoard(0, 0, 0, 0, 0, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 7, 53), BitBoard(0, 0, 0, 0, 0, 0, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(1, 7, 54), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o001, 0))
        self.assertEqual(Attack.get_attack(1, 7, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0))

    def test_get_attack_promoted_pawn(self):
        self.assertEqual(Attack.get_attack(0, 15, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 15, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 15, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(0, 15, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(0, 15, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(1, 15, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 15, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 15, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(1, 15, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(1, 15, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))

    def test_get_attack_promoted_lance(self):
        self.assertEqual(Attack.get_attack(0, 11, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 11, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 11, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(0, 11, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(0, 11, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(1, 11, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 11, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 11, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(1, 11, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(1, 11, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))

    def test_get_attack_promoted_knight(self):
        self.assertEqual(Attack.get_attack(0, 14, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 14, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 14, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(0, 14, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(0, 14, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(1, 14, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 14, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 14, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(1, 14, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(1, 14, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))

    def test_get_attack_promoted_silver(self):
        self.assertEqual(Attack.get_attack(0, 13, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 13, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(0, 13, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(0, 13, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(0, 13, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(1, 13, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 13, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(1, 13, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(1, 13, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(1, 13, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))
