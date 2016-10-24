from typing import Optional
import cmogcore
from mogcore import *
import util
import re


class TimedMove():

    def __init__(self, move_str: str, elapsed_time: Optional[int]=None):
        self.move_str = move_str
        self._elapsed_time = elapsed_time  # change the name to avoid a conflict

    def __str__(self):
        return '%s%s' % (self.move_str, '' if self._elapsed_time is None else ',T%d' % self._elapsed_time)


class Move(cmogcore.Move, TimedMove):

    def __init__(self, turn: Turn, from_: Pos, to: Pos, piece_type: PieceType, elapsed_time: Optional[int]=None):
        assert isinstance(turn, Turn)
        assert isinstance(from_, Pos)
        assert isinstance(to, Pos)
        assert isinstance(piece_type, PieceType)
        assert from_ != to, 'from_ and to must not be same'
        assert to != HAND, 'to must not be HAND'

        et = -1 if elapsed_time is None else elapsed_time
        cmogcore.Move.__init__(self, turn.value, from_.value, to.value, piece_type.value, et, 0, 0)
        TimedMove.__init__(self, str(SimpleMove.wrap(self)), elapsed_time)
        self.turn = turn
        self.from_ = from_
        self.to = to
        self.piece_type = piece_type

    def __repr__(self):
        return 'Move(turn=%s, from_=%s, to=%s, piece_type=%s, elapsed_time=%s)' % (
            self.turn, self.from_, self.to, self.piece_type, self._elapsed_time)

    @classmethod
    def wrap(cls, m: cmogcore.Move):
        if m.move_type == 0:
            return Move(Turn(m._turn), Pos(m._from), Pos(m._to), PieceType(m._piece_type), m.elapsed_time)
        elif m.move_type == 1:
            return Resign(m.elapsed_time)
        elif m.move_type == 2:
            return TimeUp(m.elapsed_time)
        elif m.move_type == 3:
            return IllegalMove(m.elapsed_time)
        elif m.move_type == 4:
            return PerpetualCheck()
        elif m.move_type == 5:
            return DeclareWin(m.elapsed_time)
        elif m.move_type == 6:
            return ThreefoldRepetition()

    @classmethod
    def from_string(cls, s: str):
        """Build Move object from CSA-formatted string"""
        pattern = re.compile(r'^([+\-%#][0-9A-Z_]+)(?:,T(\d{1,5}))?$')
        mt = pattern.match(s)
        if not mt:
            raise ValueError('Mal-formed CSA string for %s: %s' % (cls.__name__, s))

        mv, t = mt.groups()
        t = None if t is None else int(t)

        if mv[:1] == '%' or mv[:1] == '#':
            # todo reduce redundancy
            if mv == '%TORYO':
                return Resign(t)
            if mv == '#TIME_UP':
                return TimeUp(t)
            if mv == '#ILLEGAL_MOVE':
                return IllegalMove(t)
            if mv == '#OUTE_SENNICHITE' and t is None:
                return PerpetualCheck()
            if mv == '%KACHI':
                return DeclareWin(t)
            if mv == '#SENNICHITE' and t is None:
                return ThreefoldRepetition()
            raise ValueError('Mal-formed CSA string for %s: %s' % (cls.__name__, s))
        else:
            m = SimpleMove.from_string(mv)
            return Move(m.turn, m.from_, m.to, m.piece_type, t)


class Resign(cmogcore.Resign, TimedMove):

    def __init__(self, elapsed_time: Optional[int]=None):
        cmogcore.Resign.__init__(self, -1 if elapsed_time is None else elapsed_time)
        TimedMove.__init__(self, '%TORYO', elapsed_time)


class TimeUp(cmogcore.TimeUp, TimedMove):

    def __init__(self, elapsed_time: Optional[int]=None):
        cmogcore.TimeUp.__init__(self, -1 if elapsed_time is None else elapsed_time)
        TimedMove.__init__(self, '#TIME_UP', elapsed_time)


class IllegalMove(cmogcore.IllegalMove, TimedMove):

    def __init__(self, elapsed_time: Optional[int]=None):
        cmogcore.IllegalMove.__init__(self, -1 if elapsed_time is None else elapsed_time)
        TimedMove.__init__(self, '#ILLEGAL_MOVE', elapsed_time)


class PerpetualCheck(cmogcore.PerpetualCheck, TimedMove):

    def __init__(self):
        cmogcore.PerpetualCheck.__init__(self)
        TimedMove.__init__(self, '#OUTE_SENNICHITE', None)


class DeclareWin(cmogcore.DeclareWin, TimedMove):

    def __init__(self, elapsed_time: Optional[int]=None):
        cmogcore.DeclareWin.__init__(self, -1 if elapsed_time is None else elapsed_time)
        TimedMove.__init__(self, '%KACHI', elapsed_time)


class ThreefoldRepetition(cmogcore.ThreefoldRepetition, TimedMove):

    def __init__(self):
        cmogcore.ThreefoldRepetition.__init__(self)
        TimedMove.__init__(self, '#SENNICHITE', None)
