#ifndef MOG_CORE_UTIL_HPP_INCLUDED
#define MOG_CORE_UTIL_HPP_INCLUDED

#include "util/array.hpp"

namespace mog {
  namespace core {
    typedef signed long long s64;
    typedef unsigned long long u64;

    u64 const MASK27 = 0000000000777777777ULL;
    u64 const MASK54 = 0777777777777777777ULL;

    // Universal shift functions
    inline constexpr u64 lshift(u64 const u, int const n) { return -64 < n && n < 64 ? n < 0 ? u >> -n : u << n : 0ULL; }
    inline constexpr u64 rshift(u64 const u, int const n) { return -64 < n && n < 64 ? n < 0 ? u << -n : u >> n : 0ULL; }

    // Number of Trailing Zeros
    // todo: to be more efficient
    inline constexpr int ntz(u64 n, int sofar = 0) {
      return n == 0 ? 64 : (n & 1ULL) ? sofar : ntz(n >> 1, sofar + 1);
    }

    // Number of Leading Zeros
    // todo: to be more efficient
    inline constexpr int nlz(u64 n, int sofar = 0) {
      return n == 0 ? 64 : (n & 0x8000000000000000ULL) ? sofar : nlz(n << 1, sofar + 1);
    }

    // Count number of 1-bits (compile time)
    inline constexpr int pop_ct(u64 x) {
      x = x - ( ( x >> 1 ) & 0x5555555555555555ULL );
      x = ( x & 0x3333333333333333ULL ) + ( ( x >> 2 ) & 0x3333333333333333ULL );
      x = ( x + ( x >> 4 ) ) & 0x0f0f0f0f0f0f0f0fULL;
      x = x + ( x >> 8 );
      x = x + ( x >> 16 );
      x = x + ( x >> 32 );
      return x & 0x000000000000007f;
    }

    // Most Significant Bit (in compile time)
    //     If n is 0, return -1.
    inline constexpr int msb_ct(u64 n) { return 63 - nlz(n); }

//    inline int msb(unsigned long n) {
//      int msb = 0;
//      asm("bsrl %1,%0" : "=r"(msb) : "r"(n));
//      return msb;
//    }

    namespace util {
      template <typename T>
      inline constexpr T min(T const& a, T const& b) { return a < b ? a : b; }

      template <typename T>
      inline constexpr T max(T const& a, T const& b) { return a < b ? b : a; }
    }

    // Turn
    namespace turn {
//      template <int N>
//      struct Turn { static int const value = N; };
//
//      struct Black: Turn<0> {};
//      struct White: Turn<1> {};

      int const BLACK = 0;
      int const WHITE = 1;
    }

    // Piece Type
    namespace ptype {
      template <int N>
      struct PType {
        static constexpr int value = N;

        static constexpr bool is_promoted = N >> 3;
      };

      struct King: PType<0> {};
      struct Rook: PType<1> {};
      struct Bishop: PType<2> {};
      struct Lance: PType<3> {};
      struct Gold: PType<4> {};
      struct Silver: PType<5> {};
      struct Knight: PType<6> {};
      struct Pawn: PType<7> {};

      int const KING = 0;
      int const ROOK = 1;
      int const BISHOP = 2;
      int const LANCE = 3;
      int const GOLD = 4;
      int const SILVER = 5;
      int const KNIGHT = 6;
      int const PAWN = 7;
    }

    // Position
    namespace pos {
      int const UNUSED = -2;
      int const HAND = -1;

      inline constexpr int make_pos(int const file, int const rank) {
        return (1 <= file && file <= 9 && 1 <= rank && rank <= 9) ? rank * 9 + file - 10 : -1;
      }

      inline constexpr int get_file(int const index) { return index % 9 + 1; }
      inline constexpr int get_rank(int const index) { return index / 9 + 1; }
    }
  }
}

#endif  // #ifndef MOG_CORE_UTIL_HPP_INCLUDED
