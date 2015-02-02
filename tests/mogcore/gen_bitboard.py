from random import Random
from mogcore.bitboard import BitBoard

RANDOM_SEED = 12345


def gen_bitboard(n):
    rnd = Random(RANDOM_SEED)
    for num in range(n):
        if num == 0:
            yield BitBoard(0, 0)
        if num == 1:
            yield BitBoard(0o777777777777777777, 0o777777777)
        else:
            yield BitBoard(rnd.randint(0, 0o777777777777777777), rnd.randint(0, 0o777777777))


def gen_pawns(n):
    rnd = Random(RANDOM_SEED)
    for num in range(n):
        if num == 0:
            yield BitBoard(0, 0)
        if num == 1:
            yield BitBoard(0o777, 0, 0, 0, 0, 0, 0, 0, 0)
        if num == 2:
            yield BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0o777)
        else:
            bb = BitBoard()
            for f in range(9):
                if rnd.randint(0, 1):
                    bb.set(f, rnd.randint(1, 9))
            yield bb


def gen_index(n):
    rnd = Random(RANDOM_SEED)
    for num in range(n):
        if num == 0:
            yield 0
        if num == 1:
            yield 80
        else:
            yield rnd.randint(0, 80)
