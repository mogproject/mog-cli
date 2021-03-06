import unittest
from mogcore.bitboard import BitBoard
from mogcore import HAND
from .gen_bitboard import gen_bitboard, gen_pawns
from .gen_pos import gen_pos

empty = BitBoard.EMPTY
full = BitBoard.FULL


class TestBitBoard(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(BitBoard.wrap(empty)), '\n'.join(['-' * 9] * 9))
        self.assertEqual(str(BitBoard.wrap(full)), '\n'.join(['*' * 9] * 9))

    def test_repr(self):
        self.assertEqual(repr(BitBoard.wrap(empty)), 'BitBoard(000.000.000,000.000.000,000.000.000)')
        self.assertEqual(repr(BitBoard.wrap(full)), 'BitBoard(777.777.777,777.777.777,777.777.777)')

    def test_get(self):
        self.assertFalse(any(empty.get(i) for i in range(81)))
        self.assertTrue(all(full.get(i) for i in range(81)))

    def test_get_invalid_range(self):
        self.assertFalse(empty.get(-1))
        self.assertFalse(empty.get(81))
        self.assertFalse(empty.get(10000))
        self.assertFalse(full.get(-1))
        self.assertFalse(full.get(81))
        self.assertFalse(full.get(10000))

    def test_set(self):
        self.assertEqual(empty.set(0), BitBoard(1, 0))
        self.assertEqual(empty.set(80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0o400))
        self.assertEqual(empty.set(52), BitBoard(0, 0, 0, 0, 0, 0o200, 0, 0, 0))
        self.assertEqual(empty.set(53), BitBoard(0, 0, 0, 0, 0, 0o400, 0, 0, 0))
        self.assertEqual(empty.set(54), BitBoard(0, 0, 0, 0, 0, 0, 0o001, 0, 0))
        self.assertEqual(empty.set(55), BitBoard(0, 0, 0, 0, 0, 0, 0o002, 0, 0))
        self.assertEqual(full.set(0), full)
        self.assertEqual(full.set(80), full)

    def test_set_invalid_range(self):
        self.assertEqual(empty.set(-1), empty)
        self.assertEqual(empty.set(81), empty)
        self.assertEqual(empty.set(10000), empty)
        self.assertEqual(full.set(-1), full)
        self.assertEqual(full.set(81), full)
        self.assertEqual(full.set(10000), full)

    def test_reset(self):
        self.assertEqual(empty.reset(0), empty)
        self.assertEqual(empty.reset(0), empty)
        self.assertEqual(full.reset(0), BitBoard(0o776, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.reset(80), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o377))

    def test_reset_invalid_range(self):
        self.assertEqual(empty.set(-1), empty)
        self.assertEqual(empty.set(81), empty)
        self.assertEqual(empty.set(10000), empty)
        self.assertEqual(full.set(-1), full)
        self.assertEqual(full.set(81), full)
        self.assertEqual(full.set(10000), full)

    def test_not(self):
        self.assertEqual(~empty, full)
        self.assertEqual(~full, empty)

    def test_not_prop(self):
        for bb in gen_bitboard(100):
            self.assertEqual(~~bb, bb)

    def test_and_prop(self):
        for bb in gen_bitboard(100):
            self.assertEqual(bb & bb, bb)
            self.assertEqual(bb & empty, empty)
            self.assertEqual(bb & full, bb)

    def test_or_prop(self):
        for bb in gen_bitboard(100):
            self.assertEqual(bb | bb, bb)
            self.assertEqual(bb | empty, bb)
            self.assertEqual(bb | full, full)

    def test_xor_prop(self):
        for bb in gen_bitboard(100):
            self.assertEqual(bb ^ bb, empty)
            self.assertEqual(bb ^ empty, bb)
            self.assertEqual(bb ^ full, ~bb)

    def test_shift_left(self):
        self.assertEqual(empty.shift_left(-2), empty)
        self.assertEqual(empty.shift_left(0), empty)
        self.assertEqual(empty.shift_left(2), empty)
        self.assertEqual(empty.shift_left(9), empty)
        self.assertEqual(empty.shift_left(64), empty)

        self.assertEqual(full.shift_left(9), empty)
        self.assertEqual(full.shift_left(8), BitBoard(0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0o400))
        self.assertEqual(full.shift_left(7), BitBoard(0o600, 0o600, 0o600, 0o600, 0o600, 0o600, 0o600, 0o600, 0o600))
        self.assertEqual(full.shift_left(6), BitBoard(0o700, 0o700, 0o700, 0o700, 0o700, 0o700, 0o700, 0o700, 0o700))
        self.assertEqual(full.shift_left(5), BitBoard(0o740, 0o740, 0o740, 0o740, 0o740, 0o740, 0o740, 0o740, 0o740))
        self.assertEqual(full.shift_left(4), BitBoard(0o760, 0o760, 0o760, 0o760, 0o760, 0o760, 0o760, 0o760, 0o760))
        self.assertEqual(full.shift_left(3), BitBoard(0o770, 0o770, 0o770, 0o770, 0o770, 0o770, 0o770, 0o770, 0o770))
        self.assertEqual(full.shift_left(2), BitBoard(0o774, 0o774, 0o774, 0o774, 0o774, 0o774, 0o774, 0o774, 0o774))
        self.assertEqual(full.shift_left(1), BitBoard(0o776, 0o776, 0o776, 0o776, 0o776, 0o776, 0o776, 0o776, 0o776))
        self.assertEqual(full.shift_left(0), full)
        self.assertEqual(full.shift_left(-1), BitBoard(0o377, 0o377, 0o377, 0o377, 0o377, 0o377, 0o377, 0o377, 0o377))
        self.assertEqual(full.shift_left(-2), BitBoard(0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177))
        self.assertEqual(full.shift_left(-3), BitBoard(0o077, 0o077, 0o077, 0o077, 0o077, 0o077, 0o077, 0o077, 0o077))
        self.assertEqual(full.shift_left(-4), BitBoard(0o037, 0o037, 0o037, 0o037, 0o037, 0o037, 0o037, 0o037, 0o037))
        self.assertEqual(full.shift_left(-5), BitBoard(0o017, 0o017, 0o017, 0o017, 0o017, 0o017, 0o017, 0o017, 0o017))
        self.assertEqual(full.shift_left(-6), BitBoard(0o007, 0o007, 0o007, 0o007, 0o007, 0o007, 0o007, 0o007, 0o007))
        self.assertEqual(full.shift_left(-7), BitBoard(0o003, 0o003, 0o003, 0o003, 0o003, 0o003, 0o003, 0o003, 0o003))
        self.assertEqual(full.shift_left(-8), BitBoard(0o001, 0o001, 0o001, 0o001, 0o001, 0o001, 0o001, 0o001, 0o001))
        self.assertEqual(full.shift_left(-9), empty)
        self.assertEqual(full.shift_left(64), empty)
        self.assertEqual(full.shift_left(-2147483648), empty)
        self.assertEqual(full.shift_left(2147483647), empty)

    def test_shift_left_prop(self):
        for bb in gen_bitboard(100):
            self.assertEqual(bb.shift_left(-9), empty)
            self.assertEqual(bb.shift_left(9), empty)
            self.assertEqual(bb.shift_left(3) & BitBoard(0o007007007007007007, 0o007007007), empty)

    def test_shift_right(self):
        self.assertEqual(empty.shift_right(-2), empty)
        self.assertEqual(empty.shift_right(0), empty)
        self.assertEqual(empty.shift_right(2), empty)
        self.assertEqual(empty.shift_right(9), empty)
        self.assertEqual(empty.shift_right(64), empty)

        self.assertEqual(full.shift_right(-9), empty)
        self.assertEqual(full.shift_right(-8), BitBoard(0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0o400, 0o400))
        self.assertEqual(full.shift_right(-7), BitBoard(0o600, 0o600, 0o600, 0o600, 0o600, 0o600, 0o600, 0o600, 0o600))
        self.assertEqual(full.shift_right(-6), BitBoard(0o700, 0o700, 0o700, 0o700, 0o700, 0o700, 0o700, 0o700, 0o700))
        self.assertEqual(full.shift_right(-5), BitBoard(0o740, 0o740, 0o740, 0o740, 0o740, 0o740, 0o740, 0o740, 0o740))
        self.assertEqual(full.shift_right(-4), BitBoard(0o760, 0o760, 0o760, 0o760, 0o760, 0o760, 0o760, 0o760, 0o760))
        self.assertEqual(full.shift_right(-3), BitBoard(0o770, 0o770, 0o770, 0o770, 0o770, 0o770, 0o770, 0o770, 0o770))
        self.assertEqual(full.shift_right(-2), BitBoard(0o774, 0o774, 0o774, 0o774, 0o774, 0o774, 0o774, 0o774, 0o774))
        self.assertEqual(full.shift_right(-1), BitBoard(0o776, 0o776, 0o776, 0o776, 0o776, 0o776, 0o776, 0o776, 0o776))
        self.assertEqual(full.shift_right(0), full)
        self.assertEqual(full.shift_right(1), BitBoard(0o377, 0o377, 0o377, 0o377, 0o377, 0o377, 0o377, 0o377, 0o377))
        self.assertEqual(full.shift_right(2), BitBoard(0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177))
        self.assertEqual(full.shift_right(3), BitBoard(0o077, 0o077, 0o077, 0o077, 0o077, 0o077, 0o077, 0o077, 0o077))
        self.assertEqual(full.shift_right(4), BitBoard(0o037, 0o037, 0o037, 0o037, 0o037, 0o037, 0o037, 0o037, 0o037))
        self.assertEqual(full.shift_right(5), BitBoard(0o017, 0o017, 0o017, 0o017, 0o017, 0o017, 0o017, 0o017, 0o017))
        self.assertEqual(full.shift_right(6), BitBoard(0o007, 0o007, 0o007, 0o007, 0o007, 0o007, 0o007, 0o007, 0o007))
        self.assertEqual(full.shift_right(7), BitBoard(0o003, 0o003, 0o003, 0o003, 0o003, 0o003, 0o003, 0o003, 0o003))
        self.assertEqual(full.shift_right(8), BitBoard(0o001, 0o001, 0o001, 0o001, 0o001, 0o001, 0o001, 0o001, 0o001))
        self.assertEqual(full.shift_right(9), empty)
        self.assertEqual(full.shift_right(64), empty)
        self.assertEqual(full.shift_right(-2147483648), empty)
        self.assertEqual(full.shift_right(2147483647), empty)

    def test_shift_left_right(self):
        for bb in gen_bitboard(100):
            self.assertEqual(bb.shift_right(-9), empty)
            self.assertEqual(bb.shift_right(9), empty)
            self.assertEqual(bb.shift_right(3) & BitBoard(0o700700700700700700, 0o700700700), empty)

    def test_shift_down(self):
        self.assertEqual(empty.shift_down(-2), empty)
        self.assertEqual(empty.shift_down(0), empty)
        self.assertEqual(empty.shift_down(2), empty)
        self.assertEqual(empty.shift_down(9), empty)
        self.assertEqual(empty.shift_down(64), empty)

        self.assertEqual(full.shift_down(9), empty)
        self.assertEqual(full.shift_down(8), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0o777))
        self.assertEqual(full.shift_down(7), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o777, 0o777))
        self.assertEqual(full.shift_down(6), BitBoard(0, 0, 0, 0, 0, 0, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_down(5), BitBoard(0, 0, 0, 0, 0, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_down(4), BitBoard(0, 0, 0, 0, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_down(3), BitBoard(0, 0, 0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_down(2), BitBoard(0, 0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_down(1), BitBoard(0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_down(0), full)
        self.assertEqual(full.shift_down(-1), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0))
        self.assertEqual(full.shift_down(-2), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0, 0))
        self.assertEqual(full.shift_down(-3), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0, 0, 0))
        self.assertEqual(full.shift_down(-4), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0, 0, 0, 0))
        self.assertEqual(full.shift_down(-5), BitBoard(0o777, 0o777, 0o777, 0o777, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_down(-6), BitBoard(0o777, 0o777, 0o777, 0, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_down(-7), BitBoard(0o777, 0o777, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_down(-8), BitBoard(0o777, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_down(-9), empty)
        self.assertEqual(full.shift_down(64), empty)
        self.assertEqual(full.shift_down(-2147483648), empty)
        self.assertEqual(full.shift_down(2147483647), empty)

    def test_shift_down_prop(self):
        for bb in gen_bitboard(100):
            self.assertEqual(bb.shift_down(-9), empty)
            self.assertEqual(bb.shift_down(9), empty)
            self.assertEqual(bb.shift_down(3) & BitBoard(0o777, 0), empty)

    def test_shift_up(self):
        self.assertEqual(empty.shift_up(-2), empty)
        self.assertEqual(empty.shift_up(0), empty)
        self.assertEqual(empty.shift_up(2), empty)
        self.assertEqual(empty.shift_up(9), empty)
        self.assertEqual(empty.shift_up(64), empty)

        self.assertEqual(full.shift_up(-9), empty)
        self.assertEqual(full.shift_up(-8), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0o777))
        self.assertEqual(full.shift_up(-7), BitBoard(0, 0, 0, 0, 0, 0, 0, 0o777, 0o777))
        self.assertEqual(full.shift_up(-6), BitBoard(0, 0, 0, 0, 0, 0, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_up(-5), BitBoard(0, 0, 0, 0, 0, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_up(-4), BitBoard(0, 0, 0, 0, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_up(-3), BitBoard(0, 0, 0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_up(-2), BitBoard(0, 0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_up(-1), BitBoard(0, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777))
        self.assertEqual(full.shift_up(0), full)
        self.assertEqual(full.shift_up(1), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0))
        self.assertEqual(full.shift_up(2), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0, 0))
        self.assertEqual(full.shift_up(3), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0, 0, 0))
        self.assertEqual(full.shift_up(4), BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0, 0, 0, 0))
        self.assertEqual(full.shift_up(5), BitBoard(0o777, 0o777, 0o777, 0o777, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_up(6), BitBoard(0o777, 0o777, 0o777, 0, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_up(7), BitBoard(0o777, 0o777, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_up(8), BitBoard(0o777, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(full.shift_up(9), empty)
        self.assertEqual(full.shift_up(64), empty)
        self.assertEqual(full.shift_up(-2147483648), empty)
        self.assertEqual(full.shift_up(2147483647), empty)

    def test_shift_up_prop(self):
        for bb in gen_bitboard(100):
            self.assertEqual(bb.shift_up(-9), empty)
            self.assertEqual(bb.shift_up(9), empty)
            self.assertEqual(bb.shift_up(3) & BitBoard(0, 0o777), empty)

    def test_count(self):
        self.assertEqual(empty.count(), 0)
        self.assertEqual(full.count(), 81)
        self.assertEqual(BitBoard(1, 0, 0, 0, 0, 0, 0, 0, 0).count(), 1)
        self.assertEqual(BitBoard(1, 0, 0, 0, 0, 0, 0, 0, 0o400).count(), 2)
        self.assertEqual(BitBoard(1, 0, 0, 0, 0o777, 0, 0, 0, 0o400).count(), 11)

    def test_to_list(self):
        self.assertEqual(empty.to_list(), [])
        self.assertEqual(full.to_list(), [x for x in range(81)])
        self.assertEqual(BitBoard(1, 0, 0, 0, 0, 0, 0, 0, 0).to_list(), [0])
        self.assertEqual(BitBoard(1, 0, 0, 0, 0, 0, 0, 0, 0o400).to_list(), [0, 80])
        self.assertEqual(BitBoard(1, 0, 0, 0, 0o777, 0, 0, 0, 0o400).to_list(), [
            0, 36, 37, 38, 39, 40, 41, 42, 43, 44, 80
        ])

    def test_count_prop(self):
        for a in gen_bitboard(50):
            for bb in gen_bitboard(50):
                b = bb & (~a)
                self.assertEqual(a.count() + b.count(), (a | b).count())

    def test_flip_vertical(self):
        self.assertEqual(empty.flip_vertical(), empty)
        self.assertEqual(full.flip_vertical(), full)

        self.assertEqual(BitBoard(1, 0, 0, 0, 0, 0, 0, 0, 0).flip_vertical(), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 1))

    def test_flip_vertical_prop(self):
        for bb in gen_bitboard(100):
            self.assertEqual(bb.flip_vertical().flip_vertical(), bb)

    def test_flip_horizontal(self):
        self.assertEqual(empty.flip_horizontal(), empty)
        self.assertEqual(full.flip_horizontal(), full)

        self.assertEqual(BitBoard(1, 0, 0, 0, 0, 0, 0, 0, 0).flip_horizontal(), BitBoard(0o400, 0, 0, 0, 0, 0, 0, 0, 0))

    def test_flip_horizontal_prop(self):
        for bb in gen_bitboard(100):
            self.assertEqual(bb.flip_horizontal().flip_horizontal(), bb)

    def test_spread_all_file(self):
        self.assertEqual(empty.spread_all_file(), empty)

        self.assertEqual(BitBoard(1, 0, 0, 0, 0, 0, 0, 0, 0).spread_all_file(), BitBoard(1, 1, 1, 1, 1, 1, 1, 1, 1))
        self.assertEqual(BitBoard(1, 2, 4, 0o10, 0o20, 0o40, 0o100, 0o200, 0o400).spread_all_file(), full)

    def test_spread_all_file_prop(self):
        for bb in gen_pawns(100):
            self.assertEqual(bb.spread_all_file() & bb, bb)

    def test_ident(self):
        self.assertEqual(BitBoard.ident(0), BitBoard(0o001, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(BitBoard.ident(40), BitBoard(0, 0, 0, 0, 0o020, 0, 0, 0, 0))
        self.assertEqual(BitBoard.ident(80), BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0o400))
        self.assertEqual(BitBoard.ident(81), BitBoard())

    def test_ident_prop(self):
        for pos in gen_pos(100):
            if pos == HAND:
                self.assertEqual(BitBoard.ident(pos.value), BitBoard(), 'pos=%r' % pos)
            else:
                self.assertEqual(BitBoard.ident(pos.value).count(), 1, 'pos=%r' % pos)
                self.assertEqual(BitBoard.ident(pos.value).get(pos.value), True, 'pos=%r' % pos)
