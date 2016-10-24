#ifndef MOG_CORE_STATE_SIMPLE_STATE_HPP_INCLUDED
#define MOG_CORE_STATE_SIMPLE_STATE_HPP_INCLUDED

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
struct SimpleState {
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

  constexpr SimpleState(int turn = turn::BLACK, u64 owner_bits = 0ULL, u64 hand_bits = 0ULL, u64 promoted_bits = 0ULL, u64 unused_bits = MASK40,
                  BitBoard board = BitBoard(0ULL, 0ULL), PositionList const &position = {{MASK64, MASK64, MASK64, MASK64, MASK64}})
      : turn(turn),
        owner_bits(owner_bits),
        hand_bits(hand_bits),
        promoted_bits(promoted_bits),
        unused_bits(unused_bits),
        board(board),
        position(position) {}

  /**
   * Compare two objects
   *
   * Note: the order of pieces does not matters
   */
  constexpr bool operator==(SimpleState const &rhs) const { return turn == rhs.turn && __equals_helper(*this) == __equals_helper(rhs); }

  static constexpr std::pair<util::Array<util::Array<BitBoard, 14>, 2>, util::Array<util::Array<int, 7>, 2>> __equals_helper(
      SimpleState const &s) {
    util::Array<util::Array<BitBoard, 14>, 2> bbs;
    util::Array<util::Array<int, 7>, 2> hands = {{}};

    for (auto slot_id = 0; slot_id < NUM_PIECES; ++slot_id) {
      if (!s.is_used(slot_id)) continue;
      auto owner = s.get_owner(slot_id);
      auto piece_type = s.get_piece_type(slot_id);
      auto pos = s.get_position(slot_id);

      if (pos == pos::HAND) {
        hands[owner][piece_type] += 1;
      } else {
        bbs[owner][piece_type] = bbs[owner][piece_type].set(pos);
      }
    }

    return std::move(std::make_pair(bbs, hands));
  }

  constexpr bool operator!=(SimpleState const &rhs) const { return !this->operator==(rhs); }

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

