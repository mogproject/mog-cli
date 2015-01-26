#ifndef MOG_CORE_ATTACK_AERIAL_HPP_INCLUDED
#define MOG_CORE_ATTACK_AERIAL_HPP_INCLUDED

#include <array>
#include "../util.hpp"
#include "../bitboard.hpp"

namespace mog {
  namespace core {
    namespace attack {
      //
      // aerial attacks
      //
      namespace aerial {
        constexpr auto rank1 = BitBoard(0777ULL, 0ULL);
        constexpr auto rank12 = BitBoard(0777777ULL, 0ULL);
        constexpr auto empty = BitBoard(0ULL, 0ULL);
        constexpr auto full = BitBoard(0xffffffffffffffffULL, 0xffffffffffffffffULL);

        constexpr BitBoard bb_table_aerial_mask[] = {
          // king rook bishop lance  gold   silver knight  pawn
          full, empty, empty, rank1, empty, empty, rank12, rank1,
          full, full,  full,  full,  full,  full,  full,   full,
        };

        inline constexpr BitBoard make_attack_bb(int const owner, int const ptype) {
          return ~bb_table_aerial_mask[ptype].flip_by_turn(owner);
        }

        constexpr BitBoard __make_attack_bb(int const n) {
          return make_attack_bb(n >> 4, n & 0xf);
        }
      }
      constexpr auto bb_table_aerial = util::transform<32>(aerial::__make_attack_bb);
    }
  }
}

#endif  // MOG_CORE_ATTACK_AERIAL_HPP_INCLUDED