from mogcore.turn import Turn
from mogcore.pos import Pos, HAND
from mogcore.piecetype import PieceType
from util.caseclass import CaseClass


class Move(CaseClass):
    def __init__(self, turn, from_, to, piece_type):
        assert(isinstance(turn, Turn))
        assert(isinstance(from_, Pos))
        assert(isinstance(to, Pos))
        assert(isinstance(piece_type, PieceType))
        assert from_ != to, 'from_ and to must not be same'
        assert to != HAND, 'to must not be HAND'
        CaseClass.__init__(self, turn=turn, from_=from_, to=to, piece_type=piece_type)

    def __str__(self):
        return '%s%s%s%s' % (self.turn, self.from_, self.to, self.piece_type)

    @classmethod
    def from_string(cls, s):
        if not isinstance(s, str):
            raise ValueError('Mal-formed CSA string for %s: %s' % (cls.__name__, s))

        t = Turn.from_string(s[:1])
        from_ = Pos.from_string(s[1:3])
        to = Pos.from_string(s[3:5])
        pt = PieceType.from_string(s[5:])
        return cls(t, from_, to, pt)
