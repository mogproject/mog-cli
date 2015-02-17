from .atomiccsatype import AtomicCsaType


class Pos(AtomicCsaType):
    table = ['00'] + ['%d%d' % (i % 9 + 1, i // 9 + 1) for i in range(81)]

    min_value = -1

    def __init__(self, value):
        super(Pos, self).__init__(value)
        self.file = None if value < 0 else value % 9 + 1
        self.rank = None if value < 0 else value // 9 + 1
