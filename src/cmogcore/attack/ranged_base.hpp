#ifndef MOG_CORE_ATTACK_RANGED_BASE_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_BASE_HPP_INCLUDED

#include "../util.hpp"
#include "../bitboard.hpp"


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

//          static BitBoard get_attack(BitBoard const& occ) {
//            constexpr auto table = Base::make_table();
//            constexpr auto affected_bb = Base::affected_bb();
//            constexpr auto magic = 0x4040000000000000ULL >> (Base::file - 1);
//            auto bb = occ & affected_bb;
//            return table[((bb.hi * magic) >> 61) | (bb.lo >> (Base::file + 44))];
//          }

         private:
        };
      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_BISHOP_HPP_INCLUDED