def grouped(iterable, n):
    """TODO: Write description"""

    if n <= 0:
        raise ValueError('n must be positive integer.')

    return [iterable[i:i + n] for i in range(0, len(iterable), n)]
