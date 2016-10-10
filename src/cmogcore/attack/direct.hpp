#ifndef MOG_CORE_ATTACK_DIRECT_HPP_INCLUDED
#define MOG_CORE_ATTACK_DIRECT_HPP_INCLUDED

#include <array>
#include "../util.hpp"
#include "../bitboard.hpp"

namespace mog {
namespace core {
namespace attack {
//
// direct piece types
//
namespace direct {
// attack bitboard for black on position 55
constexpr BitBoard center_king = BitBoard(0, 0, 0, 0070, 0050, 0070, 0, 0, 0);
constexpr BitBoard center_gold = BitBoard(0, 0, 0, 0070, 0050, 0020, 0, 0, 0);
constexpr BitBoard center_silver = BitBoard(0, 0, 0, 0070, 0000, 0050, 0, 0, 0);
constexpr BitBoard center_knight = BitBoard(0, 0, 0050, 0, 0, 0, 0, 0, 0);
constexpr BitBoard center_pawn = BitBoard(0, 0, 0, 0020, 0, 0, 0, 0, 0);

constexpr BitBoard ptype_to_center_bb[] = {
    // rook        bishop      lance        silver         knight         pawn         glod         king
    BitBoard(), BitBoard(), BitBoard(),  center_silver, center_knight, center_pawn, center_gold, center_king,
    BitBoard(), BitBoard(), center_gold, center_gold,   center_gold,   center_gold, BitBoard(),  BitBoard(),
};

inline constexpr BitBoard make_attack_bb(int const owner, int const ptype, int const file, int const rank) {
  return ptype_to_center_bb[ptype].flip_by_turn(owner).shift_left(file - 5).shift_down(rank - 5);
}

constexpr auto generate_attack_bb(int const n) {
  return make_attack_bb((n >> 4) & 1, n & 0xf, pos::get_file(n >> 5), pos::get_rank(n >> 5));
}
}

constexpr auto bb_table_direct = util::array::iterate<81 * 2 * 16>(&direct::generate_attack_bb);
}
}
}

#endif  // MOG_CORE_ATTACK_DIRECT_HPP_INCLUDED