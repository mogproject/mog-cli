from random import Random
from mogcore import Turn

RANDOM_SEED = 12345


def gen_turn(n):
    rnd = Random(RANDOM_SEED)
    for num in range(n):
        yield Turn(rnd.randint(0, 1))
