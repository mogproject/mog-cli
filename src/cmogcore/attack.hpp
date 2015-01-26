#ifndef MOG_CORE_ATTACK_HPP_INCLUDED
#define MOG_CORE_ATTACK_HPP_INCLUDED

#include "bitboard.hpp"
#include "attack/direct.hpp"
#include "attack/ranged.hpp"
#include "attack/aerial.hpp"

namespace mog {
  namespace core {
    namespace attack {
      /** attack bitboard for direct pieces on board */
      BitBoard get_attack(int owner, int ptype, int index) {
        return attack::bb_table_direct[(owner << 4) + ptype][index];
      }

      /** attack bitboard for ranged pieces on board */
      BitBoard get_attack(int owner, int ptype, int index, BitBoard const& occ) {
        // todo: impl
        return BitBoard();
      };

      /** attack bitboard for pawn from hand */
      BitBoard get_attack(int owner, BitBoard const& occ, BitBoard const& my_pawn_occ) {
        return attack::bb_table_aerial[(owner << 4) + ptype::PAWN] & ~(occ | my_pawn_occ.spread_all_file());
      }

      /** attack bitboard for pieces from hand except pawn */
      BitBoard get_attack(int owner, int ptype, BitBoard const& occ) {
        return attack::bb_table_aerial[(owner << 4) + ptype] & ~occ;
      };
    }


    class Attack {
     public:
    };

  }
}

#endif  // MOG_CORE_ATTACK_HPP_INCLUDED