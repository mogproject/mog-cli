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
          u64 mapping = 0xffffffffffffffffULL;

          /**
           * Calculate index of the attack table from occupancy bitboard. (general model)
           *
           * @param bb effected bitboard
           */
          inline constexpr int get_index(BitBoard const& bb = bitboard::EMPTY) const {
            return (
              (rshift(bb.lo * magic_lo, shift_lo)) |
              (rshift(bb.hi * magic_hi, shift_hi))
            ) >> shift_final;
          }

          inline constexpr int get_mapping(int pos) const {
            return (mapping >> (pos * 4)) & 0xf;
          }

          /** Convert ordered bits to magic mask */
          constexpr int convert_mapping(int ordered_bits) const {
            int ret = 0;
            for (int i = 0; i < 16; ++i) {
              int k = get_mapping(i);
              if (k == 0xf) break;
              ret |= ((ordered_bits >> i) & 1) << k;
            }
            return ret;
          }
        };

      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_MAGIC_HPP_INCLUDED
