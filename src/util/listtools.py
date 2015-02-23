def grouped(iterable, n):
    """TODO: Write description"""

    return [iterable[i:i + n] for i in range(0, len(iterable), n)]