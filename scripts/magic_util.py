#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utilities for finding magic number"""


usage = """
Usage:
  Use functions in the Python REPL.

Example:
  $ python3
  >>> from scripts.magic_util import *
  >>> x2i(0x0080200802008000)
  [15, 25, 35, 45, 55]
  >>> i2x([15, 25, 35, 45, 55])
  36064015784378368
"""

from collections import defaultdict


def x2i(u64):
    """Convert 64-bit integer to list of indices of the 1-bit"""
    return [i for i in range(64) if 1 << i & u64]


def i2x(xs):
    return sum(1 << i for i in xs)


def mul(xs, ys):
    """Multiply two bit-index lists"""
    bits = defaultdict(list)
    for (i, x) in enumerate(xs):
        for y in ys:
            z = x + y
            if z >= 64:
                continue
            bits[z].append(i)

    # check bit health
    carry = 0
    buf = []
    for i in range(64):
        if not carry:
            if not bits[i]:
                s = 'empty'
            elif len(bits[i]) == 1:
                s = 'fixed => %x' % bits[i][0]
            else:
                s = 'dup   => %s' % ['%x' % x for x in bits[i]]
        else:
            s = 'dirty'
        carry = (carry + len(bits[i])) // 2
        buf.append('%2d: %s' % (i, s))

    print('\n'.join(list(reversed(buf))[:16]))
    return bits


if __name__ == '__main__':
    print(usage)
