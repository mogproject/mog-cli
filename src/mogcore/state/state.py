from collections import defaultdict
import cmogcore
from mogcore import *
import util


class State(cmogcore.State):

    def __init__(self, turn: Turn=BLACK, owner_bits: int=0, hand_bits: int=0, promoted_bits: int=0,
                 unused_bits: int=0x000000ffffffffff, board: BitBoard=BitBoard.EMPTY, position: [int]=[0xffffffffffffffff] * 5):

        if len(position) != 5:
            raise ValueError('position must have 5 elements')

        cmogcore.State.__init__(self, turn.value, owner_bits, hand_bits, promoted_bits, unused_bits, board, position)

        try:
            self.validate()
        except RuntimeError as e:
            raise ValueError('invalid state: %s: %s' % (e, State.__repr_string(
                turn, owner_bits, hand_bits, promoted_bits, unused_bits, board, position)))

        self.turn = turn
        self.board = board

    @staticmethod
    def wrap(state: cmogcore.State):
        return State(
            Turn(state._turn),
            state.owner_bits,
            state.hand_bits,
            state.promoted_bits,
            state.unused_bits,
            BitBoard.wrap(state._board),
            state.position)

    def __str__(self):
        board = [' * '] * 81
        hands = [defaultdict(int), defaultdict(int)]
        for i in range(40):
            if not self.is_used(i):
                continue

            owner = Turn(self.get_owner(i))
            pt = PieceType(self.get_piece_type(i))
            ps = Pos(self.get_position(i))

            if ps == HAND:
                hands[owner.value][pt] += 1
            else:
                board[ps.value] = '%s%s' % (owner, pt)

        buf = ['P%d%s' % (i + 1, ''.join(reversed(board[i * 9:(i + 1) * 9]))) for i in range(9)]
        buf.append('P+' + ''.join(chain.from_iterable(['00%s' % p] * hands[0][p] for p in PIECE_TYPE_HANDS)))
        buf.append('P-' + ''.join(chain.from_iterable(['00%s' % p] * hands[1][p] for p in PIECE_TYPE_HANDS)))
        buf.append(str(self.turn))
        return '\n'.join(buf)

    @staticmethod
    def __repr_string(turn, owner_bits, hand_bits, promoted_bits, unused_bits, board, position):
        flags = 'owner_bits=0x%016x, hand_bits=0x%016x, promoted_bits=0x%016x, unused_bits=0x%016x' % (
            owner_bits, hand_bits, promoted_bits, unused_bits
        )
        p = ','.join('0x%016x' % x for x in position)
        return 'State(turn=%r, %s, board=%r, position=[%s])' % (turn, flags, board, p)

    def __repr__(self):
        return self.__repr_string(
            self.turn, self.owner_bits, self.hand_bits, self.promoted_bits, self.unused_bits, self.board, self.position)

    @classmethod
    def from_string(cls, s):
        """Build State object from CSA-formatted string"""

        # recursive function
        def f(builder, lines, used_init, used_all):
            h, t = lines[:1], lines[1:]
            if h and not t:
                # turn to move should be written to the last line
                builder.set_turn(Turn.from_string(h[0]))
                return builder.result()
            elif h and h[0].startswith('PI') and not used_init and not used_all:
                # initiated expression
                return f(cls.__parse_init_expression(builder, h[0][2:]), t, True, used_all)
            elif h and h[0].startswith('P1') and not used_init and not used_all:
                # bundle expression
                return f(cls.__parse_bundle_expression(builder, lines[:9]), lines[9:], True, used_all)
            elif h and h[0][:2] in ['P+', 'P-']:
                # single expression
                (b, used_all) = cls.__parse_single_expression(builder, Turn.from_string(h[0][1]), used_all, h[0][2:])
                return f(b, t, used_init, used_all)
            else:
                raise ValueError('Mal-formed state string')

        return f(StateBuilder(), s.splitlines(), False, False)

    @classmethod
    def __parse_init_expression(cls, builder, line):
        pieces_to_reset = util.grouped(line, 4)

        m = HIRATE_PIECES.copy()

        for p in pieces_to_reset:
            ps = Pos.from_string(p[:2])
            pt = PieceType.from_string(p[2:])
            if m.get(ps) is None:
                raise ValueError('Position to remove is already empty: %s' % p)
            if m.get(ps)[1] != pt:
                raise ValueError('Unmatched piece type in initiated expression: %s' % p)
            m.pop(ps)

        for (ps, (o, pt)) in sorted(m.items()):  # sorted by position (ascending)
            builder.set_piece(o, pt, ps)
        return builder

    @classmethod
    def __parse_bundle_expression(cls, builder, lines):
        def is_valid(ls):
            if len(ls) != 9:
                return False
            for i in range(9):
                if len(ls[i]) != 2 + 3 * 9:
                    return False
                if not ls[i].startswith('P%d' % (i + 1)):
                    return False
            return True

        if not is_valid(lines):
            raise ValueError('Mal-formed bundle expression: %r' % lines)

        for r in range(9):
            for f in range(9):
                s = lines[r][26 - 3 * f:29 - 3 * f]
                if s[0] != ' ':
                    builder.set_piece(Turn.from_string(s[0]), PieceType.from_string(s[1:]), Pos(r * 9 + f))
        return builder

    @classmethod
    def __parse_single_expression(cls, builder, owner, used_all, line):
        # recursive function
        def f(b, chunks):
            if not chunks:
                return b, False
            elif not used_all and chunks == ['00AL']:
                return b.set_all_hand(owner), True
            else:
                return f(b.set_piece(owner, PieceType.from_string(chunks[0][2:]), Pos.from_string(chunks[0][:2])), chunks[1:])

        return f(builder, util.grouped(line, 4))


