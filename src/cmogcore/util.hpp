#ifndef MOG_CORE_UTIL_HPP_INCLUDED
#define MOG_CORE_UTIL_HPP_INCLUDED

#include <cassert>

namespace mog {
  namespace core {
    u64 const MASK27 = 0x0000000007ffffffULL;
    u64 const MASK54 = 0x003fffffffffffffULL;

    // Universal shift functions
    constexpr inline u64 lshift(u64 const u, int const n) { return -64 < n && n < 64 ? n < 0 ? u >> -n : u << n : 0ULL; }
    constexpr inline u64 rshift(u64 const u, int const n) { return -64 < n && n < 64 ? n < 0 ? u << -n : u >> n : 0ULL; }

    // Turn
    namespace turn {
      int const BLACK = 0;
      int const WHITE = -1;
    }

    // Piece Type
    namespace ptype {
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

      constexpr inline int make_pos(int const file, int const rank) {
//        assert(1 <= file && file <=9 && 1 <= rank && rank <= 9);
        return rank * 9 + file - 10;
      }
    }
  }
}

#endif  // #ifndef MOG_CORE_UTIL_HPP_INCLUDED
