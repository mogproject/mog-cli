import unittest
from cmogcore import Attack, BitBoard
from mogcore.bitboard import full, empty


class TestAttackAerial(unittest.TestCase):
    def test_get_attack_invalid(self):
        for owner in range(2):
            for ptype in [0] + list(range(8, 16)):
                for occ in [full, empty]:
                    self.assertEqual(Attack.get_attack(owner, ptype, occ), empty)

    def test_get_attack_pawn(self):
        self.assertEqual(Attack.get_attack(0, empty, empty),
                         BitBoard(0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(Attack.get_attack(1, empty, empty),
                         BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0))
        self.assertEqual(Attack.get_attack(0, empty, BitBoard(0, 0, 0, 0, 0o777, 0, 0, 0, 0)), empty)
        self.assertEqual(Attack.get_attack(0, full, BitBoard(0, 0, 0, 0, 0o777, 0, 0, 0, 0)), empty)
        self.assertEqual(Attack.get_attack(1, empty, BitBoard(0, 0, 0, 0, 0o777, 0, 0, 0, 0)), empty)
        self.assertEqual(Attack.get_attack(1, full, BitBoard(0, 0, 0, 0, 0o777, 0, 0, 0, 0)), empty)
        self.assertEqual(Attack.get_attack(1, BitBoard(0, 0o777, 0, 0, 0, 0, 0, 0o777, 0),
                                           BitBoard(0, 0o555, 0, 0, 0, 0, 0, 0o111, 0)),
                         BitBoard(0o222, 0, 0o222, 0o222, 0o222, 0o222, 0o222, 0, 0))

    def test_get_attack_lance(self):
        self.assertEqual(Attack.get_attack(0, 3, empty),
                         BitBoard(0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(Attack.get_attack(1, 3, empty),
                         BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0))
        self.assertEqual(Attack.get_attack(0, 3, full), empty)
        self.assertEqual(Attack.get_attack(1, 3, full), empty)
        self.assertEqual(Attack.get_attack(0, 3,
                                           BitBoard(0o001, 0o002, 0o004, 0o010, 0o020, 0o040, 0o100, 0o200, 0o400)),
                         BitBoard(0, 0o775, 0o773, 0o767, 0o757, 0o737, 0o677, 0o577, 0o377))
        self.assertEqual(Attack.get_attack(1, 3,
                                           BitBoard(0o001, 0o002, 0o004, 0o010, 0o020, 0o040, 0o100, 0o200, 0o400)),
                         BitBoard(0o776, 0o775, 0o773, 0o767, 0o757, 0o737, 0o677, 0o577, 0))

    def test_get_attack_knight(self):
        self.assertEqual(Attack.get_attack(0, 6, empty),
                         BitBoard(0, 0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(Attack.get_attack(1, 6, empty),
                         BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0, 0))
        self.assertEqual(Attack.get_attack(0, 6, full), empty)
        self.assertEqual(Attack.get_attack(1, 6, full), empty)
        self.assertEqual(Attack.get_attack(0, 6,
                                           BitBoard(0o001, 0o002, 0o004, 0o010, 0o020, 0o040, 0o100, 0o200, 0o400)),
                         BitBoard(0, 0, 0o773, 0o767, 0o757, 0o737, 0o677, 0o577, 0o377))
        self.assertEqual(Attack.get_attack(1, 6,
                                           BitBoard(0o001, 0o002, 0o004, 0o010, 0o020, 0o040, 0o100, 0o200, 0o400)),
                         BitBoard(0o776, 0o775, 0o773, 0o767, 0o757, 0o737, 0o677, 0, 0))

    def test_get_attack_others(self):
        for ptype in [1, 2, 4, 5]:
            self.assertEqual(Attack.get_attack(0, ptype, empty), full)
            self.assertEqual(Attack.get_attack(1, ptype, empty), full)
            self.assertEqual(Attack.get_attack(0, ptype, full), empty)
            self.assertEqual(Attack.get_attack(1, ptype, full), empty)
            self.assertEqual(Attack.get_attack(0, ptype,
                                               BitBoard(0o001, 0o002, 0o004, 0o010, 0o020, 0o040, 0o100, 0o200, 0o400)),
                             BitBoard(0o776, 0o0775, 0o773, 0o767, 0o757, 0o737, 0o677, 0o577, 0o377))
            self.assertEqual(Attack.get_attack(1, ptype,
                                               BitBoard(0o001, 0o002, 0o004, 0o010, 0o020, 0o040, 0o100, 0o200, 0o400)),
                             BitBoard(0o776, 0o775, 0o773, 0o767, 0o757, 0o737, 0o677, 0o577, 0o377))
