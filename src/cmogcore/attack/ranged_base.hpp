#ifndef MOG_CORE_ATTACK_RANGED_BASE_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_BASE_HPP_INCLUDED

#include "../util.hpp"
#include "../bitboard.hpp"
#include "ranged_magic.hpp"


namespace mog {
  namespace core {
    namespace attack {
      namespace ranged {
        /**
         * Base class for ranged piece types
         *
         * @tparam MagicType 0: black lance, 1: white lance, 2: bishop or promoted bishop, 3: rook or promoted rook
         */
        template <int Index, int MagicType>
        class RangedBase {
         public:
          /** File and rank (1-indexed) */
          static constexpr auto file = pos::get_file(Index);
          static constexpr auto rank = pos::get_rank(Index);

          /** Affected mask bitboard */
          static constexpr auto affected_mask = ~(
              ((rank != 1) ? bitboard::rank1 : bitboard::EMPTY) |
              ((rank != 9) ? bitboard::rank9 : bitboard::EMPTY) |
              ((file != 1) ? bitboard::file1 : bitboard::EMPTY) |
              ((file != 9) ? bitboard::file9 : bitboard::EMPTY));

         private:
          /** Generate directions. */
          static constexpr util::Array<std::pair<int, int>, 4> get_directions() {
            switch (MagicType) {
              case 0: return {{ {0, -1} }}; break;
              case 1: return {{ {0, 1} }}; break;
              case 2: return {{ {-1, -1}, {-1, 1}, {1, -1}, {1, 1} }}; break;
              case 3: return {{ {0, -1}, {-1, 0}, {0, 1}, {1, 0} }}; break;
            }
          }

          /** max attack bitboard */
          static constexpr BitBoard get_max_attack() {
            auto bb = BitBoard();
            for (auto d: directions) {
              bb = bb.set_repeat(file, rank, d.first, d.second, 8);
            }
            return bb;
          }

         public:
          /** directions */
          static constexpr auto directions = get_directions();

          /** Make affected bitboard */
          static constexpr auto affected_bb = get_max_attack() & affected_mask;

          /** size of the variation table */
          static constexpr int variation_size = 1 << affected_bb.count();

        };
      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_BISHOP_HPP_INCLUDED