class StateBuilder:

    def __init__(self):
        self.__state = State()

    def set_turn(self, t: Turn):
        self.__state = self.__state.set_turn(t.value)

    def set_piece(self, owner: Turn, ptype: PieceType, ps: Pos):
        try:
            self.__state = self.__state.set_piece(owner.value, ptype.value, ps.value)
            return self
        except RuntimeError as e:
            raise ValueError('%s: owner=%r, ptype=%r, pos=%r' % (e, owner, ptype, ps))

    def set_all_hand(self, owner: Turn):
        self.__state = self.__state.set_all_hand(owner.value)
        return self

    def result(self):
        return State.wrap(self.__state)


# Hirate mapping of Pos -> (Turn, PieceType)
HIRATE_PIECES = dict([
    (P11, (WHITE, LANCE)), (P21, (WHITE, KNIGHT)), (P31, (WHITE, SILVER)), (P41, (WHITE, GOLD)), (P51, (WHITE, KING)),
    (P91, (WHITE, LANCE)), (P81, (WHITE, KNIGHT)), (P71, (WHITE, SILVER)), (P61, (WHITE, GOLD)),
    (P22, (WHITE, BISHOP)), (P82, (WHITE, ROOK)),
] + [
    (p, (WHITE, PAWN)) for p in [P13, P23, P33, P43, P53, P63, P73, P83, P93]
] + [
    (P19, (BLACK, LANCE)), (P29, (BLACK, KNIGHT)), (P39, (BLACK, SILVER)), (P49, (BLACK, GOLD)), (P59, (BLACK, KING)),
    (P99, (BLACK, LANCE)), (P89, (BLACK, KNIGHT)), (P79, (BLACK, SILVER)), (P69, (BLACK, GOLD)),
    (P28, (BLACK, ROOK)), (P88, (BLACK, BISHOP)),
] + [
    (p, (BLACK, PAWN)) for p in [P17, P27, P37, P47, P57, P67, P77, P87, P97]
])
