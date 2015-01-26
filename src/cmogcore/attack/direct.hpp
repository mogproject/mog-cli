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

      constexpr BitBoard __make_attack_bb_1(int const n, int const index) {
        return make_attack_bb(n / 16, n % 16, pos::get_file(index), pos::get_rank(index));
      }

      constexpr std::array<BitBoard, 81> __make_attack_bb_2(int const n) {
        return util::transform_bind1<81>(__make_attack_bb_1, n);
      }

      constexpr auto bb_table_direct = util::transform<32>(__make_attack_bb_2);
    }
  }
}

#endif  // MOG_CORE_ATTACK_DIRECT_HPP_INCLUDED