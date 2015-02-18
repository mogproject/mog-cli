from .atomiccsatype import AtomicCsaType


class PieceType(AtomicCsaType):
    table = ['OU', 'HI', 'KA', 'KY', 'KI', 'GI', 'KE', 'FU',
             None, 'RY', 'UM', 'NY', None, 'NG', 'NK', 'TO']

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


PIECE_TYPE_MAX_NUMS = {KING: 2, ROOK: 2, BISHOP: 2, LANCE: 4, GOLD: 4, SILVER: 4, KNIGHT: 4, PAWN: 18}
