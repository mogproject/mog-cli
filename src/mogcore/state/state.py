from collections import defaultdict
import cmogcore
from mogcore import *
import util


class State(cmogcore.State):

    def __str__(self):
        return State.wrap(self.state).__str__()

    def __repr__(self):
        return 'State(state=%r)' % (State.wrap(self.state))

    @classmethod
    def wrap(cls, st: cmogcore.State):
        return cls(st.state, st.attack_bbs, st.board_table, st.occ, st.occ_pawn, st.hash_value)

    @classmethod
    def from_string(cls, s):
        """Build State object from CSA-formatted string"""

        return State(SimpleState.from_string(s))

    def legal_move_bbs(self) -> [BitBoard]:
        return [BitBoard.wrap(bb) for bb in self.get_legal_moves()]

    def legal_moves(self) -> [SimpleMove]:
        ret = []

        lm = self.get_legal_moves()
        for i in range(40):
            raw_pt = PieceType(self.state.get_raw_piece_type(i))
            for j, pt in [(i, raw_pt), (i + 40, raw_pt.promoted())]:
                if (lm[j]):
                    o = Turn(self.state.get_owner(i))
                    pos = Pos(self.state.get_position(i))
                    ret.extend([SimpleMove(o, pos, Pos(to), pt) for to in lm[j].to_list()])
        return ret

    def move(self, m: SimpleMove):
        return self.wrap(cmogcore.State.move(self, m))
