#ifndef MOG_CORE_STATE_SIMPLE_MOVE_HPP_INCLUDED
#define MOG_CORE_STATE_SIMPLE_MOVE_HPP_INCLUDED

namespace mog {
namespace core {
namespace state {
/*
 * SimpleMove class
 */
struct SimpleMove {
  int turn;
  int from;
  int to;
  int piece_type;  // piece type after the move

  constexpr SimpleMove(int turn, int from, int to, int piece_type) : turn(turn), from(from), to(to), piece_type(piece_type) {}

  constexpr bool operator==(SimpleMove const& rhs) const {
    return turn == rhs.turn && from == rhs.from && to == rhs.to && piece_type == rhs.piece_type;
  }
};
}
}
}

#endif  // MOG_CORE_STATE_SIMPLE_MOVE_HPP_INCLUDED