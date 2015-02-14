import cmogcore


class BitBoard(cmogcore.BitBoard):
    def __str__(self):
        s = ['*' if self.get(i) else '-' for i in range(81)]
        r = [''.join(reversed(s[i * 9: (i + 1) * 9])) for i in range(9)]
        return '\n'.join(r)

    @staticmethod
    def wrap(bb):
        return BitBoard(bb.lo, bb.hi)

    def indices(self):
        return [i for i in range(81) if self.get(i)]
