#ifndef MOG_CORE_ATTACK_RANGED_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_HPP_INCLUDED

#include "ranged_lance.hpp"
#include "ranged_bishop.hpp"
#include "ranged_rook.hpp"

namespace mog {
namespace core {
namespace attack {
//
// ranged piece types
//
namespace ranged {
//
// utilities
//
typedef BitBoard (*MagicCalculator)(BitBoard const&);

//
// Create array of functions.
//
constexpr BitBoard empty_magic(BitBoard const& notuse) { return bitboard::EMPTY; }

constexpr auto empty = util::array::fill<81>(&empty_magic);
constexpr auto rook = RookAttackGenerator<false>::generate();
constexpr auto prook = RookAttackGenerator<true>::generate();
constexpr auto bishop = BishopAttackGenerator<false>::generate();
constexpr auto pbishop = BishopAttackGenerator<true>::generate();
constexpr auto blance = LanceAttackGenerator<turn::BLACK>::generate();
constexpr auto wlance = LanceAttackGenerator<turn::WHITE>::generate();

constexpr util::Array<util::Array<MagicCalculator, 81>, 32> bb_table_ranged = {{
    rook,  bishop,  blance, empty, empty, empty, empty, empty,  //
    prook, pbishop, empty,  empty, empty, empty, empty, empty,  //
    rook,  bishop,  wlance, empty, empty, empty, empty, empty,  //
    prook, pbishop, empty,  empty, empty, empty, empty, empty,  //
}};
}

constexpr auto bb_table_ranged = ranged::bb_table_ranged;
}
}
}

#endif  // MOG_CORE_ATTACK_RANGED_HPP_INCLUDED