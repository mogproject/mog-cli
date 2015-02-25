from collections import defaultdict
import cmogcore
from mogcore import *
import util


class SimpleState(cmogcore.SimpleState):
    def __str__(self):
        board = [' * '] * 81
        hands = [defaultdict(int), defaultdict(int)]
        for i, p in enumerate(self.pieces()):
            if p < 0:
                continue
            owner = Turn(p >> 8)
            pt = PieceType(PIECE_TYPES[i].value | (p >> 7) & 1)
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

    def pieces(self):
        return [self.get_piece(i) for i in range(40)]

    @classmethod
    def from_string(cls, s):
        """Build SimpleState object from CSA-formatted string"""
        used_init = False
        used_all = False

        b = SimpleStateBuilder()

        lines = s.splitlines()
        while lines:
            h = lines[0]
            if h.startswith('PI') and not used_init and not used_all:
                b = cls.__parse_init_expression(h[2:])
                used_init = True
            elif h.startswith('P1') and not used_init and not used_all:
                # read nine lines
                pass  # todo: implement
            elif h[:2] in ['P+', 'P-']:
                pass  # todo: implement
            elif lines in [['+'], ['-']]:  # last line shows turn to move
                b.set_turn(Turn.from_string(h))
            else:
                pass
            lines = lines[1:]

        return b.result()

    @classmethod
    def make_piece(cls, owner, is_promoted, ps):
        ret = owner.value << 8
        ret |= (1 if is_promoted else 0) << 7
        ret |= ps.value
        return ret

    @classmethod
    def __parse_init_expression(cls, line):
        b = SimpleStateBuilder(HIRATE.turn, HIRATE.pieces()[:])
        ps = util.grouped(line, 4)
        # todo: implement
        return b


class SimpleStateBuilder:
    def __init__(self, t=BLACK, pieces=[None] * 40):
        self.turn = t
        self.pieces = pieces
        self.offsets = {k: (v, v + PIECE_TYPE_CAPACITIES[k]) for k, v in PIECE_TYPE_OFFSETS.items()}
        self.occ_all = BitBoard()
        self.occ_pawn = [BitBoard(), BitBoard()]

    def __borrow(self, ptype):
        origin = ptype.demoted()
        offset, limit = self.offsets[origin]
        if offset >= limit:
            return -1
        index = offset + 1
        self.offsets[origin] = (index, limit)
        return index

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
            if self.occ_all.get(pos):
                raise ValueError('Pos already occupied by another piece: %s' % args)
            if ptype == KING and self.pieces[owner] is not None:
                raise ValueError('One must not have two kings: %s' % args)
            if ptype == PAWN and self.occ_pawn[owner].get(pos):
                raise ValueError('No two pawns should exist in same file: %s' % args)

        pid = self.__borrow(ptype)
        if pid < 0:
            raise ValueError('There is no left for that piece type: %s' % args)

        # take one piece
        if ps != HAND:
            self.occ_all.set(pos)
            if ptype == PAWN:
                self.occ_pawn |= BitBoard().set(ps).spread_all_file()
        self.pieces[pid] = SimpleState.make_piece(owner, ptype.is_promoted(), ps)

    def result(self):
        if self.pieces[0:2] == [None] * 2:
            raise ValueError('There must be one or two kings.')

        return SimpleState(self.turn.value, [-1 if x is None else x for x in self.pieces])


HIRATE = SimpleState(BLACK.value, [SimpleState.make_piece(o, pr, ps) for (o, pr, ps) in [
    (BLACK, False, P59), (WHITE, False, P51),
    (BLACK, False, P28), (WHITE, False, P82),
    (BLACK, False, P88), (WHITE, False, P22),
    (BLACK, False, P19), (BLACK, False, P99), (WHITE, False, P11), (WHITE, False, P91),
    (BLACK, False, P49), (BLACK, False, P69), (WHITE, False, P41), (WHITE, False, P61),
    (BLACK, False, P39), (BLACK, False, P79), (WHITE, False, P31), (WHITE, False, P71),
    (BLACK, False, P29), (BLACK, False, P89), (WHITE, False, P21), (WHITE, False, P81),
    (BLACK, False, P17), (BLACK, False, P27), (BLACK, False, P37),
    (BLACK, False, P47), (BLACK, False, P57), (BLACK, False, P67),
    (BLACK, False, P77), (BLACK, False, P87), (BLACK, False, P97),
    (WHITE, False, P13), (WHITE, False, P23), (WHITE, False, P33),
    (WHITE, False, P43), (WHITE, False, P53), (WHITE, False, P63),
    (WHITE, False, P73), (WHITE, False, P83), (WHITE, False, P93),
]])
