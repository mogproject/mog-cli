from random import Random
from mogcore import PieceType

RANDOM_SEED = 12345


def gen_piecetype(n):
    rnd = Random(RANDOM_SEED)
    for num in range(n):
        yield PieceType(rnd.randint(0, 13))
