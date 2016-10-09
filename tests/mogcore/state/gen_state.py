from mogcore import *


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
