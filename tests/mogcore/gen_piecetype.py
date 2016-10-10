from random import Random
from mogcore import PieceType

RANDOM_SEED = 12345


def gen_piecetype(n):
    rnd = Random(RANDOM_SEED)
    for num in range(n):
        x = rnd.choice([x for x in range(14)])
        yield PieceType(x)
