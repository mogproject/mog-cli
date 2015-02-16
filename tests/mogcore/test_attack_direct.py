import unittest
from mogcore import Attack, BitBoard, BLACK, WHITE

full = BitBoard.FULL
empty = BitBoard.EMPTY


class TestAttackDirect(unittest.TestCase):
    def test_get_attack_king(self):
        self.assertEqual(Attack.get_attack(BLACK, 0, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 0, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 0, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 0, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(BLACK, 0, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(WHITE, 0, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 0, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 0, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 0, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(WHITE, 0, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

    def test_get_attack_gold(self):
        self.assertEqual(Attack.get_attack(BLACK, 4, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 4, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 4, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 4, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(BLACK, 4, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(WHITE, 4, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 4, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 4, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 4, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(WHITE, 4, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))

    def test_get_attack_silver(self):
        self.assertEqual(Attack.get_attack(BLACK, 5, 0), BitBoard(0, 0o002, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 5, 40), BitBoard(0, 0, 0, 0o070, 0, 0o050, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 5, 53), BitBoard(0, 0, 0, 0, 0o600, 0, 0o200, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 5, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0, 0o002, 0))
        self.assertEqual(Attack.get_attack(BLACK, 5, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0))

        self.assertEqual(Attack.get_attack(WHITE, 5, 0), BitBoard(0, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 5, 40), BitBoard(0, 0, 0, 0o050, 0, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 5, 53), BitBoard(0, 0, 0, 0, 0o200, 0, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 5, 54), BitBoard(0, 0, 0, 0, 0, 0o002, 0, 0o003, 0))
        self.assertEqual(Attack.get_attack(WHITE, 5, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o200, 0))

    def test_get_attack_knight(self):
        self.assertEqual(Attack.get_attack(BLACK, 6, 0), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 6, 40), BitBoard(0, 0, 0o050, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 6, 53), BitBoard(0, 0, 0, 0o200, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 6, 54), BitBoard(0, 0, 0, 0, 0o002, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 6, 80), BitBoard(0, 0, 0, 0, 0, 0, 0o200, 0, 0))

        self.assertEqual(Attack.get_attack(WHITE, 6, 0), BitBoard(0, 0, 0o002, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 6, 40), BitBoard(0, 0, 0, 0, 0, 0, 0o050, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 6, 53), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o200, 0))
        self.assertEqual(Attack.get_attack(WHITE, 6, 54), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0o002))
        self.assertEqual(Attack.get_attack(WHITE, 6, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0))

    def test_get_attack_pawn(self):
        self.assertEqual(Attack.get_attack(BLACK, 7, 0), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 7, 40), BitBoard(0, 0, 0, 0o020, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 7, 53), BitBoard(0, 0, 0, 0, 0o400, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 7, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 7, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0))

        self.assertEqual(Attack.get_attack(WHITE, 7, 0), BitBoard(0, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 7, 40), BitBoard(0, 0, 0, 0, 0, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 7, 53), BitBoard(0, 0, 0, 0, 0, 0, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 7, 54), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o001, 0))
        self.assertEqual(Attack.get_attack(WHITE, 7, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0))

    def test_get_attack_promoted_pawn(self):
        self.assertEqual(Attack.get_attack(BLACK, 15, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 15, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 15, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 15, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(BLACK, 15, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(WHITE, 15, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 15, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 15, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 15, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(WHITE, 15, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))

    def test_get_attack_promoted_lance(self):
        self.assertEqual(Attack.get_attack(BLACK, 11, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 11, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 11, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 11, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(BLACK, 11, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(WHITE, 11, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 11, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 11, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 11, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(WHITE, 11, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))

    def test_get_attack_promoted_knight(self):
        self.assertEqual(Attack.get_attack(BLACK, 14, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 14, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 14, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 14, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(BLACK, 14, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(WHITE, 14, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 14, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 14, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 14, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(WHITE, 14, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))

    def test_get_attack_promoted_silver(self):
        self.assertEqual(Attack.get_attack(BLACK, 13, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 13, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 13, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, 13, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(BLACK, 13, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(WHITE, 13, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 13, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 13, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, 13, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(WHITE, 13, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))
