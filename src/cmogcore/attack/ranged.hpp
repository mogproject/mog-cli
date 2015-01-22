#ifndef MOG_CORE_ATTACK_RANGED_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_HPP_INCLUDED

#include "../util.hpp"
#include "../bitboard.hpp"

namespace mog {
  namespace core {
    namespace attack {
      //
      // ranged piece types
      //
      constexpr BitBoard attack_bb_lance_black(int const file, int const rank) {
        return BitBoard().set_repeat(file, rank, 0, -1, 8);
      }

      constexpr BitBoard attack_bb_lance_white(int const file, int const rank) {
        return BitBoard().set_repeat(file, rank, 0, 1, 8);
      }

      constexpr BitBoard attack_bb_bishop(int const file, int const rank) {
        return BitBoard()
          .set_repeat(file, rank, -1, -1, 8)
          .set_repeat(file, rank, -1, 1, 8)
          .set_repeat(file, rank, 1, -1, 8)
          .set_repeat(file, rank, 1, 1, 8);
      }

      constexpr BitBoard attack_bb_rook(int const file, int const rank) {
        return BitBoard()
          .set_repeat(file, rank, -1, 0, 8)
          .set_repeat(file, rank, 0, -1, 8)
          .set_repeat(file, rank, 0, 1, 8)
          .set_repeat(file, rank, 1, 0, 8);
      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_HPP_INCLUDED