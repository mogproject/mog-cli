#ifndef MOG_CORE_ATTACK_RANGED_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_HPP_INCLUDED

#include "ranged_common.hpp"
#include "ranged_lance_black.hpp"
#include "ranged_lance_white.hpp"
//#include "ranged_bishop.hpp"
//#include "ranged_look.hpp"

namespace mog {
  namespace core {
    namespace attack {
      //
      // ranged piece types
      //
      namespace ranged {
        //
        // Create array of functions.
        //
        constexpr BitBoard empty_magic(BitBoard const& notuse) { return bitboard::EMPTY; }

        constexpr auto empty = util::array::fill<81>(&empty_magic);
        constexpr auto blance = generate_blance_fp();

        constexpr util::Array<MagicCalculator, 81> wlance = {{ BOOST_PP_ENUM(81, FUNC_NAME, attack_white_lance_) }};
        constexpr auto rook = util::array::fill<81>(&empty_magic);
        constexpr auto bishop = util::array::fill<81>(&empty_magic);
        constexpr auto prook = util::array::fill<81>(&empty_magic);
        constexpr auto pbishop = util::array::fill<81>(&empty_magic);

        constexpr util::Array<util::Array<ranged::MagicCalculator, 81>, 32> bb_table_ranged = {{
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