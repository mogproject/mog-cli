import random
from mogcore.bitboard import BitBoard


def gen_bitboard(n):
    for num in range(n):
        if num == 0:
            yield BitBoard(0, 0)
        if num == 1:
            yield BitBoard(0o777777777777777777, 0o777777777)
        else:
            yield BitBoard(random.randint(0, 0o777777777777777777), random.randint(0, 0o777777777))


def gen_pawns(n):
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
                if random.randint(0, 1):
                    bb.set(f, random.randint(1, 9))
            yield bb


def gen_index(n):
    for num in range(n):
        if num == 0:
            yield 0
        if num == 1:
            yield 80
        else:
            yield random.randint(0, 80)
