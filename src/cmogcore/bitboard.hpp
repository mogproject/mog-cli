#ifndef MOG_CORE_BITBOARD_HPP_INCLUDED
#define MOG_CORE_BITBOARD_HPP_INCLUDED

#include <iostream>
#include <sstream>
#include <iomanip>
#include "typedef.hpp"
#include "util.hpp"

namespace mog {
  namespace core {
    struct BitBoard {
      u64 lo, hi;

      /** constructor by two u64s */
      constexpr BitBoard(u64 lo = 0ULL, u64 hi = 0ULL): lo(lo & MASK54), hi(hi & MASK27) {}

      /** rank-wise constructor */
      constexpr BitBoard(int r1, int r2, int r3, int r4, int r5, int r6, int r7, int r8, int r9)
        : lo(((u64)r1 + ((u64)r2 << 9) + ((u64)r3 << 18) + ((u64)r4 << 27) + ((u64)r5 << 36) + ((u64)r6 << 45)) & MASK54),
          hi(((u64)r7 + ((u64)r8 << 9) + ((u64)r9 << 18)) & MASK27) {}

      constexpr bool operator==(BitBoard const& rhs) const { return lo == rhs.lo && hi == rhs.hi; }
      constexpr BitBoard operator&(BitBoard const& rhs) const { return BitBoard(lo & rhs.lo, hi & rhs.hi); }
      constexpr BitBoard operator|(BitBoard const& rhs) const { return BitBoard(lo ^ rhs.lo, hi ^ rhs.hi); }
      constexpr BitBoard operator^(BitBoard const& rhs) const { return BitBoard(lo | rhs.lo, hi | rhs.hi); }

      constexpr BitBoard set(int const index) const {
        return (0 <= index && index < 81)
          ? BitBoard(
            index < 54 ? (lo | (1ULL << index)) : lo,
            index < 54 ? hi : (hi | 1ULL << (index - 54)))
          : *this;
      }

      constexpr BitBoard set(int const file, int const rank) const {
        return (1 <= file && file <= 9 && 1 <= rank && rank <= 9) ? set(pos::make_pos(file, rank)) : *this;
      }


      // TODO: implement unary_~, reset, shiftUp, shiftDown, shiftRight, shiftDown, flipHorizontal, flipVertical, spreadAllFile
    };

    namespace bitboard {
      //
      // constant expressions
      //
      constexpr bool get(BitBoard const& bb, int const index) {
        return 0 <= index && index < 81 && (index < 54 ? (bb.lo >> index) & 1ULL : (bb.hi >> (index - 54)) & 1ULL);
      }

      constexpr bool get(BitBoard const& bb, int const file, int const rank) {
        return 1 <= file && file <= 9 && 1 <= rank && rank <= 9 && get(bb, pos::make_pos(file, rank));
      }

      //
      // non-constant expressions
      //

      /** represent as nine octets */
      std::string repr(BitBoard const& bb) {
        std::ostringstream s;
        s << "BitBoard(";
        for (auto i = 0; i < 9; ++i) {
          auto x = ((i < 6 ? bb.lo : bb.hi) >> (i % 6 * 9)) & 0x1ffULL;
          s << std::setfill('0') << std::setw(3) << std::oct << x;
          if (i != 8) s << '.';
        }
        s << ")";
        return s.str();
      }

    }
  }
}

#endif  // MOG_CORE_BITBOARD_HPP_INCLUDED