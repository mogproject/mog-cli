#ifndef MOG_CORE_ATTACK_DIRECT_HPP_INCLUDED
#define MOG_CORE_ATTACK_DIRECT_HPP_INCLUDED

#include <array>
#include "../util.hpp"
#include "../bitboard.hpp"

namespace mog {
  namespace core {
    namespace attack {
      //
      // direct piece types
      //
      namespace direct {
        // attack bitboard for black on position 55
        constexpr BitBoard center_king = BitBoard(0, 0, 0, 0070, 0050, 0070, 0, 0, 0);
        constexpr BitBoard center_gold = BitBoard(0, 0, 0, 0070, 0050, 0020, 0, 0, 0);
        constexpr BitBoard center_silver = BitBoard(0, 0, 0, 0070, 0000, 0050, 0, 0, 0);
        constexpr BitBoard center_knight = BitBoard(0, 0, 0050, 0, 0, 0, 0, 0, 0);
        constexpr BitBoard center_pawn = BitBoard(0, 0, 0, 0020, 0, 0, 0, 0, 0);

        constexpr BitBoard ptype_to_center_bb[] = {
          // king         rook        bishop      lance       gold         silver         knight         pawn
          center_king, BitBoard(), BitBoard(), BitBoard(), center_gold, center_silver, center_knight, center_pawn,
          center_king, BitBoard(), BitBoard(), center_gold, BitBoard(), center_gold, center_gold, center_gold,
        };

        inline constexpr BitBoard make_attack_bb(int const owner, int const ptype, int const file, int const rank) {
          return ptype_to_center_bb[ptype].flip_by_turn(owner).shift_left(file - 5).shift_down(rank - 5);
        }

        constexpr util::array<BitBoard, 81 * 2 * 16> init_bb_table_direct() {
          util::array<BitBoard, 81 * 2 * 16> ret;

          for (int i = 0; i < 81; ++i) for (int t = 0; t < 2; ++t) for (int ptype = 0; ptype < 16; ++ptype) {
            ret[(i << 5) + (t << 4) + ptype] = make_attack_bb(t, ptype, pos::get_file(i), pos::get_rank(i));
          }

          return ret;
        }
      }

      constexpr auto bb_table_direct = direct::init_bb_table_direct();
    }
  }
}

#endif  // MOG_CORE_ATTACK_DIRECT_HPP_INCLUDED