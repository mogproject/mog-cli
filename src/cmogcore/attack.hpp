#ifndef MOG_CORE_ATTACK_HPP_INCLUDED
#define MOG_CORE_ATTACK_HPP_INCLUDED

#include "typedef.hpp"
#include "util.hpp"

namespace mog {
  namespace core {
    class Attack {
     public:
      static BitBoard maxAttack[2][10][81];
    };
  }
}

#endif  // MOG_CORE_ATTACK_HPP_INCLUDED