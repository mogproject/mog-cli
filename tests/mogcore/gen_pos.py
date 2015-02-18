from random import Random
from mogcore import Pos, HAND

RANDOM_SEED = 12345


def gen_pos(n):
    rnd = Random(RANDOM_SEED)
    for num in range(n):
        if num == 0:
            yield HAND
        elif num == 1:
            yield Pos(0)
        elif num == 2:
            yield Pos(80)
        else:
            yield Pos(rnd.randint(0, 81))
