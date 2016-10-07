from collections import defaultdict
import cmogcore
from mogcore import *
from mogcore.state.piecestate import PieceState
import util


class SimpleState(cmogcore.SimpleState):
    def __str__(self):
        board = [' * '] * 81
        hands = [defaultdict(int), defaultdict(int)]
        for i, p in enumerate(self.pieces()):
            if p < 0:
                continue
            owner = Turn(p >> 8)
            pt = PieceType.from_piece_id(i)
            pt = pt.promoted if (p >> 7) & 1 else pt
            ps = Pos(p & 0x7f)
            if ps == HAND:
                hands[owner.value][pt] += 1
            else:
                board[ps.value] = '%s%s' % (owner, pt)

        buf = ['P%d%s' % (i + 1, ''.join(reversed(board[i * 9:(i + 1) * 9]))) for i in range(9)]
        buf.append('P+' + ''.join(chain.from_iterable(['00%s' % p] * hands[0][p] for p in PIECE_TYPE_HANDS)))
        buf.append('P-' + ''.join(chain.from_iterable(['00%s' % p] * hands[1][p] for p in PIECE_TYPE_HANDS)))
        buf.append(str(Turn(self.turn)))
        return '\n'.join(buf)

    def __repr__(self):
        return 'SimpleState(turn=%r, pieces=%r)' % (self.turn, self.pieces())

    def pieces(self):
        return [self.get_piece(i) for i in range(40)]

    @classmethod
    def from_string(cls, s):
        """Build SimpleState object from CSA-formatted string"""

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
                (builder, used_all) = cls.__parse_single_expression(
                    builder, Turn.from_string(h[0][1]), used_all, h[0][2:])
                return f(builder, t, used_init, used_all)
            else:
                raise ValueError('Malformed state string')

        return f(SimpleStateBuilder(), s.splitlines(), False, False)

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
            raise ValueError('Malformed bundle expression: %r' % lines)

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
                return builder, False
            elif not used_all and chunks == ['00AL']:
                for i, p in enumerate(builder.pieces):
                    pt = PieceType.from_piece_id(i)
                    if not p.is_active() and pt.is_capturable():
                        builder.set_piece(owner, pt, HAND)

                return b, True
            else:
                b.set_piece(owner, PieceType.from_string(chunks[0][2:]), Pos.from_string(chunks[0][:2]))
                return f(b, chunks[1:])

        return f(builder, util.grouped(line, 4))


class SimpleStateBuilder:
    def __init__(self, t=None, pieces=None):
        self.turn = t
        self.pieces = pieces or [PieceState()] * 40
        self.occ_all = BitBoard()
        self.occ_pawn = [BitBoard(), BitBoard()]

    def __borrow(self, ptype):
        origin = ptype.demoted()

        for i in range(PIECE_TYPE_OFFSETS[origin], PIECE_TYPE_OFFSETS[origin] + PIECE_TYPE_CAPACITIES[origin]):
            if not self.pieces[i].is_active():
                return i

        raise ValueError('There is no left for that piece type: %s' % ptype)

    def set_turn(self, t):
        self.turn = t

    def set_piece(self, owner, ptype, ps):
        args = 'owner=%r, ptype=%r, pos=%r' % (owner, ptype, ps)

        if ps == HAND:
            if ptype == KING:
                raise ValueError('King must not be held in hand: %s' % args)
            if ptype.is_promoted():
                raise ValueError('Promoted piece must not be held in hand: %s' % args)
        else:
            if self.occ_all.get(ps.value):
                raise ValueError('Pos already occupied by another piece: %s' % args)
            if ptype == KING and self.pieces[0].is_active() and self.pieces[0].owner == owner:
                raise ValueError('One must not have two kings: %s' % args)
            if ptype == PAWN and self.occ_pawn[owner.value].get(ps.value):
                raise ValueError('No two pawns should exist in same file: %s' % args)

        pid = self.__borrow(ptype)

        # take one piece
        if ps != HAND:
            self.occ_all.set(ps.value)
            if ptype == PAWN:
                self.occ_pawn[owner.value] |= BitBoard().set(ps.value).spread_all_file()
        self.pieces[pid] = PieceState(owner, ptype.is_promoted(), ps)

    def result(self):
        return SimpleState(self.turn.value, [x.value() for x in self.pieces])


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
