from .atomiccsatype import AtomicCsaType


class Turn(AtomicCsaType):
    table = ['+', '-']

    def __init__(self, value):
        super(Turn, self).__init__(value)

    def __invert__(self):
        return Turn(self.value ^ 1)

BLACK, WHITE = (Turn(i) for i in range(2))
