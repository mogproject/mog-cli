import unittest
from mogcore import Attack, BitBoard, BLACK, WHITE, SILVER, KNIGHT, PAWN, KING, GOLD, PLANCE, PSILVER, PKNIGHT, PPAWN

full = BitBoard.FULL
empty = BitBoard.EMPTY


class TestAttackDirect(unittest.TestCase):

    def test_get_attack_silver(self):
        self.assertEqual(Attack.get_attack(BLACK, SILVER, 0), BitBoard(0, 0o002, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, SILVER, 40), BitBoard(0, 0, 0, 0o070, 0, 0o050, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, SILVER, 53), BitBoard(0, 0, 0, 0, 0o600, 0, 0o200, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, SILVER, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0, 0o002, 0))
        self.assertEqual(Attack.get_attack(BLACK, SILVER, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0))

        self.assertEqual(Attack.get_attack(WHITE, SILVER, 0), BitBoard(0, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, SILVER, 40), BitBoard(0, 0, 0, 0o050, 0, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, SILVER, 53), BitBoard(0, 0, 0, 0, 0o200, 0, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, SILVER, 54), BitBoard(0, 0, 0, 0, 0, 0o002, 0, 0o003, 0))
        self.assertEqual(Attack.get_attack(WHITE, SILVER, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o200, 0))

    def test_get_attack_knight(self):
        self.assertEqual(Attack.get_attack(BLACK, KNIGHT, 0), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, KNIGHT, 40), BitBoard(0, 0, 0o050, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, KNIGHT, 53), BitBoard(0, 0, 0, 0o200, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, KNIGHT, 54), BitBoard(0, 0, 0, 0, 0o002, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, KNIGHT, 80), BitBoard(0, 0, 0, 0, 0, 0, 0o200, 0, 0))

        self.assertEqual(Attack.get_attack(WHITE, KNIGHT, 0), BitBoard(0, 0, 0o002, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, KNIGHT, 40), BitBoard(0, 0, 0, 0, 0, 0, 0o050, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, KNIGHT, 53), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o200, 0))
        self.assertEqual(Attack.get_attack(WHITE, KNIGHT, 54), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0o002))
        self.assertEqual(Attack.get_attack(WHITE, KNIGHT, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0))

    def test_get_attack_pawn(self):
        self.assertEqual(Attack.get_attack(BLACK, PAWN, 0), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PAWN, 40), BitBoard(0, 0, 0, 0o020, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PAWN, 53), BitBoard(0, 0, 0, 0, 0o400, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PAWN, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PAWN, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0))

        self.assertEqual(Attack.get_attack(WHITE, PAWN, 0), BitBoard(0, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PAWN, 40), BitBoard(0, 0, 0, 0, 0, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PAWN, 53), BitBoard(0, 0, 0, 0, 0, 0, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PAWN, 54), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o001, 0))
        self.assertEqual(Attack.get_attack(WHITE, PAWN, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0))

    def test_get_attack_king(self):
        self.assertEqual(Attack.get_attack(BLACK, KING, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, KING, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, KING, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, KING, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(BLACK, KING, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(WHITE, KING, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, KING, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, KING, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, KING, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(WHITE, KING, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

    def test_get_attack_gold(self):
        self.assertEqual(Attack.get_attack(BLACK, GOLD, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, GOLD, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, GOLD, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, GOLD, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(BLACK, GOLD, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(WHITE, GOLD, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, GOLD, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, GOLD, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, GOLD, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(WHITE, GOLD, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))

    def test_get_attack_promoted_pawn(self):
        self.assertEqual(Attack.get_attack(BLACK, PPAWN, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PPAWN, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PPAWN, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PPAWN, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(BLACK, PPAWN, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(WHITE, PPAWN, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PPAWN, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PPAWN, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PPAWN, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(WHITE, PPAWN, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))

    def test_get_attack_promoted_lance(self):
        self.assertEqual(Attack.get_attack(BLACK, PLANCE, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PLANCE, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PLANCE, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PLANCE, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(BLACK, PLANCE, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(WHITE, PLANCE, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PLANCE, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PLANCE, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PLANCE, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(WHITE, PLANCE, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))

    def test_get_attack_promoted_knight(self):
        self.assertEqual(Attack.get_attack(BLACK, PKNIGHT, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PKNIGHT, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PKNIGHT, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PKNIGHT, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(BLACK, PKNIGHT, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(WHITE, PKNIGHT, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PKNIGHT, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PKNIGHT, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PKNIGHT, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(WHITE, PKNIGHT, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))

    def test_get_attack_promoted_silver(self):
        self.assertEqual(Attack.get_attack(BLACK, PSILVER, 0), BitBoard(0o002, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PSILVER, 40), BitBoard(0, 0, 0, 0o070, 0o050, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PSILVER, 53), BitBoard(0, 0, 0, 0, 0o600, 0o200, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, PSILVER, 54), BitBoard(0, 0, 0, 0, 0, 0o003, 0o002, 0o001, 0))
        self.assertEqual(Attack.get_attack(BLACK, PSILVER, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o600, 0o200))

        self.assertEqual(Attack.get_attack(WHITE, PSILVER, 0), BitBoard(0o002, 0o003, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PSILVER, 40), BitBoard(0, 0, 0, 0o020, 0o050, 0o070, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PSILVER, 53), BitBoard(0, 0, 0, 0, 0o400, 0o200, 0o600, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, PSILVER, 54), BitBoard(0, 0, 0, 0, 0, 0o001, 0o002, 0o003, 0))
        self.assertEqual(Attack.get_attack(WHITE, PSILVER, 80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0o200))
