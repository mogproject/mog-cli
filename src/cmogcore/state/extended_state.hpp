#ifndef MOG_CORE_STATE_EXTENDED_STATE_HPP_INCLUDED
#define MOG_CORE_STATE_EXTENDED_STATE_HPP_INCLUDED

#include <cassert>
#include <algorithm>
#include "../util.hpp"
#include "../bitboard.hpp"
#include "../attack.hpp"
#include "./state.hpp"
#include "./move.hpp"

namespace mog {
namespace core {
namespace state {

/*
  * Create random hash seed by using linear congruential generator(LCG).
  */
template <size_t N>
constexpr auto __make_hash_seed(uint32_t random_seed) {
  util::Array<u64, N> seeds = {{}};

  for (size_t i = 0; i < N; ++i) {
    uint32_t lo = util::lcg_parkmiller(random_seed);
    uint32_t hi = util::lcg_parkmiller(lo);
    random_seed = hi;
    seeds[i] = static_cast<u64>(hi) << 32 | lo;
  }
  return std::move(seeds);
}

/*
 * State class with calculated attack bitboards
 */
struct ExtendedState {
  typedef util::Array<BitBoard, State::NUM_PIECES * 2> LegalMoveList;
  typedef util::Array<BitBoard, State::NUM_PIECES> AttackBBList;
  typedef util::Array<int, pos::NUM_CELLS> BoardTable;
  typedef util::Array<BitBoard, turn::NUM_TURNS> OccBBList;

  int const EMPTY_CELL = -1;
  static constexpr size_t HASH_SEED_BOARD_SIZE = turn::NUM_TURNS * ptype::NUM_PIECE_TYPES * pos::NUM_CELLS;
  static constexpr size_t HASH_SEED_HAND_SIZE = turn::NUM_TURNS * ptype::NUM_HAND_TYPES * ptype::NUM_PAWNS;

  State state;
  AttackBBList attack_bbs = {{}};
  BoardTable board_table = {{}};  // pos -> slot_id
  OccBBList occ = {{}};
  OccBBList occ_pawn = {{}};
  u64 hash_value = 0ULL;  // 64 bit hash

  // todo: refactor to be a constexpr class?

  constexpr ExtendedState(State const& s, AttackBBList const& attack_bbs, BoardTable board_table, OccBBList occ, OccBBList occ_pawn,
                          u64 hash_value)
      : state(s), attack_bbs(attack_bbs), board_table(board_table), occ(occ), occ_pawn(occ_pawn), hash_value(hash_value) {}

  constexpr ExtendedState(State const& s) : state(s) {
    std::fill(board_table.begin(), board_table.end(), EMPTY_CELL);
    hash_value = s.turn ? __hash_seed_turn : 0ULL;

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

      // initialize hash value for board
      hash_value ^= __get_hash_seed_board(owner, piece_type, pos);
    }

    // initialize hash value for hands
    for (int owner = 0; owner < turn::NUM_TURNS; ++owner)
      for (int pt = 0; pt < ptype::NUM_HAND_TYPES; ++pt) {
        auto cnt = s.get_num_hand(owner, pt);
        for (int i = 0; i < cnt; ++i) hash_value ^= __get_hash_seed_hand(owner, pt, i);
      }
  }

  constexpr bool operator==(ExtendedState const& rhs) const { return state == rhs.state; }

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
    auto new_hash_value = hash_value ^ __hash_seed_turn;

    // captured piece
    if (board_table[to_pos] != EMPTY_CELL) {
      captured_slot_id = board_table[to_pos];
      auto captured_ptype = state.get_piece_type(captured_slot_id);
      auto captured_raw_ptype = state.get_raw_piece_type(captured_slot_id);
      auto new_turn = turn ^ 1;

      new_occ[new_turn] = new_occ[new_turn].reset(to_pos);
      if (state.get_piece_type(captured_slot_id) == ptype::PAWN) {
        new_occ_pawn[new_turn] = new_occ_pawn[new_turn].reset(to_pos);
      }
      new_hash_value ^= __get_hash_seed_board(new_turn, captured_ptype, to_pos);
      new_hash_value ^= __get_hash_seed_hand(turn, captured_raw_ptype, state.get_num_hand(turn, captured_raw_ptype));
    }

    // update state
    auto new_state = state.move(slot_id, to_pos, promote, captured_slot_id);

    // moved piece
    if (from_hand) {
      new_hash_value ^= __get_hash_seed_hand(turn, from_ptype, new_state.get_num_hand(turn, from_ptype));
    } else {
      new_occ[turn] = new_occ[turn].reset(from_pos);
      if (from_ptype == ptype::PAWN) new_occ_pawn[turn] = new_occ_pawn[turn].reset(from_pos);
      new_board_table[from_pos] = EMPTY_CELL;
      new_hash_value ^= __get_hash_seed_board(turn, from_ptype, from_pos);
    }

    new_occ[turn] = new_occ[turn].set(to_pos);
    if (to_ptype == ptype::PAWN) new_occ_pawn[turn] = new_occ[turn].set(to_pos);
    new_board_table[to_pos] = slot_id;
    new_hash_value ^= __get_hash_seed_board(turn, to_ptype, to_pos);

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
                         std::move(new_occ_pawn), new_hash_value);
  }

  /** get attack bitboards */
  constexpr BitBoard get_attack_bb(size_t index) const { return index < State::NUM_PIECES ? attack_bbs[index] : bitboard::EMPTY; }

  /*
   * Return true if the player's king is checked by the opponent's piece(s)
   */
  bool is_checked() const {
    auto bb = BitBoard();
    auto mask = state.get_board_mask(state.turn ^ 1);
    for (int i = 0; i < State::NUM_PIECES; ++i) {
      if (mask & (1ULL << i)) bb = bb | attack_bbs[i];
    }
    return bb.get(state.get_king_position(state.turn));
  }

  bool is_mated() const {
    // todo
    return false;
  }

  /*
   * Return true if the player can satisfy the conditions of declaring win.
   */
  bool can_declare_win(int min_point=24) const {
    // todo
    return false;
  }

  /*
   * Test king's existance on the board
   */
  bool is_king_alive(int owner) const { return state.get_king_position(owner) != pos::HAND; }

 private:
  static constexpr u64 __hash_seed_turn = __make_hash_seed<1>(0UL)[0];
  static constexpr auto __hash_seed_board = __make_hash_seed<HASH_SEED_BOARD_SIZE>(1UL);
  static constexpr auto __hash_seed_hand = __make_hash_seed<HASH_SEED_HAND_SIZE>(2UL);

  // todo: to be a static table[2]
  inline constexpr static BitBoard __get_promotion_zone(int const owner) {
    return (bitboard::rank1 | bitboard::rank2 | bitboard::rank3).flip_by_turn(owner);
  }

  // todo: to be a static table[2][14]
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

  inline static constexpr u64 __get_hash_seed_board(int owner, int piece_type, int pos) {
    return __hash_seed_board[owner + piece_type * turn::NUM_TURNS + pos * turn::NUM_TURNS * ptype::NUM_PIECE_TYPES];
  }

  inline static constexpr u64 __get_hash_seed_hand(int owner, int piece_type, int num) {
    return __hash_seed_hand[owner + piece_type * turn::NUM_TURNS + num * turn::NUM_TURNS * ptype::NUM_HAND_TYPES];
  }
};
}
}
}

#endif  // MOG_CORE_STATE_EXTENDED_STATE_HPP_INCLUDED