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

         private:
        };
      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_BISHOP_HPP_INCLUDED