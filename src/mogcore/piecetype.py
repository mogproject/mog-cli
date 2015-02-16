from .atomiccsatype import AtomicCsaType


class PieceType(AtomicCsaType):
    table = ['OU', 'HI', 'KA', 'KY', 'KI', 'GI', 'KE', 'FU',
             None, 'RY', 'UM', 'NY', None, 'NG', 'NK', 'TO']

    min_value = 0

    def __init__(self, value):
        super(PieceType, self).__init__(value)

    def promoted(self):
        """Get promoted piece type. If the piece type doesn't allow promoting, return self."""
        try:
            return PieceType(self.value | 8)
        except AssertionError:
            return self

    def demoted(self):
        """Get original piece type"""
        return PieceType(self.value & 7)
