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

        constexpr auto empty = util::array::fill<MagicCalculator, 81>(&empty_magic);

        constexpr util::Array<MagicCalculator, 81> atk_blance = {{ BOOST_PP_ENUM(81, FUNC_NAME, attack_black_lance_) }};
        constexpr util::Array<MagicCalculator, 81> atk_wlance = {{ BOOST_PP_ENUM(81, FUNC_NAME, attack_white_lance_) }};

        constexpr util::Array<util::Array<ranged::MagicCalculator, 81>, 32> bb_table_ranged = {{
          empty, empty, empty, atk_blance, empty, empty, empty,  empty,
          empty, empty, empty, empty,      empty, empty, empty,  empty,
          empty, empty, empty, atk_wlance, empty, empty, empty,  empty,
          empty, empty, empty, empty,      empty, empty, empty,  empty,
        }};
      }

      constexpr auto bb_table_ranged = ranged::bb_table_ranged;
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_HPP_INCLUDED