import cmogcore
from mogcore.turn import Turn
from mogcore.pos import Pos, HAND
from mogcore.piecetype import PieceType


class SimpleMove(cmogcore.SimpleMove):

    def __init__(self, turn: Turn, from_: Pos, to: Pos, piece_type: PieceType):
        assert isinstance(turn, Turn)
        assert isinstance(from_, Pos)
        assert isinstance(to, Pos)
        assert isinstance(piece_type, PieceType)
        assert from_ != to, 'from_ and to must not be same'
        assert to != HAND, 'to must not be HAND'

        cmogcore.SimpleMove.__init__(self, turn.value, from_.value, to.value, piece_type.value)
        self.turn = turn
        self.from_ = from_
        self.to = to
        self.piece_type = piece_type

    def __str__(self):
        return '%s%s%s%s' % (self.turn, self.from_, self.to, self.piece_type)

    def __repr__(self):
        return 'SimpleMove(turn=%r, from_=%r, to=%r, piece_type=%r)' % (self.turn, self.from_, self.to, self.piece_type)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.turn == other.turn and self.from_ == other.from_ and self.to == other.to and self.piece_type == other.piece_type

    @classmethod
    def wrap(cls, m: cmogcore.SimpleMove):
        return cls(Turn(m._turn), Pos(m._from), Pos(m._to), PieceType(m._piece_type))

    @classmethod
    def from_string(cls, s: str):
        if not isinstance(s, str):
            raise ValueError('Mal-formed CSA string for %s: %s' % (cls.__name__, s))

        t = Turn.from_string(s[:1])
        from_ = Pos.from_string(s[1:3])
        to = Pos.from_string(s[3:5])
        pt = PieceType.from_string(s[5:])
        return SimpleMove(t, from_, to, pt)
