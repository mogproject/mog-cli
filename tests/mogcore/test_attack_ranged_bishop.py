import unittest
from cmogcore import Attack, BitBoard
from mogcore.bitboard import full, empty
from .gen_bitboard import gen_bitboard, gen_index
from .util.bitboard_util import bitboards_from_string


class TestAttackRangedLance(unittest.TestCase):
    def test_get_attack_bishop(self):
        ss = [
            """
            --------- --------- --------- --------- ---------
            -------*- ------*-* -----*-*- ----*-*-- ---*-*---
            ------x-- -----x--- ----x---x ---x---x- --x---x--
            -----o--- ----o---- ---o----- --o-----o -o-----o-
            ----o---- ---o----- --o------ -o------- o-------o
            ---o----- --o------ -o------- o-------- ---------
            --o------ -o------- o-------- --------- ---------
            -o------- o-------- --------- --------- ---------
            o-------- --------- --------- --------- ---------
            """,
            """
            -------*- ------*-* -----*-*- ----*-*-- ---*-*---
            --------- --------- --------- --------- ---------
            -------*- ------*-* -----*-*- ----*-*-- ---*-*---
            ------x-- -----x--- ----x---x ---x---x- --x---x--
            -----o--- ----o---- ---o----- --o-----o -o-----o-
            ----o---- ---o----- --o------ -o------- o-------o
            ---o----- --o------ -o------- o-------- ---------
            --o------ -o------- o-------- --------- ---------
            -o------- o-------- --------- --------- ---------
            """,
            """
            ------x-- -----x--- ----x---x ---x---x- --x---x--
            -------*- ------*-* -----*-*- ----*-*-- ---*-*---
            --------- --------- --------- --------- ---------
            -------*- ------*-* -----*-*- ----*-*-- ---*-*---
            ------x-- -----x--- ----x---x ---x---x- --x---x--
            -----o--- ----o---- ---o----- --o-----o -o-----o-
            ----o---- ---o----- --o------ -o------- o-------o
            ---o----- --o------ -o------- o-------- ---------
            --o------ -o------- o-------- --------- ---------
            """,
            """
            -----o--- ----o---- ---o----- --o-----o -o-----o-
            ------x-- -----x--- ----x---x ---x---x- --x---x--
            -------*- ------*-* -----*-*- ----*-*-- ---*-*---
            --------- --------- --------- --------- ---------
            -------*- ------*-* -----*-*- ----*-*-- ---*-*---
            ------x-- -----x--- ----x---x ---x---x- --x---x--
            -----o--- ----o---- ---o----- --o-----o -o-----o-
            ----o---- ---o----- --o------ -o------- o-------o
            ---o----- --o------ -o------- o-------- ---------
            """,
            """
            ----o---- ---o----- --o------ -o------- o-------o
            -----o--- ----o---- ---o----- --o-----o -o-----o-
            ------x-- -----x--- ----x---x ---x---x- --x---x--
            -------*- ------*-* -----*-*- ----*-*-- ---*-*---
            --------- --------- --------- --------- ---------
            -------*- ------*-* -----*-*- ----*-*-- ---*-*---
            ------x-- -----x--- ----x---x ---x---x- --x---x--
            -----o--- ----o---- ---o----- --o-----o -o-----o-
            ----o---- ---o----- --o------ -o------- o-------o
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
            self.assertEqual(Attack.get_attack(0, 2, i, empty), b[2], msg)
            self.assertEqual(Attack.get_attack(0, 2, i, b[0] ^ b[1]), b[1], msg)
            self.assertEqual(Attack.get_attack(0, 2, i, full), b[0], msg)

    def test_get_attack_bishop_prop_owner(self):
        """Owner doesn't care"""

        for bb in gen_bitboard(100):
            for i in gen_index(100):
                msg = 'bb=%r, i=%d' % (bb, i)
                self.assertEqual(Attack.get_attack(0, 2, i, bb), Attack.get_attack(1, 2, i, bb), msg)

    def test_get_attack_bishop_prop_symmetry(self):
        """Keep vertical and horizontal symmetric"""

        for bb in gen_bitboard(100):
            for i in gen_index(100):
                # vertical symmetric
                j = (8 - i // 9) * 9 + i % 9
                msg = 'bb=%r, i=%d, j=%d' % (bb, i, j)

                a = Attack.get_attack(0, 2, i, bb)
                b = Attack.get_attack(0, 2, j, bb.flip_vertical())

                self.assertEqual(a, b.flip_vertical(), msg)

                # horizontal symmetric
                k = i // 9 * 9 + (8 - i % 9)
                msg = 'bb=%r, i=%d, k=%d' % (bb, i, k)

                a = Attack.get_attack(0, 2, i, bb)
                b = Attack.get_attack(0, 2, k, bb.flip_horizontal())

                self.assertEqual(a, b.flip_horizontal(), msg)

    def test_get_attack_bishop_prop_neighbor(self):
        """neighbors' attack never intersect"""

        for bb in gen_bitboard(100):
            for i in gen_index(100):
                j = i - 1 if i % 9 == 8 else i + 1
                msg = 'bb=%r, i=%d, j=%d' % (bb, i, j)

                a = Attack.get_attack(0, 2, i, bb)
                b = Attack.get_attack(0, 2, j, bb)

                self.assertEqual(a & b, empty, msg)
