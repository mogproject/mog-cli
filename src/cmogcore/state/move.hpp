#ifndef MOG_CORE_STATE_MOVE_HPP_INCLUDED
#define MOG_CORE_STATE_MOVE_HPP_INCLUDED

#include "./simple_move.hpp"

namespace mog {
namespace core {
namespace state {

/*
 * Move class
 */
struct Move : public SimpleMove {
  static const int DRAW_GAME = 1;
  static const int PLAYER_WIN = 2;
  static const int PLAYER_LOSE = 3;

  int elapsed_time;  // in seconds
  int move_type;
  int judge;  // 0: game continues, 1: draw, 2: win, 3: lose

  constexpr Move(int turn, int from, int to, int piece_type, int elapsed_time = -1, int move_type = 0, int judge = 0)
      : SimpleMove(turn, from, to, piece_type), elapsed_time(elapsed_time), move_type(move_type), judge(judge) {}

  constexpr bool is_special() const { return move_type != 0; }

  constexpr bool operator==(Move const& rhs) const {
    return turn == rhs.turn && from == rhs.from && to == rhs.to && piece_type == rhs.piece_type && elapsed_time == rhs.elapsed_time &&
           move_type == rhs.move_type && judge == rhs.judge;
  }
};

// lose
struct Resign : public Move {
  constexpr Resign(int elapsed_time = -1) : Move(0, 0, 0, 0, elapsed_time, 1, Move::PLAYER_LOSE) {}
};
struct TimeUp : public Move {
  constexpr TimeUp(int elapsed_time = -1) : Move(0, 0, 0, 0, elapsed_time, 2, Move::PLAYER_LOSE) {}
};
struct IllegalMove : public Move {
  constexpr IllegalMove(int elapsed_time = -1) : Move(0, 0, 0, 0, elapsed_time, 3, Move::PLAYER_LOSE) {}
};
struct PerpetualCheck : public Move {
  constexpr PerpetualCheck() : Move(0, 0, 0, 0, -1, 4, Move::PLAYER_LOSE) {}
};

// win
struct DeclareWin : public Move {
  constexpr DeclareWin(int elapsed_time = -1) : Move(0, 0, 0, 0, elapsed_time, 5, Move::PLAYER_WIN) {}
};

// draw
struct ThreefoldRepetition : public Move {
  constexpr ThreefoldRepetition() : Move(0, 0, 0, 0, -1, 6, Move::DRAW_GAME) {}
};
}
}
}

#endif  // MOG_CORE_STATE_MOVE_HPP_INCLUDED