#ifndef MOG_CORE_ATTACK_RANGED_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_HPP_INCLUDED

#include "ranged_lance.hpp"
#include "ranged_bishop.hpp"
//#include "ranged_look.hpp"

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
        constexpr auto blance = LanceAttackGenerator<turn::BLACK>::generate();
        constexpr auto wlance = LanceAttackGenerator<turn::WHITE>::generate();
        constexpr auto rook = util::array::fill<81>(&empty_magic);
        constexpr auto prook = util::array::fill<81>(&empty_magic);
        constexpr auto bishop = BishopAttackGenerator<false>::generate();
        constexpr auto pbishop = BishopAttackGenerator<true>::generate();

        constexpr util::Array<util::Array<MagicCalculator, 81>, 32> bb_table_ranged = {{
          empty, rook,  bishop,  blance, empty, empty, empty,  empty,
          empty, prook, pbishop, empty,  empty, empty, empty,  empty,
          empty, rook,  bishop,  wlance, empty, empty, empty,  empty,
          empty, prook, pbishop, empty,  empty, empty, empty,  empty,
        }};
      }

      constexpr auto bb_table_ranged = ranged::bb_table_ranged;
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_HPP_INCLUDED