import cmogcore
from mogcore import *


class Game(cmogcore.Game):

    def __init__(self, state: State):
        cmogcore.Game.__init__(self, state)

    def __str__(self):
        buf = []
        buf.append(str(State.wrap(self.states[0].state)))
        for m in self.moves:
            buf.append(str(ExtendedMove.wrap(m)))
        return '\n'.join(buf)
