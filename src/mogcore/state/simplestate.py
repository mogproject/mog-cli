from itertools import chain
from collections import defaultdict
import cmogcore
from mogcore import *


class SimpleState(cmogcore.SimpleState):
    piece_types = list(chain.from_iterable([p] * PIECE_TYPE_MAX_NUMS[p] for p in [PieceType(i) for i in range(8)]))

    def __str__(self):
        board = [' * '] * 81
        hands = [defaultdict(int), defaultdict(int)]
        for i, p in enumerate(self.pieces()):
            if p < 0:
                continue
            owner = Turn(p >> 8)
            pt = PieceType(self.piece_types[i].value | (p >> 4) & 1)
            pos = Pos(p & 0x3f)
            if pos == HAND:
                hands[owner.value][pt] += 1
            else:
                board[pos.value] = '%s%s' % (owner, pt)

        buf = ['P%d%s' % (i + 1, ''.join(board[(i + 1) * 9 - 1:max(0, i * 9 - 1): -1])) for i in range(9)]

        hand_piece_types = [ROOK, BISHOP, GOLD, SILVER, KNIGHT, LANCE, PAWN]
        buf.append('P+' + ''.join(chain.from_iterable(['00%s' % p] * hands[0][p] for p in hand_piece_types)))
        buf.append('P-' + ''.join(chain.from_iterable(['00%s' % p] * hands[1][p] for p in hand_piece_types)))
        buf.append(str(Turn(self.turn)))
        return '\n'.join(buf)

    def pieces(self):
        return [self.get_piece(i) for i in range(40)]

    @classmethod
    def from_string(s):
        """Build SimpleState object from CSA-formatted string"""
        b = SimpleStateBuilder()

        # todo: implement

        return b.result()


class SimpleStateBuilder:
    def __init__(self):
        self.unused_pieces = SimpleState.piece_nums.copy()
        self.pieces = [-1] * 40
        self.occ_all = BitBoard()
        self.occ_pawn = [BitBoard(), BitBoard()]
        self.king_used = [False, False]

    def append(self, owner, ptype, pos):
        args = 'owner=%r, ptype=%r, pos=%r' % (owner, ptype, pos)

        if pos == HAND:
            if ptype == KING:
                raise ValueError('King must not be held in hand: %s' % args)
            if ptype.is_promoted():
                raise ValueError('Promoted piece must not be held in hand: %s' % args)
        else:
            if self.occ_all.get(pos):
                raise ValueError('Pos already occupied by another piece: %s' % args)
            if ptype == KING and self.king_used[owner]:
                raise ValueError('One must not have two kings: %s' % args)
            if ptype == PAWN and self.occ_pawn[owner].get(pos):
                raise ValueError('No two pawns should exist in same file: %s' % args)

        org = ptype.demoted()
        if self.unused_pieces[org] == 0:
            raise ValueError('There is no left for that piece type: %s' % args)

        # take one piece
        self.unused_pieces[org] -= 1
        if pos != HAND:
            self.occ_all.set(pos)
            if ptype == PAWN:
                self.occ_pawn |= BitBoard().set(pos).spread_all_file()
            if ptype == KING:
                self.king_used[owner] = True
        self.pieces.append((owner, ptype, pos))

    def result(self):
        if not any(self.king_used):
            raise ValueError('There must be one or two kings.')
        for owner, ptype, pos in self.pieces:
            pass
