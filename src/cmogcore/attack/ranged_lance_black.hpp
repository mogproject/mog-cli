#ifndef MOG_CORE_ATTACK_RANGED_LANCE_BLACK_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_LANCE_BLACK_HPP_INCLUDED

#include "../util.hpp"
#include "../bitboard.hpp"
#include "ranged_common.hpp"

namespace mog {
  namespace core {
    namespace attack {
      namespace ranged {
        //
        // Base class
        //
        template <int Index>
        class BlackLanceAttackBase {
         private:
          /** File and rank (1-indexed) */
          static constexpr auto file = pos::get_file(Index);
          static constexpr auto rank = pos::get_rank(Index);

          /** Number of the masking bits */
          static constexpr int __num_bits = util::max(0, pos::get_rank(Index) - 2);

          /** Make attack bitboard with the specified mask */
          static constexpr BitBoard __make_table(int const mask) {
            return BitBoard().set_repeat(file, rank, 0, -1, ntz(mask) + 1);
          }

         public:
          static constexpr auto make_table() {
            return util::array::iterate<1 << __num_bits>(&__make_table);
          }

          static constexpr int logic_type = rank <= 7 ? rank <= 3 ? rank <= 2 ? 0 : 1 : 2 : rank <= 8 ? 3 : 4;
        };

        /**
         * LogicType = 0: Fixed
         */
        template <int LogicType, int Index>
        struct BlackLanceAttack {
          static BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = BlackLanceAttackBase<Index>::make_table();
            return table[0];
          }
        };

        /**
         * LogicType = 1: Low shift only
         *
         * e.g.
         *   lo >> 9
         * ---------      --------a
         * --------a      ---------
         * ---------  =>  ---------
         * ---------      ---------
         * ---------      ---------
         * ---------      ---------
         */
        template <int Index>
        struct BlackLanceAttack<1, Index> {
          static BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = BlackLanceAttackBase<Index>::make_table();
            constexpr auto affected_bb_lo = (table[0] & ~bitboard::rank1).lo;
            constexpr auto shift_width = pos::get_file(Index) + 8;
            return table[(occ.lo & affected_bb_lo) >> shift_width];
          }
        };

        /**
         * LogicType = 2: Low multiply only
         *
         * e.g.
         *   lo * 0x0040100401004000ULL (2^54 + 2^44 + 2^34 + 2^24 + 2^14) >> 59
         * ---------      ---------      ----abcde
         * --------a      ---------      ---------
         * --------b  =>  ---a-----  =>  ---------
         * --------c      --ab-----      ---------
         * --------d      -abc-----      ---------
         * --------e      abcd-----      ---------
         *                bcde-----
         *                        a
         */
        template <int Index>
        struct BlackLanceAttack<2, Index> {
          static BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = BlackLanceAttackBase<Index>::make_table();
            constexpr auto affected_bb_lo = (table[0] & ~bitboard::rank1).lo;
            constexpr auto magic = 0x0040100401004000ULL >> (pos::get_file(Index) - 1);
            constexpr auto shift_width = 66 - pos::get_rank(Index);
            return table[((occ.lo & affected_bb_lo) * magic) >> shift_width];
          }
        };

        /**
         * LogicType = 3: Low multiply and high shift
         *
         * e.g.
         *   lo * 0x0040100401004000ULL (2^54 + 2^44 + 2^34 + 2^24 + 1^14) >> 58
         * ---------      ---------      ---abcde-
         * --------a      ---------      ---------
         * --------b  =>  ---a-----  =>  ---------
         * --------c      --ab-----      ---------
         * --------d      -abc-----      ---------
         * --------e      abcd-----      ---------
         *                bcde-----
         *                        a
         *
         *   hi
         * --------f                                    ---abcdef
         * ---------                                =>  ---------
         * ---------                                    ---------
         */
        template <int Index>
        struct BlackLanceAttack<3, Index> {
          static BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = BlackLanceAttackBase<Index>::make_table();
            constexpr auto affected_bb = table[0] & ~bitboard::rank1;
            constexpr auto magic = 0x0040100401004000ULL >> (pos::get_file(Index) - 1);
            constexpr auto shift_width = pos::get_file(Index) - 1;
            auto bb = occ & affected_bb;
            return table[((bb.lo * magic) >> 58) | (bb.hi >> shift_width)];
          }
        };

        /**
         * LogicType = 4: Low and high multiply
         *
         * e.g.
         *   lo * 0x0040100401004000ULL (2^54 + 2^44 + 2^34 + 2^24 + 1^14) ... (a)
         * ---------      ---------
         * --------a      ---------
         * --------b  =>  ---a-----
         * --------c      --ab-----
         * --------d      -abc-----
         * --------e      abcd-----
         *                bcde-----
         *                        a
         *
         *   hi * 0x0401000000000000ULL (2^58 + 2^48) + (a) >> 57
         * --------f      ---------      ---------      --abcdefg
         * --------g      ---------      ---------      ---------
         * ---------  =>  ---------  =>  ---a-----  =>  ---------
         *                ---------      --ab-----      ---------
         *                ---------      -abc-----      ---------
         *                -----f---      abcd-f---      ---------
         *                ----fg---      bcdefg---      ---------
         *                        -              a              -
         */
        template <int Index>
        struct BlackLanceAttack<4, Index> {
          static BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = BlackLanceAttackBase<Index>::make_table();
            constexpr auto affected_bb = table[0] & ~bitboard::rank1;
            constexpr auto magic_lo = 0x0040100401004000ULL >> (pos::get_file(Index) - 1);
            constexpr auto magic_hi = 0x0401000000000000ULL >> (pos::get_file(Index) - 1);
            auto bb = occ & affected_bb;
            return table[(bb.lo * magic_lo | bb.hi * magic_hi) >> 57];
          }
        };

        //
        // Generate arrays of function pointers to each index.
        //
        template <int... Is>
        constexpr auto generate_blance_fp(util::seq<Is...>)
          -> util::Array<decltype(&BlackLanceAttack<0, 0>::get_attack), sizeof...(Is)> {
          return {{ &BlackLanceAttack<BlackLanceAttackBase<Is>::logic_type, Is>::get_attack... }};
        }

        constexpr auto generate_blance_fp() -> decltype(generate_blance_fp(util::gen_seq<81>{})) {
          return generate_blance_fp(util::gen_seq<81>{});
        }

      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_LANCE_BLACK_HPP_INCLUDED