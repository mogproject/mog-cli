import unittest
from mogcore import Attack, BitBoard, BLACK, WHITE, ROOK
from .gen_bitboard import gen_bitboard, gen_index
from .util.bitboard_util import bitboards_from_string

full = BitBoard.FULL
empty = BitBoard.EMPTY


class TestAttackRangedRook(unittest.TestCase):
    ptype = 0

    def test_get_attack_rook(self):
        ss = [
            """
            oooooox*- ooooox*-* oooox*-*x ooox*-*xo oox*-*xoo
            --------* -------*- ------*-- -----*--- ----*----
            --------x -------x- ------x-- -----x--- ----x----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            """,
            """
            --------* -------*- ------*-- -----*--- ----*----
            oooooox*- ooooox*-* oooox*-*x ooox*-*xo oox*-*xoo
            --------* -------*- ------*-- -----*--- ----*----
            --------x -------x- ------x-- -----x--- ----x----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            """,
            """
            --------x -------x- ------x-- -----x--- ----x----
            --------* -------*- ------*-- -----*--- ----*----
            oooooox*- ooooox*-* oooox*-*x ooox*-*xo oox*-*xoo
            --------* -------*- ------*-- -----*--- ----*----
            --------x -------x- ------x-- -----x--- ----x----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            """,
            """
            --------o -------o- ------o-- -----o--- ----o----
            --------x -------x- ------x-- -----x--- ----x----
            --------* -------*- ------*-- -----*--- ----*----
            oooooox*- ooooox*-* oooox*-*x ooox*-*xo oox*-*xoo
            --------* -------*- ------*-- -----*--- ----*----
            --------x -------x- ------x-- -----x--- ----x----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            """,
            """
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            --------x -------x- ------x-- -----x--- ----x----
            --------* -------*- ------*-- -----*--- ----*----
            oooooox*- ooooox*-* oooox*-*x ooox*-*xo oox*-*xoo
            --------* -------*- ------*-- -----*--- ----*----
            --------x -------x- ------x-- -----x--- ----x----
            --------o -------o- ------o-- -----o--- ----o----
            --------o -------o- ------o-- -----o--- ----o----
            """,
        ]

        # make bitboards
        a = [bitboards_from_string(s) for s in ss]
        # mirror horizontal
        a = [ys + list([bb.flip_horizontal() for bb in xs] for xs in reversed(ys[0:4])) for ys in a]
        # mirror vertical
        a += list([[bb.flip_vertical() for bb in xs] for xs in ys] for ys in reversed(a[0:4]))

        for i in range(81):
            b = a[i // 9][i % 9]
            msg = 'i=%d' % i
            self.assertEqual(Attack.get_attack(BLACK, self.ptype, i, empty), b[2], msg)
            self.assertEqual(Attack.get_attack(BLACK, self.ptype, i, b[0] ^ b[1]), b[1], msg)
            self.assertEqual(Attack.get_attack(BLACK, self.ptype, i, full), b[0], msg)

    def test_get_attack_rook_prop_owner(self):
        # Owner doesn't care

        for bb, i in zip(gen_bitboard(100), gen_index(100)):
            msg = 'bb=%r, i=%d' % (bb, i)
            self.assertEqual(
                Attack.get_attack(BLACK, self.ptype, i, bb), Attack.get_attack(WHITE, self.ptype, i, bb), msg)

    def test_get_attack_rook_prop_symmetry(self):
        # Keep vertical and horizontal symmetric

        for bb, i in zip(gen_bitboard(100), gen_index(100)):
            # vertical symmetric
            j = (8 - i // 9) * 9 + i % 9
            msg = 'bb=%r, i=%d, j=%d' % (bb, i, j)

            a = Attack.get_attack(BLACK, self.ptype, i, bb)
            b = Attack.get_attack(BLACK, self.ptype, j, bb.flip_vertical())

            self.assertEqual(a, b.flip_vertical(), msg)

            # horizontal symmetric
            k = i // 9 * 9 + (8 - i % 9)
            msg = 'bb=%r, i=%d, k=%d' % (bb, i, k)

            a = Attack.get_attack(BLACK, self.ptype, i, bb)
            b = Attack.get_attack(BLACK, self.ptype, k, bb.flip_horizontal())

            self.assertEqual(a, b.flip_horizontal(), msg)

    def test_get_attack_prop_duel(self):
        # If a rook could attack another rook, it also can be attacked.

        for bb, i, j in zip(gen_bitboard(100), gen_index(100), gen_index(100)):
            msg = 'bb=%r, i=%d, j=%d' % (bb, i, j)
            self.assertEqual(
                Attack.get_attack(BLACK, self.ptype, i, bb).get(j),
                Attack.get_attack(WHITE, self.ptype, j, bb).get(i),
                msg)
