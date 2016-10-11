#ifndef MOG_CORE_STATE_EXTENDED_DSTATE_HPP_INCLUDED
#define MOG_CORE_STATE_EXTENDED_DSTATE_HPP_INCLUDED

#include <cassert>
#include <algorithm>
#include "../util.hpp"
#include "../bitboard.hpp"
#include "../attack.hpp"
#include "./state.hpp"

namespace mog {
namespace core {
namespace state {
/*
 * State class with calculated attack bitboards
 */
struct ExtendedState {
  typedef util::Array<BitBoard, State::NUM_PIECES * 2> LegalMoveList;
  int const EMPTY_CELL = -1;

  State state;
  util::Array<BitBoard, State::NUM_PIECES> attack_bbs;
  util::Array<int, pos::NUM_CELLS> board_table;  // pos -> slot_id

  BitBoard occ[turn::NUM_TURNS];
  BitBoard occ_pawn[turn::NUM_TURNS];

  // todo: refactor to be a constexpr class?
  ExtendedState(State const& s) : state(s) {
    std::fill(board_table.begin(), board_table.end(), EMPTY_CELL);

    // prepare occupancy bitboards and initialize boards array
    for (size_t slot_id = 0; slot_id < State::NUM_PIECES; ++slot_id) {
      if (!state.is_used(slot_id)) continue;

      auto pos = state.get_position(slot_id);
      if (pos == pos::HAND) continue;

      auto owner = state.get_owner(slot_id);
      auto piece_type = state.get_piece_type(slot_id);

      // prepare occupancy bitboards
      occ[owner] = occ[owner].set(pos);
      if (piece_type == ptype::PAWN) occ_pawn[owner] = occ_pawn[owner].set(pos);

      // initialize board table
      board_table[pos] = slot_id;

      // set attack bbs
      attack_bbs[slot_id] = ptype::is_ranged(piece_type) ? attack::get_attack(owner, piece_type, pos, state.board)
                                                         : attack::get_attack(owner, piece_type, pos);
    }
  }

  /*
   * index 0-39: raw moves
   * index 40-79: promoted moves
   */
  LegalMoveList get_legal_moves() {
    LegalMoveList ret;

    int hand_used = 0;

    for (size_t slot_id = 0; slot_id < State::NUM_PIECES; ++slot_id) {
      if (!state.is_used(slot_id)) continue;

      auto owner = state.get_owner(slot_id);
      if (owner != state.turn) continue;

      auto pos = state.get_position(slot_id);
      auto piece_type = state.get_piece_type(slot_id);

      if (pos == pos::HAND) {
        auto mask = 1 << state.get_raw_piece_type(slot_id);
        if (!(hand_used & mask)) {
          if (piece_type == ptype::PAWN) {
            ret[slot_id] = attack::get_attack(owner, state.board, occ_pawn[state.turn]);
          } else {
            ret[slot_id] = attack::get_attack(owner, piece_type, state.board);
          }
          hand_used |= mask;
        }
      } else {  // board
        auto base = ((ptype::is_ranged(piece_type)) ? attack::get_attack(owner, piece_type, pos, state.board)
                                                    : attack::get_attack(owner, piece_type, pos)) &
                    ~occ[state.turn];

        if (ptype::is_promoted(piece_type)) {  // already promoted
          ret[slot_id + State::NUM_PIECES] = base;
        } else if (!ptype::can_promote(piece_type)) {  // cannot promote
          ret[slot_id] = base;
        } else {
          auto promo_zone = __get_promotion_zone(owner);
          auto restriction = __get_restriction(owner, piece_type);

          if (promo_zone.get(pos)) {  // in the promotion zone
            ret[slot_id] = base & restriction;
            ret[slot_id + State::NUM_PIECES] = base;
          } else {
            ret[slot_id] = base & restriction;
            ret[slot_id + State::NUM_PIECES] = base & promo_zone;
          }
        }
      }
    }
    return ret;
  }

  /*
   * Make one move.
   */
  void move(int slot_id, int to_pos, bool promote) {
    assert(0 <= slot_id && slot_id < State::NUM_PIECES);

    auto captured_slot_id = -1;

    // captured piece
    if (board_table[to_pos] != EMPTY_CELL) {
      captured_slot_id = board_table[to_pos];
      occ[state.turn ^ 1] = occ[state.turn ^ 1].reset(to_pos);
      if (state.get_piece_type(captured_slot_id) == ptype::PAWN) occ_pawn[state.turn ^ 1] = occ_pawn[state.turn ^ 1].reset(to_pos);
    }

    // moved piece
    auto from_ptype = state.get_piece_type(slot_id);
    auto to_ptype = from_ptype | (promote ? 8 : 0);
    auto from_pos = state.get_position(slot_id);

    occ[state.turn] = occ[state.turn].reset(from_pos);
    occ[state.turn] = occ[state.turn].set(to_pos);

    if (from_ptype == ptype::PAWN) occ_pawn[state.turn] = occ_pawn[state.turn].reset(from_pos);
    if (to_ptype == ptype::PAWN) occ_pawn[state.turn] = occ[state.turn].set(to_pos);

    board_table[to_pos] = slot_id;

    // update state
    state = state.move(slot_id, to_pos, promote, captured_slot_id);

    // update attack bbs
    attack_bbs[slot_id] =
        ptype::is_ranged(to_ptype) ? attack::get_attack(to_ptype, to_pos, state.board) : attack::get_attack(to_ptype, to_ptype, to_pos);

    // on-board ranged pieces (can be affected by this move)
    BitBoard from_and_to = BitBoard().set(from_pos).set(to_pos);

    u64 mask = ~(state.unused_bits | state.hand_bits | (state.piece_masks[ptype::LANCE] & state.promoted_bits));
    for (auto i = 0; i < 8; ++i) {  // slot id: ROOK, BISHOP, LANCE
      if (i == slot_id) continue;

      auto owner = state.get_owner(i);
      auto piece_type = state.get_piece_type(i);
      auto pos = state.get_position(i);

      if (((mask >> i) & 1) && (attack_bbs[i] & from_and_to).is_defined()) attack_bbs[i] = attack::get_attack(owner, piece_type, pos, state.board);
    }
  }

  void move(int turn, int from_pos, int to_pos, bool promote) {
    // todo; check turn and throw error
    move(board_table[from_pos], to_pos, promote);
  }
  
  /** get attack bitboards */
  BitBoard get_attack_bb(size_t index) const { return index < State::NUM_PIECES ? attack_bbs[index] : bitboard::EMPTY; }

 private:
  inline constexpr static BitBoard __get_promotion_zone(int const owner) {
    return (bitboard::rank1 | bitboard::rank2 | bitboard::rank3).flip_by_turn(owner);
  }

  inline constexpr static BitBoard __get_restriction(int const owner, int const piece_type) {
    if (piece_type == ptype::PAWN || piece_type == ptype::LANCE) {
      return (~bitboard::rank1).flip_by_turn(owner);
    } else if (piece_type == ptype::KNIGHT) {
      return (~(bitboard::rank1 | bitboard::rank2)).flip_by_turn(owner);
    } else {
      return bitboard::FULL;
    }
  }
};
}
}
}

#endif  // MOG_CORE_STATE_EXTENDED_DSTATE_HPP_INCLUDED