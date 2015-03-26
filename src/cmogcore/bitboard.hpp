#ifndef MOG_CORE_BITBOARD_HPP_INCLUDED
#define MOG_CORE_BITBOARD_HPP_INCLUDED

#include <iostream>
#include <sstream>
#include <iomanip>
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

      constexpr BitBoard set_repeat(int const file_origin, int const rank_origin,
                                    int const file_offset, int const rank_offset, int const length) const {
        return length <= 0 || file_origin < 1 || 9 < file_origin || rank_origin < 1 || 9 < rank_origin
          ? *this
          : set(file_origin + file_offset, rank_origin + rank_offset)
              .set_repeat(file_origin + file_offset, rank_origin + rank_offset, file_offset, rank_offset, length - 1);
      }

      /**
       * Count number of 1-bits
       */
      constexpr int count() const {
        return pop_ct(lo) + pop_ct(hi);
      }

      /**
       * Make u64 value spreading file bits to each rank
       *
       * e.g.
       *   n       * 01001001001001001
       * abcdefghi      abcdefghi
       * ---------      abcdefghi
       * ---------  =>  abcdefghi
       * ---------      abcdefghi
       * ---------      abcdefghi
       * ---------      abcdefghi
       */
      inline static constexpr u64 files(int n) { return 0001001001001001001ULL * n; }

      /**
       * Make u64 value spreading rank bits to each file
       *
       * e.g.
       *   n       * 0x101010101010 & 01001001001001001 * 0777
       * ---abcdef      f--abcdef      --------f      fffffffff
       * ---------      ef--abcde      --------e      eeeeeeeee
       * ---------  =>  def--abcd  =>  --------d  =>  ddddddddd
       * ---------      cdef--abc      --------c      ccccccccc
       * ---------      bcdef--ab      --------b      bbbbbbbbb
       * ---------      --------a      --------a      aaaaaaaaa
       */
      inline static constexpr u64 ranks(int n) { return ((0x10101010101ULL * n) & 0001001001001001001ULL) * 0777; }

      /**
       * Shift all bits to left.
       * @param n shift width
       *
       * e.g. n=2
       * *********      *******--
       * -*-----*-      -----*---
       * *--***-**      -***-**--
       * ------*--      ----*----
       * -*-------  =>  ---------
       * --*----*-      *----*---
       * *******-*      *****-*--
       * -------*-      -----*---
       * *********      *******--
       */
      constexpr BitBoard shift_left(int const n) const { return _shift_left(0, n); }

      constexpr BitBoard _shift_left(int step, int n, u64 x = 0) const {
        return step == 0
          ? _shift_left(1, n, files(rshift(0777, n) & 0777))
          : BitBoard(lshift(lo & x, n), lshift(hi & x, n));
      }

      /**
       * Shift all bits to right.
       * @param n shift width
       *
       * e.g. n=2
       * *********      --*******
       * -*-----*-      ---*-----
       * *--***-**      --*--***-
       * ------*--      --------*
       * -*-------  =>  ---*-----
       * --*----*-      ----*----
       * *******-*      --*******
       * -------*-      ---------
       * *********      --*******
       */
      constexpr BitBoard shift_right(int const n) const { return -9 < n && n < 9 ? shift_left(-n) : BitBoard(); }

      /**
       * Shift all bits to down.
       * @param n shift width
       *
       * e.g. n=2
       * *********      ---------
       * -*-----*-      ---------
       * *--***-**      *********
       * ------*--      -*-----*-
       * -*-------  =>  *--***-**
       * --*----*-      ------*--
       * *******-*      -*-------
       * -------*-      --*----*-
       * *********      *******-*
       */
      constexpr BitBoard shift_down(int const n) const {
        return BitBoard(lshift(lo, n * 9) | lshift(hi, (n + 6) * 9), lshift(hi, n * 9) | lshift(lo, (n - 6) * 9));
      }

      /**
       * Shift all bits to up.
       * @param n shift width
       *
       *  e.g. n=2
       *  *********      *--***-**
       *  -*-----*-      ------*--
       *  *--***-**      -*-------
       *  ------*--      --*----*-
       *  -*-------  =>  *******-*
       *  --*----*-      -------*-
       *  *******-*      *********
       *  -------*-      ---------
       *  *********      ---------
       */
      constexpr BitBoard shift_up(int const n) const { return -9 < n && n < 9 ? shift_down(-n) : BitBoard(); }

      /**
       * Flip a bitboard vertically about the centre rank.
       * Rank 1 is mapped to rank 9 and vice versa.
       *
       * e.g.
       * *********      *********
       * -*-----*-      -------*-
       * *--***-**      *******-*
       * ------*--      --*----*-
       * -*-------  =>  -*-------
       * --*----*-      ------*--
       * *******-*      *--***-**
       * -------*-      -*-----*-
       * *********      *********
       */
      constexpr BitBoard flip_vertical() const { return _flip_vertical(0); }

      constexpr BitBoard _flip_vertical(int step, u64 x = 0ULL) const {
        return step == 0  // x := rank 654321 -> 4__1__ + _5__2_ + __6__3 = 456123
          ? _flip_vertical(1, ((lo & ranks(011)) << 18) + (lo & ranks(022)) + ((lo >> 18) & ranks(011)))
          // lo: (987 -> ____9 + ___8_ + 987__ = 98789 -> 789) + 456___ = 456789, hi: 123
          : BitBoard(((hi & ranks(001)) << 18) + (hi & ranks(002)) + (hi >> 18) + (x & ranks(070)), x);
      }

      /**
       * Flip a bitboard horizontally about the center file.
       * File 1 is mapped to file 9 and vice versa.
       *
       * e.g.
       * *********      *********
       * -*-----*-      -*-----*-
       * *--***-**      **-***--*
       * ------*--      --*------
       * -*-------  =>  -------*-
       * --*----*-      -*----*--
       * *******-*      *-*******
       * -------*-      -*-------
       * *********      *********
       */
      constexpr BitBoard flip_horizontal() const { return BitBoard(_flip_horizontal(0, lo), _flip_horizontal(0, hi)); }

      constexpr u64 _flip_horizontal(int step, u64 x, u64 y = 0ULL) const {
        return step == 0  // y := file 987654321 -> _9_7__4_2 + 8_6__3_1_ = 8967_3412
          ? _flip_horizontal(1, x, ((x & files(0512)) >> 1) + ((x & files(0245)) << 1))
          : step == 1  // file (8967_3412 -> __89__34) + (8967_3412 -> 67___12) = 6789_1234
            ? _flip_horizontal(2, x, ((y & files(0614)) >> 2) + ((y & files(0143)) << 2))
            // file (6789_1234 -> _____6789) + ____5____ + (6789_1234 -> 1234_____) = 123456789
            : ((y & files(0740)) >> 5) + (x & files(0020)) + ((y & files(0017)) << 5);
      }

      /**
       * Spread each bit to all file-direction.
       *
       * IMPORTANT: This method is assuming that there are no two or more bits in same file.
       *
       * e.g.
       * ---------      ****-*--*
       * ---------      ****-*--*
       * ---------      ****-*--*
       * ---------      ****-*--*
       * ---*-----  =>  ****-*--*
       * *-*--*--*      ****-*--*
       * -*-------      ****-*--*
       * ---------      ****-*--*
       * ---------      ****-*--*
       */
      constexpr BitBoard spread_all_file() const {
        return _spread_all_file(files((((lo | hi) * 02002002002002002000ULL) >> 55) & 0777ULL));
      }

      // TODO: rename(refactor) to be nicer
      constexpr BitBoard _spread_all_file(u64 x) const {
        return BitBoard(x, x);
      }

      /** Flip vertical if the turn is white */
      constexpr BitBoard flip_by_turn(int turn) const {
        return turn ? flip_vertical() : *this;
      }
    };

    namespace bitboard {
      /** Empty and full */
      static constexpr BitBoard EMPTY = BitBoard();
      static constexpr BitBoard FULL = BitBoard(0777, 0777, 0777, 0777, 0777, 0777, 0777, 0777, 0777);

      /** Identity with a single bit */
      constexpr BitBoard ident(int index) {
        return BitBoard(lshift(1ULL, index), lshift(1ULL, index - 54));
      }

      /** Ranks */
      static constexpr BitBoard rank1 = BitBoard(0777, 0, 0, 0, 0, 0, 0, 0, 0);
      static constexpr BitBoard rank2 = BitBoard(0, 0777, 0, 0, 0, 0, 0, 0, 0);
      static constexpr BitBoard rank3 = BitBoard(0, 0, 0777, 0, 0, 0, 0, 0, 0);
      static constexpr BitBoard rank4 = BitBoard(0, 0, 0, 0777, 0, 0, 0, 0, 0);
      static constexpr BitBoard rank5 = BitBoard(0, 0, 0, 0, 0777, 0, 0, 0, 0);
      static constexpr BitBoard rank6 = BitBoard(0, 0, 0, 0, 0, 0777, 0, 0, 0);
      static constexpr BitBoard rank7 = BitBoard(0, 0, 0, 0, 0, 0, 0777, 0, 0);
      static constexpr BitBoard rank8 = BitBoard(0, 0, 0, 0, 0, 0, 0, 0777, 0);
      static constexpr BitBoard rank9 = BitBoard(0, 0, 0, 0, 0, 0, 0, 0, 0777);

      /** Files */
      static constexpr BitBoard file1 = BitBoard(0001, 0001, 0001, 0001, 0001, 0001, 0001, 0001, 0001);
      static constexpr BitBoard file2 = BitBoard(0002, 0002, 0002, 0002, 0002, 0002, 0002, 0002, 0002);
      static constexpr BitBoard file3 = BitBoard(0004, 0004, 0004, 0004, 0004, 0004, 0004, 0004, 0004);
      static constexpr BitBoard file4 = BitBoard(0010, 0010, 0010, 0010, 0010, 0010, 0010, 0010, 0010);
      static constexpr BitBoard file5 = BitBoard(0020, 0020, 0020, 0020, 0020, 0020, 0020, 0020, 0020);
      static constexpr BitBoard file6 = BitBoard(0040, 0040, 0040, 0040, 0040, 0040, 0040, 0040, 0040);
      static constexpr BitBoard file7 = BitBoard(0100, 0100, 0100, 0100, 0100, 0100, 0100, 0100, 0100);
      static constexpr BitBoard file8 = BitBoard(0200, 0200, 0200, 0200, 0200, 0200, 0200, 0200, 0200);
      static constexpr BitBoard file9 = BitBoard(0400, 0400, 0400, 0400, 0400, 0400, 0400, 0400, 0400);

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
