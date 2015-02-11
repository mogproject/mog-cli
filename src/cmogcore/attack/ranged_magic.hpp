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
          u64 magic_lo_2 = 0ULL;  // use for rook
          int shift_lo_2 = 0;  // use for rook

          /**
           * Calculate index of the attack table from occupancy bitboard. (general model)
           *
           * @param bb effected bitboard
           */
          inline constexpr int get_index(BitBoard const& bb = bitboard::EMPTY) const {
            return (
              (rshift(bb.lo * magic_lo, shift_lo)) |
              (rshift(bb.lo * magic_lo_2, shift_lo_2)) |
              (rshift(bb.hi * magic_hi, shift_hi))
            ) >> shift_final;
          }

          constexpr int get_mapping(int pos) const {
            return (mapping >> (pos * 4)) & 0xf;
          }
        };

      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_MAGIC_HPP_INCLUDED