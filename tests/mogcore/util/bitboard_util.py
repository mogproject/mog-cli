from cmogcore import BitBoard


def bitboards_from_string(s):
    """
    Make bitboard tuple array from string
    :param s: string with 9 lines (should contain only '-', '*', 'x', 'o', space and new line)
    :return: array of 3-array of (bitboard with {'*' is on}, {'*x' are on}, {'*xo' are on})

    e.g.

    bitboards_from_string(\"""
    --------- ********* ---------
    --------- ********* ---------
    --------- ********* ---------
    --------- ********* ---------
    --------- ********* ---------
    --------- ********* ---------
    --------- ********* ooooooooo
    --------- ********* xxxxxxxxx
    --------- ********* *********
    \""") = [
      [
        BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000),
        BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000),
        BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000)
      ], [
        BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777),
        BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777),
        BitBoard(0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777, 0o777)
      ], [
        BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o777),
        BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o777, 0o777),
        BitBoard(0o000, 0o000, 0o000, 0o000, 0o000, 0o000, 0o777, 0o777, 0o777)
      ]
    ]
    """
    # trim spaces and empty line
    xs = [line.replace(' ', '') for line in s.splitlines() if line.strip()]

    # split by 9-characters
    ys = [[ss[0 + i:9 + i] for i in range(0, len(ss), 9)] for ss in xs]

    # transpose
    zs = list(map(list, zip(*ys)))

    traits = ['*', '*x', '*xo']

    return [[BitBoard(*[sum(1 << i if a[8 - i] in t else 0 for i in range(9)) for a in z]) for t in traits] for z in zs]
