#ifndef MOG_CORE_ATTACK_HPP_INCLUDED
#define MOG_CORE_ATTACK_HPP_INCLUDED

#include "typedef.hpp"
#include "util.hpp"
#include "bitboard.hpp"

namespace mog {
  namespace core {
    class Attack {
     public:
      BitBoard get_attack(int owner, BitBoard const& my_pawn_occ);  // pawn from hand
      BitBoard get_attack(int owner, int ptype, BitBoard const& occ);  // from hand except pawn
      BitBoard get_attack(int owner, int ptype, int index);  // direct pieces on board
      BitBoard get_attack(int owner, int ptype, int index, BitBoard const& occ);  // ranged pieces on board

      // max_attack[Turn][PieceType][Pos]
      static BitBoard attack_bb[2][16][81];
    };

    namespace attack {
      constexpr BitBoard set_direction(BitBoard const& bb, int const file, int const rank, int const file_offset,
                                       int const rank_offset, int const max_distance) {
        return max_distance > 0
                 ? set_direction(bb.set(file + file_offset, rank + rank_offset),
                   file + file_offset, rank + rank_offset, file_offset, rank_offset, max_distance - 1)
                 : bb;
      }



      constexpr BitBoard attack_bb_king(int const file, int const rank) {
        return BitBoard()
          .set(file - 1, rank - 1).set(file, rank - 1).set(file + 1, rank - 1)
          .set(file - 1, rank).set(file + 1, rank)
          .set(file - 1, rank + 1).set(file, rank + 1).set(file + 1, rank + 1);
      }

      constexpr BitBoard attack_bb_gold(int const file, int const rank) {
        return BitBoard()
          .set(file - 1, rank - 1).set(file, rank - 1).set(file + 1, rank - 1)
          .set(file - 1, rank).set(file + 1, rank)
          .set(file, rank + 1);
      }

      constexpr BitBoard attack_bb_silver(int const file, int const rank) {
        return BitBoard()
          .set(file - 1, rank - 1).set(file, rank - 1).set(file + 1, rank - 1)
          .set(file - 1, rank + 1).set(file + 1, rank + 1);
      }

      constexpr BitBoard attack_bb_knight(int const file, int const rank) {
        return BitBoard().set(file - 1, rank - 2).set(file + 1, rank - 2);
      }

      constexpr BitBoard attack_bb_pawn(int const file, int const rank) {
        return BitBoard().set(file - 1, rank);
      }

      constexpr BitBoard xxx = attack_bb_gold(5, 5);
    }
  }
}

#endif  // MOG_CORE_ATTACK_HPP_INCLUDED