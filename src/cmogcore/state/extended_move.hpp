#ifndef MOG_CORE_STATE_EXTENDED_MOVE_HPP_INCLUDED
#define MOG_CORE_STATE_EXTENDED_MOVE_HPP_INCLUDED

#include "./move.hpp"

namespace mog {
namespace core {
namespace state {

/*
 * ExtendedMove class
 */
struct ExtendedMove : public Move {
  static const int DRAW_GAME = 1;
  static const int PLAYER_WIN = 2;
  static const int PLAYER_LOSE = 3;

  int elapsed_time;  // in seconds
  int move_type;
  int judge;  // 0: game continues, 1: draw, 2: win, 3: lose

  constexpr ExtendedMove(int turn, int from, int to, int piece_type, int elapsed_time = -1, int move_type = 0, int judge = 0)
      : Move(turn, from, to, piece_type), elapsed_time(elapsed_time), move_type(move_type), judge(judge) {}

  constexpr bool is_special() const { return move_type != 0; }

  constexpr bool operator==(ExtendedMove const& rhs) const {
    return turn == rhs.turn && from == rhs.from && to == rhs.to && piece_type == rhs.piece_type && elapsed_time == rhs.elapsed_time &&
           move_type == rhs.move_type && judge == rhs.judge;
  }
};

// lose
struct Resign : public ExtendedMove {
  constexpr Resign(int elapsed_time = -1) : ExtendedMove(0, 0, 0, 0, elapsed_time, 1, ExtendedMove::PLAYER_LOSE) {}
};
struct TimeUp : public ExtendedMove {
  constexpr TimeUp(int elapsed_time = -1) : ExtendedMove(0, 0, 0, 0, elapsed_time, 2, ExtendedMove::PLAYER_LOSE) {}
};
struct IllegalMove : public ExtendedMove {
  constexpr IllegalMove(int elapsed_time = -1) : ExtendedMove(0, 0, 0, 0, elapsed_time, 3, ExtendedMove::PLAYER_LOSE) {}
};
struct PerpetualCheck : public ExtendedMove {
  constexpr PerpetualCheck() : ExtendedMove(0, 0, 0, 0, -1, 4, ExtendedMove::PLAYER_LOSE) {}
};

// win
struct DeclareWin : public ExtendedMove {
  constexpr DeclareWin(int elapsed_time = -1) : ExtendedMove(0, 0, 0, 0, elapsed_time, 5, ExtendedMove::PLAYER_WIN) {}
};

// draw
struct ThreefoldRepetition : public ExtendedMove {
  constexpr ThreefoldRepetition() : ExtendedMove(0, 0, 0, 0, -1, 6, ExtendedMove::DRAW_GAME) {}
};
}
}
}

#endif  // MOG_CORE_STATE_EXTENDED_MOVE_HPP_INCLUDED