#ifndef MOG_CORE_STATE_EXTENDED_STATE_HPP_INCLUDED
#define MOG_CORE_STATE_EXTENDED_STATE_HPP_INCLUDED

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
  typedef util::Array<BitBoard, State::NUM_PIECES> AttackBBList;
  typedef util::Array<int, pos::NUM_CELLS> BoardTable;
  typedef util::Array<BitBoard, turn::NUM_TURNS> OccBBList;

  int const EMPTY_CELL = -1;

  State state;
  AttackBBList attack_bbs = {{}};
  BoardTable board_table = {{}};  // pos -> slot_id
  OccBBList occ = {{}};
  OccBBList occ_pawn = {{}};

  // todo: refactor to be a constexpr class?

  constexpr ExtendedState(State const& s, AttackBBList const& attack_bbs, BoardTable board_table, OccBBList occ, OccBBList occ_pawn)
      : state(s), attack_bbs(attack_bbs), board_table(board_table), occ(occ), occ_pawn(occ_pawn) {}

  constexpr ExtendedState(State const& s) : state(s) {
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
  constexpr LegalMoveList get_legal_moves() const {
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
    return std::move(ret);
  }

  /*
   * Make one move.
   */
  constexpr ExtendedState move(Move const& m) const {
    auto turn = m.turn;
    if (turn != state.turn) throw RuntimeError("invalid turn");

    auto from_pos = m.from;
    auto to_pos = m.to;
    auto to_ptype = m.piece_type;

    bool from_hand = from_pos == pos::HAND;
    auto slot_id = from_hand ? __get_hand_slot(turn, to_ptype) : board_table[from_pos];
    auto from_ptype = from_hand ? to_ptype : state.get_piece_type(slot_id);
    bool promote = from_ptype != to_ptype;

    auto captured_slot_id = -1;

    auto new_attack_bbs = attack_bbs;
    auto new_board_table = board_table;
    auto new_occ = occ;
    auto new_occ_pawn = occ_pawn;

    // captured piece
    if (board_table[to_pos] != EMPTY_CELL) {
      captured_slot_id = board_table[to_pos];
      new_occ[turn ^ 1] = new_occ[turn ^ 1].reset(to_pos);
      if (state.get_piece_type(captured_slot_id) == ptype::PAWN) new_occ_pawn[turn ^ 1] = new_occ_pawn[turn ^ 1].reset(to_pos);
    }

    // moved piece
    if (!from_hand) {
      new_occ[turn] = new_occ[turn].reset(from_pos);
      if (from_ptype == ptype::PAWN) new_occ_pawn[turn] = new_occ_pawn[turn].reset(from_pos);
      new_board_table[from_pos] = EMPTY_CELL;
    }

    new_occ[turn] = new_occ[turn].set(to_pos);
    if (to_ptype == ptype::PAWN) new_occ_pawn[turn] = new_occ[turn].set(to_pos);
    new_board_table[to_pos] = slot_id;

    // update state
    auto new_state = state.move(slot_id, to_pos, promote, captured_slot_id);

    // update attack bbs
    new_attack_bbs[slot_id] =
        ptype::is_ranged(to_ptype) ? attack::get_attack(to_ptype, to_pos, new_state.board) : attack::get_attack(to_ptype, to_ptype, to_pos);

    // on-board ranged pieces (can be affected by this move)
    BitBoard from_and_to = BitBoard().set(to_pos);
    if (!from_hand) from_and_to.set(from_pos);

    u64 mask = ~(new_state.unused_bits | new_state.hand_bits | (new_state.piece_masks[ptype::LANCE] & new_state.promoted_bits));
    for (auto i = 0; i < 8; ++i) {  // slot id: ROOK, BISHOP, LANCE
      if (i == slot_id) continue;

      auto owner = new_state.get_owner(i);
      auto piece_type = new_state.get_piece_type(i);
      auto pos = new_state.get_position(i);

      if (((mask >> i) & 1) && (attack_bbs[i] & from_and_to).is_defined())
        new_attack_bbs[i] = attack::get_attack(owner, piece_type, pos, new_state.board);
    }

    return ExtendedState(std::move(new_state), std::move(new_attack_bbs), std::move(new_board_table), std::move(new_occ),
                         std::move(new_occ_pawn));
  }

  /** get attack bitboards */
  constexpr BitBoard get_attack_bb(size_t index) const { return index < State::NUM_PIECES ? attack_bbs[index] : bitboard::EMPTY; }

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

  constexpr int __get_hand_slot(int owner, int piece_type) const {
    u64 mask = state.piece_masks[piece_type] & (owner ? state.owner_bits : ~state.owner_bits) & state.hand_bits;
    return ntz(mask);
  }
};
}
}
}

#endif  // MOG_CORE_STATE_EXTENDED_STATE_HPP_INCLUDED