#ifndef MOG_CORE_ATTACK_RANGED_COMMON_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_COMMON_HPP_INCLUDED

#include <array>
#include <boost/preprocessor.hpp>
#include "../util.hpp"
#include "../bitboard.hpp"

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

#define POS_INDEX_TO_FILE(n) BOOST_PP_ADD(BOOST_PP_MOD(n, 9), 1)
#define POS_INDEX_TO_RANK(n) BOOST_PP_ADD(BOOST_PP_DIV(n, 9), 1)

#define FUNC_NAME(z, n, text) text##n

      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_COMMON_HPP_INCLUDED