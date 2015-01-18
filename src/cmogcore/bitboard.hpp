#ifndef MOG_CORE_BITBOARD_HPP_INCLUDED
#define MOG_CORE_BITBOARD_HPP_INCLUDED

#include <cassert>
#include "typedef.hpp"
#include "util.hpp"

namespace mog {
  namespace core {
    class BitBoard {
     public:
      u64 x[2];

      BitBoard() {
        x[0] = x[1] = 0ULL;
      }

      BitBoard(u64 lo, u64 hi) {
        x[0] = lo & MASK54;
        x[1] = hi & MASK27;
      }

      BitBoard(BitBoard const& obj) {
        x[0] = obj.x[0];
        x[1] = obj.x[1];
      }

      bool operator==(BitBoard const& rhs) const {
        return x[0] == rhs.x[0] && x[1] == rhs.x[1];
      }

      bool get(int index) const {
        assert(0 <= index && index < 81);
        return (x[index / 54] >> (index % 54)) & 1;
      }

      BitBoard set(int index) {
        assert(0 <= index && index < 81);
        x[index / 54] |= 1LL << (index % 54);
        return *this;
      }
    };

    // TODO: constexpr flip_bb()
  }
}

#endif  // MOG_CORE_BITBOARD_HPP_INCLUDED