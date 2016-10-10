import unittest
from mogcore import Attack, BitBoard, BLACK, WHITE, LANCE, KNIGHT, ROOK, BISHOP, SILVER, GOLD

full = BitBoard.FULL
empty = BitBoard.EMPTY


class TestAttackAerial(unittest.TestCase):

    def test_get_attack_invalid(self):
        for owner in range(2):
            for ptype in list(range(7, 16)):
                for occ in [full, empty]:
                    self.assertEqual(Attack.get_attack(owner, ptype, occ), empty)

    def test_get_attack_pawn(self):
        self.assertEqual(Attack.get_attack(BLACK, empty, empty),
                         BitBoard(0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(Attack.get_attack(WHITE, empty, empty),
                         BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0))
        self.assertEqual(Attack.get_attack(BLACK, empty, BitBoard(0, 0, 0, 0, 0o777, 0, 0, 0, 0)), empty)
        self.assertEqual(Attack.get_attack(BLACK, full, BitBoard(0, 0, 0, 0, 0o777, 0, 0, 0, 0)), empty)
        self.assertEqual(Attack.get_attack(WHITE, empty, BitBoard(0, 0, 0, 0, 0o777, 0, 0, 0, 0)), empty)
        self.assertEqual(Attack.get_attack(WHITE, full, BitBoard(0, 0, 0, 0, 0o777, 0, 0, 0, 0)), empty)
        self.assertEqual(Attack.get_attack(WHITE, BitBoard(0, 0o777, 0, 0, 0, 0, 0, 0o777, 0),
                                           BitBoard(0, 0o555, 0, 0, 0, 0, 0, 0o111, 0)),
                         BitBoard(0o222, 0, 0o222, 0o222, 0o222, 0o222, 0o222, 0, 0))

    def test_get_attack_lance(self):
        self.assertEqual(Attack.get_attack(BLACK, LANCE, empty),
                         BitBoard(0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(Attack.get_attack(WHITE, LANCE, empty),
                         BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0))
        self.assertEqual(Attack.get_attack(BLACK, LANCE, full), empty)
        self.assertEqual(Attack.get_attack(WHITE, LANCE, full), empty)
        self.assertEqual(Attack.get_attack(BLACK, LANCE,
                                           BitBoard(0o001, 0o002, 0o004, 0o010, 0o020, 0o040, 0o100, 0o200, 0o400)),
                         BitBoard(0, 0o775, 0o773, 0o767, 0o757, 0o737, 0o677, 0o577, 0o377))
        self.assertEqual(Attack.get_attack(WHITE, LANCE,
                                           BitBoard(0o001, 0o002, 0o004, 0o010, 0o020, 0o040, 0o100, 0o200, 0o400)),
                         BitBoard(0o776, 0o775, 0o773, 0o767, 0o757, 0o737, 0o677, 0o577, 0))

    def test_get_attack_knight(self):
        self.assertEqual(Attack.get_attack(BLACK, KNIGHT, empty),
                         BitBoard(0, 0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(Attack.get_attack(WHITE, KNIGHT, empty),
                         BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, KNIGHT, full), empty)
        self.assertEqual(Attack.get_attack(WHITE, KNIGHT, full), empty)
        self.assertEqual(Attack.get_attack(BLACK, KNIGHT,
                                           BitBoard(0o001, 0o002, 0o004, 0o010, 0o020, 0o040, 0o100, 0o200, 0o400)),
                         BitBoard(0, 0, 0o773, 0o767, 0o757, 0o737, 0o677, 0o577, 0o377))
        self.assertEqual(Attack.get_attack(WHITE, KNIGHT,
                                           BitBoard(0o001, 0o002, 0o004, 0o010, 0o020, 0o040, 0o100, 0o200, 0o400)),
                         BitBoard(0o776, 0o775, 0o773, 0o767, 0o757, 0o737, 0o677, 0, 0))

    def test_get_attack_others(self):
        for ptype in [ROOK, BISHOP, SILVER, GOLD]:
            self.assertEqual(Attack.get_attack(BLACK, ptype, empty), full)
            self.assertEqual(Attack.get_attack(WHITE, ptype, empty), full)
            self.assertEqual(Attack.get_attack(BLACK, ptype, full), empty)
            self.assertEqual(Attack.get_attack(WHITE, ptype, full), empty)
            self.assertEqual(Attack.get_attack(BLACK, ptype,
                                               BitBoard(0o001, 0o002, 0o004, 0o010, 0o020, 0o040, 0o100, 0o200, 0o400)),
                             BitBoard(0o776, 0o0775, 0o773, 0o767, 0o757, 0o737, 0o677, 0o577, 0o377))
            self.assertEqual(Attack.get_attack(WHITE, ptype,
                                               BitBoard(0o001, 0o002, 0o004, 0o010, 0o020, 0o040, 0o100, 0o200, 0o400)),
                             BitBoard(0o776, 0o775, 0o773, 0o767, 0o757, 0o737, 0o677, 0o577, 0o377))
