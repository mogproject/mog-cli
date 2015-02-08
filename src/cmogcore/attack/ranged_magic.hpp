#ifndef MOG_CORE_ATTACK_RANGED_MAGIC_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_MAGIC_HPP_INCLUDED

#include "../util.hpp"
#include "../bitboard.hpp"


namespace mog {
  namespace core {
    namespace attack {
      namespace ranged {
        //
        // Calculate magic number for ranged attack
        //
        struct Magic {
          u64 magic_lo;
          int shift_lo;
          u64 magic_hi;
          int shift_hi;
          int shift_final;
          u64 mapping = 0ULL;
          u64 magic_lo_left = 0ULL;  // use for rook
          int shift_lo_left = 0;  // use for rook

          /**
           * Calculate index of the attack table from occupancy bitboard. (general model)
           *
           * @param bb effected bitboard
           */
          inline constexpr int get_index(BitBoard const& bb = bitboard::EMPTY) const {
            return (
              ((bb.lo * magic_lo) >> shift_lo) |
              ((bb.hi * magic_hi) >> shift_hi) |
              ((bb.lo * magic_lo_left) << shift_lo_left)
            ) >> shift_final;
          }
        };

      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_MAGIC_HPP_INCLUDED