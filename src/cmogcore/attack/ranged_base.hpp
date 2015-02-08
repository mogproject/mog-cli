#ifndef MOG_CORE_ATTACK_RANGED_BASE_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_BASE_HPP_INCLUDED

#include "../util.hpp"
#include "../bitboard.hpp"
#include "ranged_magic.hpp"


namespace mog {
  namespace core {
    namespace attack {
      namespace ranged {
        //
        // Base class
        //
        template <int Index>
        class RangedBase {
         public:
          /** File and rank (1-indexed) */
          static constexpr auto file = pos::get_file(Index);
          static constexpr auto rank = pos::get_rank(Index);

          /** Affected mask bitboard */
          static constexpr auto affected_mask() {
            return ~(
              ((rank != 1) ? bitboard::rank1 : bitboard::EMPTY) |
              ((rank != 9) ? bitboard::rank9 : bitboard::EMPTY) |
              ((file != 1) ? bitboard::file1 : bitboard::EMPTY) |
              ((file != 9) ? bitboard::file9 : bitboard::EMPTY));
          }

         private:
        };
      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_BISHOP_HPP_INCLUDED