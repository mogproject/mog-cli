from random import Random
from mogcore import *

RANDOM_SEED = 12345


def gen_state(n):
    rnd = Random(RANDOM_SEED)

    for num in range(n):
        if num == 0:
            yield State()
        if num == 1:
            yield STATE_HIRATE
        if num == 2:
            yield STATE_TSUME_BLACK
        else:
            s = State()

            s.set_turn(rnd.randint(0, 1))

            for i in range(40):
                if rnd.random() < 0.004:  # randomely set unused
                    continue

                pt = PieceType(s.get_raw_piece_type(i))

                if pt == KING:
                    owner = Turn(i & 1)
                else:
                    owner = Turn(rnd.randint(0, 1))

                if pt != KING and rnd.random() < 0.2:  # randomly in hand
                    ps = HAND
                else:
                    if rnd.random() < 0.2:  # randomly promote
                        pt = pt.promoted()
                    used = s.board
                    if pt == PAWN or pt == LANCE:
                        used |= BitBoard.rank1.flip_by_turn(owner.value)
                    if pt == KNIGHT:
                        used |= (BitBoard.rank1 | BitBoard.rank2).flip_by_turn(owner.value)
                    ps = Pos(rnd.choice((~used).to_list()))

                s.set_piece(owner.value, pt.value, ps.value)

            yield s


STR_HIRATE = '\n'.join([
    'PI',
    '+'
])

STR_TSUME_BLACK = '\n'.join([
    'P1 *  *  *  * -OU *  *  *  * ',
    'P2 *  *  *  *  *  *  *  *  * ',
    'P3 *  *  *  *  *  *  *  *  * ',
    'P4 *  *  *  *  *  *  *  *  * ',
    'P5 *  *  *  *  *  *  *  *  * ',
    'P6 *  *  *  *  *  *  *  *  * ',
    'P7 *  *  *  *  *  *  *  *  * ',
    'P8 *  *  *  *  *  *  *  *  * ',
    'P9 *  *  *  *  *  *  *  *  * ',
    'P+00HI00HI00KA00KA00KI00KI00KI00KI00GI00GI00GI00GI00KE00KE00KE00KE00KY00KY00KY00KY'
    '00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU',
    'P-',
    '+'
])

STR_TSUME_WHITE = '\n'.join([
    'P1 *  *  *  *  *  *  *  *  * ',
    'P2 *  *  *  *  *  *  *  *  * ',
    'P3 *  *  *  *  *  *  *  *  * ',
    'P4 *  *  *  *  *  *  *  *  * ',
    'P5 *  *  *  *  *  *  *  *  * ',
    'P6 *  *  *  *  *  *  *  *  * ',
    'P7 *  *  *  *  *  *  *  *  * ',
    'P8 *  *  *  *  *  *  *  *  * ',
    'P9 *  *  *  * +OU *  *  *  * ',
    'P+',
    'P-00HI00HI00KA00KA00KI00KI00KI00KI00GI00GI00GI00GI00KE00KE00KE00KE00KY00KY00KY00KY'
    '00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU',
    '-'
])

STR_MAX_LEGAL_MOVES = '\n'.join([
    'P1 *  *  *  *  *  *  *  * +HI',
    'P2-OU+GI+GI * +GI * +OU *  * ',
    'P3 *  *  *  * +KA *  *  *  * ',
    'P4 *  *  *  *  *  *  *  *  * ',
    'P5 *  *  *  *  *  *  *  *  * ',
    'P6 *  *  *  *  *  *  *  *  * ',
    'P7 *  *  *  *  *  *  *  *  * ',
    'P8 *  *  *  *  *  *  *  *  * ',
    'P9 *  *  * +KY * +KY * +KY * ',
    'P+00HI00KA00KI00GI00KE00KY00FU',
    'P-00KI00KI00KI00KE00KE00KE00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU00FU',
    '+'
])

STATE_HIRATE = State.from_string(STR_HIRATE)
STATE_TSUME_BLACK = State.from_string(STR_TSUME_BLACK)
STATE_TSUME_WHITE = State.from_string(STR_TSUME_WHITE)
STATE_MAX_LEGAL_MOVES = State.from_string(STR_MAX_LEGAL_MOVES)
