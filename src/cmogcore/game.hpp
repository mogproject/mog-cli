#ifndef MOG_CORE_GAME_HPP_INCLUDED
#define MOG_CORE_GAME_HPP_INCLUDED

#include <cassert>
#include <vector>
#include "../util.hpp"
#include "../bitboard.hpp"
#include "./state/extended_state.hpp"
#include "./state/move.hpp"

namespace mog {
namespace core {

/*
 * Game class
 */
struct Game {
  std::vector<ExtendedState> states;
  std::vector<state::Move> moves;

  Game(State const& initial_state, std::vector<state::Move> moves) : moves(moves) {
    states.push_back(ExtendedState(initial_state));
    for (auto m : moves) {
      states.push_back(states.back().move(m));
    }
  }
}
}
}

#endif  // MOG_CORE_GAME_HPP_INCLUDED