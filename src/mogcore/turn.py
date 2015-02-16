from .atomiccsatype import AtomicCsaType


class Turn(AtomicCsaType):
    table = ['+', '-']

    min_value = 0

    def __init__(self, value):
        super(Turn, self).__init__(value)

    def __invert__(self):
        return Turn(self.value ^ 1)
