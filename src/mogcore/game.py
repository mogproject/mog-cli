import cmogcore
from mogcore import *
from mogcore.state.simple_state import HIRATE


class Game(cmogcore.Game):

    def __init__(self, state: SimpleState=HIRATE):
        cmogcore.Game.__init__(self, state)

    def __str__(self):
        buf = []
        buf.append(str(SimpleState.wrap(self.states[0].state)))
        for m in self.moves:
            buf.append(str(Move.wrap(m)))
        return '\n'.join(buf)
