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
      namespace ranged {
        typedef BitBoard (*MagicCalculator)(BitBoard const&);

        inline constexpr BitBoard f(BitBoard const& occ) {
          // todo: implement
          return BitBoard();
        }

        inline constexpr MagicCalculator make_attack_bb(int const owner, int const ptype, int const file, int const rank) {
          return &f;
        }

        constexpr MagicCalculator __make_attack_bb_1(int const n, int const index) {
          return make_attack_bb(n >> 4, n & 0xf, pos::get_file(index), pos::get_rank(index));
        }

        constexpr std::array<MagicCalculator, 81> __make_attack_bb_2(int const n) {
          return util::transform<81>(util::bind1st(&__make_attack_bb_1, n));
        }
      }

      constexpr auto bb_table_ranged = util::transform<32>(ranged::__make_attack_bb_2);

    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_HPP_INCLUDED