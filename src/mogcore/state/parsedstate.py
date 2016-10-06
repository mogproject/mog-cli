from collections import defaultdict
import cmogcore
from mogcore import *
import util
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
