from util import CaseClass


class Turn(CaseClass):
    table = ['+', '-']
    table_inv = dict((v, k) for (k, v) in enumerate(table))

    def __init__(self, value=0):
        assert (isinstance(value, int) and 0 <= value <= 1)
        super(Turn, self).__init__(value=value)

    def __str__(self):
        return Turn.table[self.value]

    def __invert__(self):
        return Turn(1 - self.value)

    @staticmethod
    def from_string(s):
        """Parse CSA format string and get turn"""
        t = Turn.table_inv.get(s)
        return Turn(t) if t is not None else None


BLACK = Turn(0)
WHITE = Turn(1)
