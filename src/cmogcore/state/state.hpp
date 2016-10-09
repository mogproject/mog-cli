#ifndef MOG_CORE_STATE_STATE_HPP_INCLUDED
#define MOG_CORE_STATE_STATE_HPP_INCLUDED

#include "../util.hpp"
#include "../bitboard.hpp"

namespace mog {
namespace core {
namespace state {

/*
 * Immutable state structure
 *
 * This class is an atomic class for the state of the board and hands.
 * In this model, a state is described by the player's turn and the state of
 * each piece (there should be 40 pieces).
 *
 * @param turn 0 -> black, 1 -> white
 * @param owner_bits a 64-bit bitmask which describes that N-th smallest bit is ON when piece N's owner is white.
 * @param hand_bits a 64-bit bitmask which describes that N-th smallest bit is ON when piece N is in hands.
 * @param promoted_bits a 64-bit bitmask which describes that N-th smallest bit is ON when piece N is promoted.
 * @param unused_bits a 64-bit bitmask which describes that N-th smallest bit is ON when piece N is unused (neither on board nor in hands).
 * @param board a bitboard which denotes bits on board where a piece is set.
 * @param position a fixed-size array which contains position information of each of the 40 pieces.
 *
 * Slot id:
 *    0- 1: rook
 *    2- 3: bishop
 *    4- 7: lance
 *    8-11: silver
 *   12-15: knight
 *   16-33: pawn
 *   34-37: gold
 *   38   : black king
 *   39   : white king
 */
struct State {
  static constexpr int NUM_PIECES = 40;
  static constexpr int NUM_POSITION_LIST = 5;

  int turn;
  u64 owner_bits;
  u64 hand_bits;
  u64 promoted_bits;
  u64 unused_bits;
  BitBoard board;
  typedef util::Array<u64, NUM_POSITION_LIST> PositionList;
  PositionList position;

  constexpr State(int turn = turn::BLACK, u64 owner_bits = 0ULL, u64 hand_bits = 0ULL, u64 promoted_bits = 0ULL, u64 unused_bits = MASK40,
                  BitBoard board = BitBoard(0ULL, 0ULL), PositionList const &position = {{MASK64, MASK64, MASK64, MASK64, MASK64}})
      : turn(turn),
        owner_bits(owner_bits),
        hand_bits(hand_bits),
        promoted_bits(promoted_bits),
        unused_bits(unused_bits),
        board(board),
        position(position) {
    assert(is_valid());
  }

  /**
   * Compare two objects
   */
  constexpr bool operator==(State const &rhs) const {
    return turn == rhs.turn && owner_bits == rhs.owner_bits && hand_bits == rhs.hand_bits && promoted_bits == rhs.promoted_bits &&
           unused_bits == rhs.unused_bits && position == rhs.position;
  }

  constexpr bool operator!=(State const &rhs) const { return !this->operator==(rhs); }

  /*
   * Return true if a specified piece is in use.
   */
  constexpr bool is_used(int slot_id) const {
    assert(0 <= slot_id && slot_id < NUM_PIECES);

    return ~(unused_bits >> slot_id) & 1;
  }

  /*
   * Return the owner of a specified piece.
   *
   * Return 0 if the owner is BLACK or the piece is unused, and return 1 if the owner is WHITE
   */
  constexpr int get_owner(int slot_id) const {
    assert(0 <= slot_id && slot_id < NUM_PIECES);

    return (owner_bits >> slot_id) & 1;
  }

  /*
   * Return the piece type of a specified piece.
   */
  constexpr int get_piece_type(int slot_id) const {
    assert(0 <= slot_id && slot_id < NUM_PIECES);

    auto raw_type = __raw_piece_types[slot_id];
    return (((promoted_bits >> slot_id) & 1) << 3) | raw_type;
  }

  /*
   * Return the position of a specified piece.
   *
   * Return 81 if the piece is in hand or unused.
   */
  constexpr int get_position(int slot_id) const {
    assert(0 <= slot_id && slot_id < NUM_PIECES);

    auto x = __get_position(slot_id);
    return x == 0xff ? pos::HAND : x;
  }

  /*
   * Return a new instance with a specified turn.
   */
  constexpr State set_turn(int new_turn) const {
    return State(new_turn, owner_bits, hand_bits, promoted_bits, unused_bits, board, position);
  }

  /*
   * Return a new instance with which an unused piece is set to the board or hands.
   */
  constexpr State set_piece(int owner, int piece_type, int pos) const {
    int slot_id = __get_unused_slot(owner, piece_type);
    if (slot_id == 64) return *this;  // no slot left

    auto mask = 1ULL << slot_id;

    // update flags
    auto new_unused_bits = unused_bits ^ mask;
    auto new_owner_bits = owner_bits | (static_cast<u64>(owner) << slot_id);
    auto new_promoted_bits = promoted_bits | (static_cast<u64>(ptype::is_promoted(piece_type)) << slot_id);

    if (pos == pos::HAND) {
      auto new_hand_bits = hand_bits | mask;
      return std::move(State(turn, new_owner_bits, new_hand_bits, new_promoted_bits, new_unused_bits, board, position));
    } else {
      if (board.get(pos)) return *this;  // the position is already set by another piece
      auto new_board = board.set(pos);

      // set position
      auto new_position = __set_position(slot_id, pos);
      return std::move(
          State(turn, new_owner_bits, hand_bits, new_promoted_bits, new_unused_bits, std::move(new_board), std::move(new_position)));
    }
  }

