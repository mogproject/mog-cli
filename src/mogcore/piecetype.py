from itertools import chain, accumulate
from .atomiccsatype import AtomicCsaType


class PieceType(AtomicCsaType):
    table = ['OU', 'HI', 'KA', 'KY', 'KI', 'GI', 'KE', 'FU',
             None, 'RY', 'UM', 'NY', None, 'NG', 'NK', 'TO']

    # max number of each pieces
    capacity = [2, 2, 2, 4, 4, 4, 4, 18]

    def __init__(self, value):
        super(PieceType, self).__init__(value)

    def is_promoted(self):
        """Return True if it is promoted."""
        return self.value >= 8

    def promoted(self):
        """Get promoted piece type. If the piece type doesn't allow promoting, return self."""
        try:
            return PieceType(self.value | 8)
        except AssertionError:
            return self

    def demoted(self):
        """Get original piece type"""
        return PieceType(self.value & 7)


# define piece types
(
    KING, ROOK, BISHOP, LANCE, GOLD, SILVER, KNIGHT, PAWN,
    PROOK, PBISHOP, PLANCE, PSILVER, PKNIGHT, PPAWN
) = (PieceType(i) for i in range(16) if i not in [8, 12])

# List of hand-available piece types (ordered)
PIECE_TYPE_HANDS = [ROOK, BISHOP, GOLD, SILVER, KNIGHT, LANCE, PAWN]

# Helper dictionary to look up capacity from piece type
PIECE_TYPE_CAPACITIES = dict((PieceType(i), PieceType.capacity[i]) for i in range(8))

# Helper dictionary to get offset for each demoted piece type
PIECE_TYPE_OFFSETS = dict(accumulate(
    ((PieceType(i), ([0] + PieceType.capacity)[i]) for i in range(8)), lambda a, x: (x[0], a[1] + x[1])))

# Helper list to get piece type from piece id
PIECE_TYPES = list(chain.from_iterable([p] * PIECE_TYPE_CAPACITIES[p] for p in [PieceType(i) for i in range(8)]))
