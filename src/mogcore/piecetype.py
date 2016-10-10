from itertools import chain, accumulate
from .atomiccsatype import AtomicCsaType


class PieceType(AtomicCsaType):
    table = ['HI', 'KA', 'KY', 'GI', 'KE', 'FU', 'KI', 'OU',
             'RY', 'UM', 'NY', 'NG', 'NK', 'TO']

    # max number of each pieces
    capacity = [2, 2, 4, 4, 4, 18, 4, 2]

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

    def is_capturable(self):
        """Return True if it can be captured."""
        return self != KING

    @classmethod
    def from_piece_id(cls, id):
        """Get object from piece id"""
        return _PIECE_TYPES[id]


# define piece types
(
    ROOK, BISHOP, LANCE, SILVER, KNIGHT, PAWN, GOLD, KING,
    PROOK, PBISHOP, PLANCE, PSILVER, PKNIGHT, PPAWN
) = (PieceType(i) for i in range(14))

# List of hand-available piece types (ordered)
PIECE_TYPE_HANDS = [ROOK, BISHOP, GOLD, SILVER, KNIGHT, LANCE, PAWN]

# Helper dictionary to look up capacity from piece type
PIECE_TYPE_CAPACITIES = dict((PieceType(i), PieceType.capacity[i]) for i in range(8))

# Helper dictionary to get offset for each demoted piece type
PIECE_TYPE_OFFSETS = dict(accumulate(
    ((PieceType(i), ([0] + PieceType.capacity)[i]) for i in range(8)), lambda a, x: (x[0], a[1] + x[1])))

# Helper list to get piece type from piece id
_PIECE_TYPES = list(chain.from_iterable([p] * PIECE_TYPE_CAPACITIES[p] for p in [PieceType(i) for i in range(8)]))