  constexpr int get_raw_piece_type(int slot_id) const {
    assert(0 <= slot_id && slot_id < NUM_PIECES);

    return __raw_piece_types[slot_id];
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
   * Return pos::HAND if the piece is in hand or unused.
   */
  constexpr int get_position(int slot_id) const {
    assert(0 <= slot_id && slot_id < NUM_PIECES);

    auto x = __get_position(slot_id);
    return x == 0xff ? pos::HAND : x;
  }

  /*
   * Return the number of hand pieces.
   */
  inline constexpr int get_num_hand(int owner, int piece_type) const {
    assert(0 <= piece_type && piece_type < 8);

    return pop_ct(hand_bits & (owner ? owner_bits : ~owner_bits) & piece_masks[piece_type]);
  }

  /*
   * Return a new instance with a specified turn.
   */
  constexpr SimpleState set_turn(int new_turn) const {
    return SimpleState(new_turn, owner_bits, hand_bits, promoted_bits, unused_bits, board, position);
  }

  /*
   * Return a new instance with which an unused piece is set to the board or hands.
   */
  constexpr SimpleState set_piece(int owner, int piece_type, int pos) const {
    int slot_id = __get_unused_slot(owner, piece_type);
    if (slot_id == 64) throw RuntimeError("no left for the piece");

    auto mask = 1ULL << slot_id;

    // update flags
    auto new_unused_bits = unused_bits ^ mask;
    auto new_owner_bits = owner_bits | (static_cast<u64>(owner) << slot_id);
    auto new_promoted_bits = promoted_bits | (static_cast<u64>(ptype::is_promoted(piece_type)) << slot_id);

    if (pos == pos::HAND) {
      // check piece type
      if (piece_type == ptype::KING) throw RuntimeError("king in hand");
      if (ptype::is_promoted(piece_type)) throw RuntimeError("promoted piece in hand");

      auto new_hand_bits = hand_bits | mask;
      return std::move(SimpleState(turn, new_owner_bits, new_hand_bits, new_promoted_bits, new_unused_bits, board, position));
    } else {
      // check board
      if (board.get(pos)) throw RuntimeError("position already taken");

      // check pawn files
      if (piece_type == ptype::PAWN) {
        // exclude unused, in-hand, promoted, and opponent's pieces
        auto m = ~(unused_bits | hand_bits | promoted_bits | (owner ? ~owner_bits : owner_bits));
        for (int i = 16; i < 34; ++i) {
          if (((m >> i) & 1) && pos % 9 == __get_position(i) % 9) throw RuntimeError("two pawns in the same file");
        }
      }

      // check unmovable pieces
      if (piece_type == ptype::PAWN || piece_type == ptype::LANCE || piece_type == ptype::KNIGHT) {
        auto bb = (piece_type == ptype::KNIGHT ? (bitboard::rank1 | bitboard::rank2) : bitboard::rank1).flip_by_turn(owner);
        if (bb.get(pos)) throw RuntimeError("unmovable piece");
      }

      auto new_board = board.set(pos);

      // set position
      auto new_position = __set_position(slot_id, pos);
      return std::move(
          SimpleState(turn, new_owner_bits, hand_bits, new_promoted_bits, new_unused_bits, std::move(new_board), std::move(new_position)));
    }
  }

  /*
   * Return a new instance where all unused pieces are set to one side's hand.
   */
  constexpr SimpleState set_all_hand(int owner) const {
    auto target = unused_bits & 0x0000007fffffffffULL;  // except kings
    auto new_owner_bits = owner == turn::WHITE ? owner_bits | target : owner_bits;
    return std::move(SimpleState(turn, new_owner_bits, hand_bits | target, promoted_bits, unused_bits ^ target, board, position));
  }

  constexpr SimpleState move(int slot_id, int to_pos, bool promote, int captured_slot_id = -1) const {
    assert(slot_id >= 0 && slot_id < 40);                     // Invalid slot id
    assert(to_pos >= 0 && to_pos < 81);                       // Invalid to position
    assert(captured_slot_id >= -1 && captured_slot_id < 40);  // Invalid slot id
    assert(captured_slot_id == -1 && !board.get(to));         // There must be captured piece

    // move
    auto new_owner_bits = owner_bits;
    auto new_hand_bits = hand_bits & ~(1ULL << slot_id);
    auto new_promoted_bits = promoted_bits | (static_cast<u64>(promote) << slot_id);
    auto new_unused_bits = unused_bits;
    auto new_board = board.reset(__get_position(slot_id)).set(to_pos);
    PositionList new_position = position;

    __set_position(new_position, slot_id, to_pos);

    // capture
    if (captured_slot_id != -1) {
      auto mask = 1ULL << captured_slot_id;
      if (captured_slot_id >= 38) {  // king is captured
        new_owner_bits &= ~mask;
        new_unused_bits |= mask;
      } else {
        new_owner_bits ^= mask;
        new_hand_bits ^= mask;
        new_promoted_bits &= ~mask;  // reset promoted bit
      }

      __reset_position(new_position, captured_slot_id);
    }

    return std::move(
        SimpleState(turn ^ 1, new_owner_bits, new_hand_bits, new_promoted_bits, new_unused_bits, std::move(new_board), std::move(new_position)));
  }

  /*
   * Check the validity of the state
   *
   * This does not check legal moves
   */
  constexpr void validate() const {
    if (owner_bits & unused_bits) throw RuntimeError("conflict between owner bits and unused bits");
    if (hand_bits & unused_bits) throw RuntimeError("conflict between hand bits and unused bits");
    if (promoted_bits & unused_bits) throw RuntimeError("conflict between promoted bits and unused bits");
    if (hand_bits & promoted_bits) throw RuntimeError("conflict between hand bits and promoted bits");

    // check board
    BitBoard bb;
    for (int i = 0; i < NUM_PIECES; ++i) {
      int pos = __get_position(i);

      if (pos == 0xff) {
        if (!(((hand_bits | unused_bits) >> i) & 1)) throw RuntimeError("position must be in hand or unused");
      } else {
        if (((hand_bits | unused_bits) >> i) & 1) throw RuntimeError("position must not be in hand or unused");
        if (pos >= 81) throw RuntimeError("invalid position value");
        if (bb.get(pos)) throw RuntimeError("position already taken");
        bb = bb.set(pos);
      }
    }
    if (bb != board) throw RuntimeError("inconsistent board bitboard");
  }

  /*
   * Return 64-bit mask of the onboard pieces.
   */
  inline constexpr u64 get_board_mask() const {
    return ~(hand_bits | unused_bits);
  }

  /*
   * Return 64-bit mask of the specific side's onboard pieces.
   */
  inline constexpr u64 get_board_mask(int owner) const {
    return ~(hand_bits | unused_bits | (owner ? ~owner_bits : owner_bits));
  }

  /*
   * Return the slot number of a king.
   */
  inline static constexpr int get_king_slot(int owner) {
    assert(owner == 0 || owner == 1);
    return 38 + owner;
  }

  /*
   * Return the position of a king.
   * If the king is not on board, return pos::HAND.
   */
  inline constexpr int get_king_position(int owner) const {
    return get_position(get_king_slot(owner));
  }

  /*
   * -------- -------- -------- -------- -------- -------- -------- ------** rook
   * -------- -------- -------- -------- -------- -------- -------- ----**-- bishop
   * -------- -------- -------- -------- -------- -------- -------- ****---- lance
   * -------- -------- -------- -------- -------- -------- ----**** -------- silver
   * -------- -------- -------- -------- -------- -------- ****---- -------- knight
   * -------- -------- -------- ------** ******** ******** -------- -------- pawn
   * -------- -------- -------- --****-- -------- -------- -------- -------- gold
   * -------- -------- -------- **------ -------- -------- -------- -------- king
   */
  // todo: create in the compile time?
  static constexpr util::Array<u64, 8> piece_masks = {{
      0x0000000003ULL,  // rook
      0x000000000cULL,  // bishop
      0x00000000f0ULL,  // lance
      0x0000000f00ULL,  // silver
      0x000000f000ULL,  // knight
      0x03ffff0000ULL,  // pawn
      0x3c00000000ULL,  // gold
      0xc000000000ULL,  // king
  }};

 private:
  static constexpr util::Array<u64, NUM_PIECES> __raw_piece_types = {
      {ptype::ROOK,   ptype::ROOK,   ptype::BISHOP, ptype::BISHOP, ptype::LANCE,  ptype::LANCE,  ptype::LANCE,  ptype::LANCE,
       ptype::SILVER, ptype::SILVER, ptype::SILVER, ptype::SILVER, ptype::KNIGHT, ptype::KNIGHT, ptype::KNIGHT, ptype::KNIGHT,
       ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,
       ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,   ptype::PAWN,
       ptype::PAWN,   ptype::PAWN,   ptype::GOLD,   ptype::GOLD,   ptype::GOLD,   ptype::GOLD,   ptype::KING,   ptype::KING}};

  // todo: create in the compile time?
  static constexpr util::Array<int, 8> __piece_offsets = {{0, 2, 4, 8, 12, 16, 34, 38}};

  /*
   * Return one unused slot number.
   * If there is no slot, returns 64.
   */
  constexpr int __get_unused_slot(int owner_bit, int piece_type) const {
    if (piece_type == ptype::KING) {
      return unused_bits & (1ULL << (__piece_offsets[ptype::KING] + owner_bit)) ? __piece_offsets[ptype::KING] + owner_bit : 64;
    } else {
      return ntz(unused_bits & piece_masks[ptype::demoted(piece_type)]);
    }
  }

  constexpr int __get_position(int slot_id) const { return (position[slot_id / 8] >> (8 * (slot_id % 8))) & 0xffULL; }

  static inline constexpr void __set_position(PositionList &position_list, int slot_id, int pos) {
    auto &x = position_list[slot_id / 8];
    auto y = 8 * (slot_id % 8);
    x &= ~(0xffULL << y);
    x |= static_cast<u64>(pos) << y;
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

#endif  // MOG_CORE_STATE_SIMPLE_STATE_HPP_INCLUDED
