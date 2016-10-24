#ifndef MOG_CORE_GAME_HPP_INCLUDED
#define MOG_CORE_GAME_HPP_INCLUDED

#include <map>
#include "./state/extended_state.hpp"
#include "./state/extended_move.hpp"

namespace mog {
namespace core {

/*
 * Game class
 */
struct Game {
 public:
  typedef std::vector<state::ExtendedState> StateList;
  typedef std::vector<state::ExtendedMove> MoveList;

  StateList states;
  MoveList moves;

  Game(state::State const& initial_state) {
    auto s = state::ExtendedState(initial_state);
    states.push_back(s);
    ++__repetitions[s.hash_value];
  }

  /*
   * @return 0: game continues, 1: draw, 2: win, 3: lose
   */
  int move(state::ExtendedMove const& move) {
    if (is_finished()) {
      throw RuntimeError("The game is already finished.");
    }

    // special moves
    if (move.is_special()) {
      // check declaration
      if (move.move_type == state::DeclareWin().move_type && !states.back().can_declare_win()) {
        return __insert_special_move(state::IllegalMove(move.elapsed_time));
      }
      return __insert_special_move(move);
    }

    auto new_state = states.back().move(move);

    // pawn-dropping checkmate => illegal move
    if (move.from == pos::HAND && move.piece_type == ptype::PAWN && new_state.is_mated()) {
      return __insert_special_move(state::IllegalMove(move.elapsed_time));
    }

    // confirm the move
    states.push_back(new_state);
    moves.push_back(move);

    // repetition
    if (++__repetitions[new_state.hash_value] == 4) {
      state::ExtendedMove m(0, 0, 0, 0);

      // examine if this is a perpetual check
      if (is_perpetual_check(new_state.hash_value))
        m = state::PerpetualCheck();
      else
        m = state::ThreefoldRepetition();
      return __insert_special_move(m);
    }

    return 0;
  }

  template <typename T>
  int move_(T const& m) { return move(static_cast<state::ExtendedMove>(m)); }

  /*
   * Return true if the game is finished.
   */
  bool is_finished() const { return !moves.empty() && moves.back().is_special(); }

  /*
   * Return true if it is a perpetual check
   */
  bool is_perpetual_check(u64 hash_value) const {
    int n = states.size();
    int count = 3;
    for (int i = n - 1; i >= 0; i -= 2) {
      if (!states[i].is_checked()) return false;
      if (states[i].hash_value == hash_value && count-- == 0) return true;
    }
    return false;
  }

 private:
  std::map<u64, int> __repetitions;

  int __insert_special_move(state::ExtendedMove move) {
    moves.push_back(move);
    return move.judge;
  }
};
}
}

#endif  // MOG_CORE_GAME_HPP_INCLUDED