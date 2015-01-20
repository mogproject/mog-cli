#ifndef MOG_CORE_BITBOARD_HPP_INCLUDED
#define MOG_CORE_BITBOARD_HPP_INCLUDED

#include <iostream>
#include <sstream>
#include <iomanip>
#include "typedef.hpp"
#include "util.hpp"

namespace mog {
  namespace core {
    /**
     * Immutable bitboard structure
     */
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
      constexpr BitBoard operator|(BitBoard const& rhs) const { return BitBoard(lo | rhs.lo, hi | rhs.hi); }
      constexpr BitBoard operator^(BitBoard const& rhs) const { return BitBoard(lo ^ rhs.lo, hi ^ rhs.hi); }
      constexpr BitBoard operator~() const { return BitBoard(~lo, ~hi); }

      constexpr bool get(int const index) const {
        return (rshift(lo, index) | rshift(hi, index - 54)) & 1ULL;
      }

      constexpr bool get(int const file, int const rank) const { return get(pos::make_pos(file, rank)); }

      constexpr BitBoard set(int const index) const {
        return BitBoard(lo | lshift(1ULL, index), hi | lshift(1ULL, index - 54));
      }

      constexpr BitBoard set(int const file, int const rank) const { return set(pos::make_pos(file, rank)); }

      constexpr BitBoard reset(int const index) const {
        return BitBoard(lo & ~lshift(1ULL, index), hi & ~lshift(1ULL, index - 54));
      }

      constexpr BitBoard reset(int const file, int const rank) const { return reset(pos::make_pos(file, rank)); }

      /**
       * Shift all bits to down.
       * @param n shift width
       *
       *          e.g. n=2
       *          *********       ---------
       *          -*-----*-       ---------
       *          *--***-**       *********
       *          ------*--       -*-----*-
       *          -*-------   =>  *--***-**
       *          --*----*-       ------*--
       *          *******-*       -*-------
       *          -------*-       --*----*-
       *          *********       *******-*
       */
      constexpr BitBoard shift_down(int const n) const {
        return BitBoard(lshift(lo, n * 9) | lshift(hi, (n + 6) * 9), lshift(hi, n * 9) | lshift(lo, (n - 6) * 9));
      }
      /**
       * Shift all bits to up.
       * @param n shift width
       *
       *          e.g. n=2
       *          *********       *--***-**
       *          -*-----*-       ------*--
       *          *--***-**       -*-------
       *          ------*--       --*----*-
       *          -*-------   =>  *******-*
       *          --*----*-       -------*-
       *          *******-*       *********
       *          -------*-       ---------
       *          *********       ---------
       */
      constexpr BitBoard shift_up(int const n) const { return -9 < n && n < 9 ? shift_down(-n) : BitBoard(); }

      // TODO: implement shiftRight, shiftDown, flipHorizontal, flipVertical, spreadAllFile
    };

    namespace bitboard {
      //
      // constant expressions
      //

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
          if (i == 2 || i == 5) s << ',';
          if (i % 3 != 2) s << '.';
        }
        s << ")";
        return s.str();
      }

    }
  }
}

#endif  // MOG_CORE_BITBOARD_HPP_INCLUDED
