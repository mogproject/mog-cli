from .bitboard import BitBoard

from .turn import Turn

BLACK = Turn(0)
WHITE = Turn(1)

from .piecetype import PieceType

KING = PieceType(0)
ROOK = PieceType(1)
BISHOP = PieceType(2)
LANCE = PieceType(3)
GOLD = PieceType(4)
SILVER = PieceType(5)
KNIGHT = PieceType(6)
PAWN = PieceType(7)

PROOK = PieceType(9)
PBISHOP = PieceType(10)
PLANCE = PieceType(11)
PSILVER = PieceType(13)
PKNIGHT = PieceType(14)
PPAWN = PieceType(15)

from .attack import Attack

from .state.simplestate import SimpleState
