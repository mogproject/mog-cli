import cmogcore


class BitBoard(cmogcore.BitBoard):
    def __str__(self):
        s = ['*' if self.get(i) else '-' for i in range(81)]
        r = [''.join(reversed(s[i * 9: (i + 1) * 9])) for i in range(9)]
        return '\n'.join(r)

# constant bitboards
empty = BitBoard(0, 0)
full = BitBoard(0xffffffffffffffff, 0xffffffffffffffff)
