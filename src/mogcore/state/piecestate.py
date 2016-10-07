from typing import Optional
import cmogcore
from mogcore import *
from util import CaseClass


class PieceState(CaseClass):
    """
    Set owner None when the piece is not active.
    """

    def __init__(self, owner: Optional[Turn]=None, is_promoted: bool=False, position: Pos=HAND):
        CaseClass.__init__(self, owner=owner, is_promoted=is_promoted, position=position)

    def is_active(self) -> bool:
        return self.owner is not None

    def value(self) -> int:
        if self.is_active():
            ret = self.owner.value << 8
            ret |= (1 if self.is_promoted else 0) << 7
            ret |= self.position.value
            return ret
        else:
            return -1

    @classmethod
    def wrap(cls, value: int):
        if value == -1:
            return PieceState()
        owner = WHITE if value >> 8 else BLACK
        is_promoted = bool((value >> 7) & 1)
        position = Pos(value & 127)
        return PieceState(owner, is_promoted, position)


RAW_PIECE_TYPES = [
    KING, KING,
    ROOK, ROOK,
    BISHOP, BISHOP,
    LANCE, LANCE, LANCE, LANCE,
    GOLD, GOLD, GOLD, GOLD,
    SILVER, SILVER, SILVER, SILVER,
    KNIGHT, KNIGHT, KNIGHT, KNIGHT,
    PAWN, PAWN, PAWN, PAWN, PAWN, PAWN, PAWN, PAWN, PAWN,
    PAWN, PAWN, PAWN, PAWN, PAWN, PAWN, PAWN, PAWN, PAWN,
]
