from collections import defaultdict
import cmogcore
from mogcore import *
import util
from mogcore.state.piecestate import PieceState, RAW_PIECE_TYPES
from mogcore.state.simplestate import SimpleState


class ParsedState(cmogcore.ParsedState):

    def __str__(self):
        return SimpleState(self.turn, self.pieces()).__str__()

    def __repr__(self):
        return 'ParsedState(turn=%r, pieces=%r)' % (self.turn, self.pieces())

    def pieces(self):
        return [self.get_piece(i) for i in range(40)]

    @classmethod
    def from_string(cls, s):
        """Build ParsedState object from CSA-formatted string"""
        return ParsedState(SimpleState.from_string(s))

    def legal_move_bbs(self) -> [BitBoard]:
        return [BitBoard.wrap(bb) for bb in self.get_legal_moves()]

    def legal_moves(self) -> [Move]:
        ret = []
        pieces = [PieceState.wrap(p) for p in self.pieces()]
        lm = self.get_legal_moves()
        for i in range(40):
            for j, pt in [(i, RAW_PIECE_TYPES[i]), (i + 40, RAW_PIECE_TYPES[i].promoted())]:
                if (lm[j]):
                    ret.extend([Move(pieces[i].owner, pieces[i].position, Pos(to), pt) for to in lm[j].to_list()])
        return ret

    def move_next(move: Move) -> None:
        # todo
        pass