  /*
   * Return a new instance where all unused pieces are set to one side's hand.
   */
  constexpr State set_all_hand(int owner) const {
    auto target = unused_bits & 0x0000007fffffffffULL;  // except kings
    auto new_owner_bits = owner == turn::WHITE ? owner_bits | target : owner_bits;
    return std::move(State(turn, new_owner_bits, hand_bits | target, promoted_bits, unused_bits ^ target, board, position));
  }

  constexpr State move(int slot_id, int to_pos, bool promote, int captured_slot_id = -1) const {
    assert(slot_id >= 0 && slot_id < 40);                     // Invalid slot id
    assert(to_pos >= 0 && to_pos < 81);                       // Invalid to position
    assert(captured_slot_id >= -1 && captured_slot_id < 40);  // Invalid slot id
    assert(captured_slot_id == -1 && !board.get(to));         // There must be captured piece

    auto new_owner_bits = owner_bits;
    auto new_hand_bits = hand_bits;
    auto new_promoted_bits = promoted_bits;
    auto from_pos = __get_position(slot_id);
    PositionList new_position = position;

    // capture
    if (captured_slot_id != -1) {
      auto mask = 1ULL << captured_slot_id;
      new_owner_bits ^= mask;
      new_hand_bits ^= mask;
      new_promoted_bits ^= promoted_bits & mask;  // reset promoted bit
      __reset_position(new_position, slot_id);
    }

    // move
    __set_position(new_position, slot_id, to_pos);

    return std::move(State(turn ^ 1, new_owner_bits, new_hand_bits, new_promoted_bits, unused_bits, std::move(board.reset(from_pos)),
                           std::move(new_position)));
  }

  constexpr bool is_valid() const {
    if (owner_bits & unused_bits) return false;
    if (promoted_bits & unused_bits) return false;
    if (hand_bits & unused_bits) return false;
    if (promoted_bits & hand_bits) return false;

    // check board
    BitBoard bb;
    for (int i = 0; i < 40; ++i) {
      int pos = __get_position(i);

      if (pos != 0xff) {
        if (pos >= 81) return false;
        if (bb.get(pos)) return false;
        bb = bb.set(pos);
      }
    }
    if (bb != board) return false;

    // this class does not check the move rules
    return true;
  }

 private:
  static constexpr util::Array<u64, 8> __piece_masks = {{
      0xc000000000ULL,  // king
      0x0000000003ULL,  // rook
      0x000000000cULL,  // bishop
      0x00000000f0ULL,  // lance
      0x3c00000000ULL,  // gold
      0x0000000f00ULL,  // silver
      0x000000f000ULL,  // knight
      0x03ffff0000ULL,  // pawn
  }};

  static constexpr util::Array<u64, NUM_PIECES> __raw_piece_types = {
      {ptype::ROOK,   ptype::ROOK,   ptype::BISHOP, ptype::BISHOP, ptype::LANCE,  ptype::LANCE,  ptype::LANCE,  ptype::LANCE,
       ptype::SILVER, ptype::SILVER, ptype::SILVER, ptype::SILVER, ptype::KNIGHT, ptype::KNIGHT, ptype::KNIGHT, ptype::KNIGHT,
       ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,
       ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,
       ptype::PAWN,   ptype::PAWN,   ptype::GOLD,   ptype::GOLD,   ptype::GOLD,   ptype::GOLD,   ptype::KING,   ptype::KING}};

  /*
   * Return one unused slot number.
   * If there is no slot, returns 64.
   */
  constexpr int __get_unused_slot(int owner_bits, int piece_type) const {
    if (piece_type == ptype::KING) {
      return unused_bits & (1ULL << (38 + owner_bits)) ? 38 + owner_bits : 64;  // 38=king's offset
    } else {
      return ntz(unused_bits & __piece_masks[ptype::demoted(piece_type)]);
    }
  }

  constexpr int __get_position(int slot_id) const { return (position[slot_id / 8] >> (8 * (slot_id % 8))) & 0xffULL; }

  static inline constexpr void __set_position(PositionList &position_list, int slot_id, int pos) {
    auto i = slot_id / 8;
    auto j = 8 * (slot_id % 8);
    position_list[i] = (position_list[i] & (MASK64 ^ (0xffULL << j))) | (static_cast<u64>(pos) << j);
  }

  constexpr PositionList __set_position(int slot_id, int pos) const {
    PositionList p = position;
    __set_position(p, slot_id, pos);
    return std::move(p);
  }

  static inline constexpr void __reset_position(PositionList &position_list, int slot_id) { __set_position(position_list, slot_id, 0xff); }
};
}
}
}

#endif  // MOG_CORE_STATE_STATE_HPP_INCLUDED
