from collections import defaultdict
import cmogcore
from mogcore import *


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
        b = SimpleStateBuilder()

        # todo: implement

        return b.result()


class SimpleStateBuilder:
    def __init__(self):
        self.turn = BLACK
        self.pieces = [None] * 40
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

    @staticmethod
    def __make_int(owner, ptype, ps):
        ret = owner.value << 8
        ret |= (1 if ptype.is_promoted() else 0) << 7
        ret |= ps.value
        return ret

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
        self.pieces[pid] = self.__make_int(owner, ptype, ps)

    def result(self):
        if self.pieces[0:2] == [None] * 2:
            raise ValueError('There must be one or two kings.')

        return SimpleState(self.turn.value, [-1 if x is None else x in self.pieces])
