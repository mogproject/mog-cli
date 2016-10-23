import cmogcore
from mogcore import *
import util


class TimedMove():

    def __init__(self, move_str: str, elapsed_time: int=-1):
        self.move_str = move_str
        self._elapsed_time = elapsed_time  # change the name to avoid a conflict

    def __str__(self):
        return '%s%s' % (self.move_str, '' if self._elapsed_time < 0 else ',T%d' % self._elapsed_time)


class ExtendedMove(cmogcore.ExtendedMove, TimedMove):

    def __init__(self, turn: Turn, from_: Pos, to: Pos, piece_type: PieceType, elapsed_time: int=-1):
        assert isinstance(turn, Turn)
        assert isinstance(from_, Pos)
        assert isinstance(to, Pos)
        assert isinstance(piece_type, PieceType)
        assert from_ != to, 'from_ and to must not be same'
        assert to != HAND, 'to must not be HAND'

        cmogcore.ExtendedMove.__init__(self, turn.value, from_.value, to.value, piece_type.value, elapsed_time, 0, 0)
        TimedMove.__init__(self, str(Move.wrap(self)), elapsed_time)
        self.turn = turn
        self.from_ = from_
        self.to = to
        self.piece_type = piece_type

    def __repr__(self):
        # todo
        return 'ExtendedMove()'

    @classmethod
    def wrap(cls, m: cmogcore.ExtendedMove):
        if m.move_type == 0:
            return ExtendedMove(Turn(m._turn), Pos(m._from), Pos(m._to), PieceType(m._piece_type), m.elapsed_time)
        elif m.move_type == 1:
            return Resign(m.elapsed_time)
        elif m.move_type == 2:
            return TimeUp(m.elapsed_time)
        elif m.move_type == 3:
            return IllegalMove(m.elapsed_time)
        elif m.move_type == 4:
            return PerpetualCheck(m.elapsed_time)
        elif m.move_type == 5:
            return DeclareWin(m.elapsed_time)
        elif m.move_type == 6:
            return ThreefoldRepetition(m.elapsed_time)

    @classmethod
    def from_string(cls, s):
        """Build ExtendedMove object from CSA-formatted string"""
        # todo
        return ExtendedMove(State.from_string(s))


class Resign(cmogcore.Resign, TimedMove):

    def __init__(self, elapsed_time=-1):
        cmogcore.Resign.__init__(self, elapsed_time)
        TimedMove.__init__(self, '%TORYO', elapsed_time)


class TimeUp(cmogcore.TimeUp, TimedMove):

    def __init__(self, elapsed_time=-1):
        cmogcore.TimeUp.__init__(self, elapsed_time)
        TimedMove.__init__(self, '#TIME_UP', elapsed_time)


class IllegalMove(cmogcore.IllegalMove, TimedMove):

    def __init__(self, elapsed_time=-1):
        cmogcore.IllegalMove.__init__(self, elapsed_time)
        TimedMove.__init__(self, '#ILLEGAL_MOVE', elapsed_time)


class PerpetualCheck(cmogcore.PerpetualCheck, TimedMove):

    def __init__(self, elapsed_time=-1):
        cmogcore.PerpetualCheck.__init__(self, elapsed_time)
        TimedMove.__init__(self, '#OUTE_SENNICHITE', elapsed_time)


class DeclareWin(cmogcore.DeclareWin, TimedMove):

    def __init__(self, elapsed_time=-1):
        cmogcore.DeclareWin.__init__(self, elapsed_time)
        TimedMove.__init__(self, '%KACHI', elapsed_time)


class ThreefoldRepetition(cmogcore.ThreefoldRepetition, TimedMove):

    def __init__(self, elapsed_time=-1):
        cmogcore.ThreefoldRepetition.__init__(self, elapsed_time)
        TimedMove.__init__(self, '#SENNICHITE', elapsed_time)
