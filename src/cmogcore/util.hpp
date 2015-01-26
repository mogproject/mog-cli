#ifndef MOG_CORE_UTIL_HPP_INCLUDED
#define MOG_CORE_UTIL_HPP_INCLUDED

#include "util/transform.hpp"

namespace mog {
  namespace core {
    typedef signed long long s64;
    typedef unsigned long long u64;

    u64 const MASK27 = 0000000000777777777ULL;
    u64 const MASK54 = 0777777777777777777ULL;

    // Universal shift functions
    inline constexpr u64 lshift(u64 const u, int const n) { return -64 < n && n < 64 ? n < 0 ? u >> -n : u << n : 0ULL; }
    inline constexpr u64 rshift(u64 const u, int const n) { return -64 < n && n < 64 ? n < 0 ? u << -n : u >> n : 0ULL; }

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
      struct PType { static int const value = N; };

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
