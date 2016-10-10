import unittest
from mogcore import Attack, BitBoard, BLACK, WHITE, LANCE
from .gen_bitboard import gen_bitboard, gen_index

full = BitBoard.FULL
empty = BitBoard.EMPTY


class TestAttackRangedLance(unittest.TestCase):
    ptype = LANCE

    def test_get_attack_lance_black(self):
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 0, empty), empty)
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 40, empty),
                         BitBoard(0o020, 0o020, 0o020, 0o020, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 53, empty),
                         BitBoard(0o400, 0o400, 0o400, 0o400, 0o400, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 54, empty),
                         BitBoard(0o001, 0o001, 0o001, 0o001, 0o001, 0o001, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 80, empty),
                         BitBoard(0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 0, full), empty)
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 18, empty), BitBoard(0o001, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 18, BitBoard(0o001, 0, 0, 0, 0, 0, 0, 0, 0)),
                         BitBoard(0o001, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 18, BitBoard(0, 0o001, 0, 0, 0, 0, 0, 0, 0)),
                         BitBoard(0o000, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 18, BitBoard(0o001, 0o001, 0, 0, 0, 0, 0, 0, 0)),
                         BitBoard(0o000, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 40, full), BitBoard(0, 0, 0, 0o020, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 8, full), empty)
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 17, full), BitBoard(0o400, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 26, full), BitBoard(0, 0o400, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 35, full), BitBoard(0, 0, 0o400, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 44, full), BitBoard(0, 0, 0, 0o400, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 53, full), BitBoard(0, 0, 0, 0, 0o400, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 62, full), BitBoard(0, 0, 0, 0, 0, 0o400, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 71, full), BitBoard(0, 0, 0, 0, 0, 0, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 54, full), BitBoard(0, 0, 0, 0, 0, 0o001, 0, 0, 0))
        self.assertEqual(Attack.get_attack(BLACK, self.ptype, 80, full), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0))

    def test_get_attack_lance_black_prop(self):
        for bb in gen_bitboard(100):
            for i in gen_index(100):
                atk = BitBoard.wrap(Attack.get_attack(BLACK, self.ptype, i, bb))

                # should be same file
                self.assertTrue(all(x % 9 == i % 9 for x in atk.indices()), 'bb=%r, i=%s' % (bb, i))

                # should be upper rank
                self.assertTrue(all(x / 9 < i / 9 for x in atk.indices()), 'bb=%r, i=%s' % (bb, i))

                # horizontal symmetric
                j = i // 9 * 9 + (8 - i % 9)
                self.assertEqual(
                    atk, Attack.get_attack(BLACK, self.ptype, j, bb.flip_horizontal()).flip_horizontal(),
                    'bb=%r, i=%d, j=%d' % (bb, i, j))

        for i in gen_index(100):
            expected_count = 0 if i < 9 else 1
            self.assertEqual(Attack.get_attack(BLACK, self.ptype, i, full).count(), expected_count, 'i=%s' % i)

    def test_get_attack_lance_white(self):
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 0, empty),
                         BitBoard(0, 0o001, 0o001, 0o001, 0o001, 0o001, 0o001, 0o001, 0o001))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 40, empty),
                         BitBoard(0, 0, 0, 0, 0, 0o020, 0o020, 0o020, 0o020))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 53, empty),
                         BitBoard(0, 0, 0, 0, 0, 0, 0o400, 0o400, 0o400))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 54, empty), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o001, 0o001))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 80, empty), empty)
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 0, full), BitBoard(0, 0o001, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 54, BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0o001)),
                         BitBoard(0, 0, 0, 0, 0, 0, 0, 0o001, 0o001))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 54, BitBoard(0, 0, 0, 0, 0, 0, 0, 0o001, 0)),
                         BitBoard(0, 0, 0, 0, 0, 0, 0, 0o001, 0))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 54, BitBoard(0, 0, 0, 0, 0, 0, 0, 0o001, 0o001)),
                         BitBoard(0, 0, 0, 0, 0, 0, 0, 0o001, 0))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 40, full), BitBoard(0, 0, 0, 0, 0, 0o020, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 8, full), BitBoard(0, 0o400, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 17, full), BitBoard(0, 0, 0o400, 0, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 26, full), BitBoard(0, 0, 0, 0o400, 0, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 35, full), BitBoard(0, 0, 0, 0, 0o400, 0, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 44, full), BitBoard(0, 0, 0, 0, 0, 0o400, 0, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 53, full), BitBoard(0, 0, 0, 0, 0, 0, 0o400, 0, 0))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 62, full), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o400, 0))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 71, full), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0o400))
        self.assertEqual(Attack.get_attack(WHITE, self.ptype, 80, full), empty)

    def test_get_attack_lance_white_prop(self):
        for bb, i in zip(gen_bitboard(100), gen_index(100)):
            atk = BitBoard.wrap(Attack.get_attack(WHITE, self.ptype, i, bb))

            # should be same file
            self.assertTrue(all(x % 9 == i % 9 for x in atk.indices()), 'bb=%r, i=%s' % (bb, i))

            # should be lower rank
            self.assertTrue(all(x / 9 > i / 9 for x in atk.indices()), 'bb=%r, i=%s' % (bb, i))

            # horizontal symmetric
            j = i // 9 * 9 + (8 - i % 9)
            self.assertEqual(
                atk, Attack.get_attack(WHITE, self.ptype, j, bb.flip_horizontal()).flip_horizontal(),
                'bb=%r, i=%d, j=%d' % (bb, i, j))

        for i in gen_index(100):
            expected_count = 0 if 72 <= i else 1
            self.assertEqual(Attack.get_attack(WHITE, self.ptype, i, full).count(), expected_count, 'i=%s' % i)

    def test_get_attack_lance_prop(self):
        for bb, i in zip(gen_bitboard(100), gen_index(100)):
            # vertical symmetric
            j = (8 - i // 9) * 9 + i % 9
            a = Attack.get_attack(BLACK, self.ptype, i, bb)
            b = Attack.get_attack(WHITE, self.ptype, j, bb.flip_vertical())
            self.assertEqual(a, b.flip_vertical(), 'bb=%r, i=%d, j=%d' % (bb, i, j))

            # black never intersect over white and vice versa
            self.assertEqual(
                Attack.get_attack(BLACK, self.ptype, i, bb) & Attack.get_attack(WHITE, self.ptype, i, bb), empty)

    def test_get_attack_prop_duel(self):
        # If a lance could attack another lance, it also can be attacked.

        for bb, i, j in zip(gen_bitboard(100), gen_index(100), gen_index(100)):
            msg = 'bb=%r, i=%d, j=%d' % (bb, i, j)
            self.assertEqual(
                Attack.get_attack(BLACK, self.ptype, i, bb).get(j),
                Attack.get_attack(WHITE, self.ptype, j, bb).get(i),
                msg)
