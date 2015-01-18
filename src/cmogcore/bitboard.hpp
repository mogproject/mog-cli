#ifndef MOG_CORE_BITBOARD_HPP_INCLUDED
#define MOG_CORE_BITBOARD_HPP_INCLUDED

#include <cassert>
#include "typedef.hpp"
#include "util.hpp"

namespace mog {
  namespace core {
    namespace bitboard {
      struct BitBoard {
        u64 lo, hi;
        constexpr BitBoard(u64 lo = 0ULL, u64 hi = 0ULL): lo(lo), hi(hi) {}

        constexpr bool operator==(BitBoard const& rhs) const {
          return lo == rhs.lo && hi == rhs.hi;
        }
      };

      constexpr bool get(BitBoard const& bb, int index) {
        // assert(0 <= index && index < 81);
        return index < 54 ? (bb.lo >> index) & 1 : (bb.hi >> (index - 54)) & 1;
      }

      constexpr BitBoard set(BitBoard const& bb, int index) {
        // assert(0 <= index && index < 81);
        return BitBoard(
          index < 54 ? (bb.lo | (1ULL << index)) : bb.lo,
          index < 54 ? bb.hi : (bb.hi | 1ULL << (index - 54))
        );
      }

      // TODO: constexpr flip_bb()
    }
  }
}

#endif  // MOG_CORE_BITBOARD_HPP_INCLUDED