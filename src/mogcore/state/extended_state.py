from collections import defaultdict
import cmogcore
from mogcore import *
import util


class ExtendedState(cmogcore.ExtendedState):

    def __str__(self):
        return State.wrap(self.state).__str__()

    def __repr__(self):
        return 'ExtendedState(state=%r)' % (self.state)

    @classmethod
    def from_string(cls, s):
        """Build ExtendedState object from CSA-formatted string"""

        return ExtendedState(State.from_string(s))

    def legal_move_bbs(self) -> [BitBoard]:
        return [BitBoard.wrap(bb) for bb in self.get_legal_moves()]

    def legal_moves(self) -> [Move]:
        ret = []

        lm = self.get_legal_moves()
        for i in range(40):
            raw_pt = PieceType(self.state.get_raw_piece_type(i))
            for j, pt in [(i, raw_pt), (i + 40, raw_pt.promoted())]:
                if (lm[j]):
                    o = Turn(self.state.get_owner(i))
                    pos = Pos(self.state.get_position(i))
                    ret.extend([Move(o, pos, Pos(to), pt) for to in lm[j].to_list()])
        return ret

    def move_next(move: Move) -> None:
        self.move(move.turn, move.from_, move.to, move.piece_type)
