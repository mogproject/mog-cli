#ifndef MOG_CORE_ATTACK_RANGED_LANCE_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_LANCE_HPP_INCLUDED

#include "../util.hpp"
#include "../bitboard.hpp"

namespace mog {
  namespace core {
    namespace attack {
      namespace ranged {
        //
        // Base class
        //
        template <int Owner, int Index>
        class LanceAttackBase {
         public:
          /** File and rank (1-indexed) */
          static constexpr auto file = pos::get_file(Index);
          static constexpr auto rank = pos::get_rank(Index);

         private:
          /**
           * Number of the masking bits
           *
           * rank   1  2  3  4  5  6  7  8  9
           * black  0  0  1  2  3  4  5  6  7
           * white  7  6  5  4  3  2  1  0  0
           */
          static constexpr int __num_bits = util::max(0, (1 - Owner) * (rank - 2) + Owner * (8 - rank));

          /** Make attack bitboard with the specified mask */
          static constexpr BitBoard __make_table(int const mask) {
            return BitBoard().set_repeat(file, rank, 0, -1 + Owner * 2, ntz(mask) + 1);
          }

         public:
          /** Make bitboard array for all variation */
          static constexpr auto make_table() {
            return util::array::iterate<1 << __num_bits>(&__make_table);
          }

          static constexpr auto affected_bb() {
            return __make_table(0) & ~(bitboard::rank1.flip_by_turn(Owner));
          }

          /**
           * Return logic type
           *
           * rank   1  2  3  4  5  6  7  8  9
           * black  0  0  1  2  2  2  2  3  4
           * white  4  4  4  4  3  2  1  0  0
           */
          static constexpr int logic_type =
            Owner == turn::BLACK
              ? rank <= 7 ? rank <= 3 ? rank <= 2 ? 0 : 1 : 2 : rank <= 8 ? 3 : 4
              : rank <= 5 ? rank <= 4 ? 4 : 3 : rank <= 7 ? rank <= 6 ? 2 : 1 : 0;
        };

        //
        // Black lance
        //

        /**
         * LogicType = 0: Fixed
         */
        template <int Owner, int LogicType, int Index>
        struct LanceAttack {
          typedef LanceAttackBase<turn::BLACK, Index> Base;

          static constexpr BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = Base::make_table();
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
        struct LanceAttack<turn::BLACK, 1, Index> {
          typedef LanceAttackBase<turn::BLACK, Index> Base;

          static constexpr BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = Base::make_table();
            constexpr auto affected_bb_lo = Base::affected_bb().lo;
            return table[(occ.lo & affected_bb_lo) >> (Base::file + 8)];
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
        struct LanceAttack<turn::BLACK, 2, Index> {
          typedef LanceAttackBase<turn::BLACK, Index> Base;

          static constexpr BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = Base::make_table();
            constexpr auto affected_bb_lo = Base::affected_bb().lo;
            constexpr auto magic = 0x0040100401004000ULL >> (Base::file - 1);
            return table[((occ.lo & affected_bb_lo) * magic) >> (66 - Base::rank)];
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
        struct LanceAttack<turn::BLACK, 3, Index> {
          typedef LanceAttackBase<turn::BLACK, Index> Base;

          static constexpr BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = Base::make_table();
            constexpr auto affected_bb = Base::affected_bb();
            constexpr auto magic = 0x0040100401004000ULL >> (Base::file - 1);
            auto bb = occ & affected_bb;
            return table[((bb.lo * magic) >> 58) | (bb.hi >> (Base::file - 1))];
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
        struct LanceAttack<turn::BLACK, 4, Index> {
          typedef LanceAttackBase<turn::BLACK, Index> Base;

          static constexpr BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = Base::make_table();
            constexpr auto affected_bb = Base::affected_bb();
            constexpr auto magic_lo = 0x0040100401004000ULL >> (Base::file - 1);
            constexpr auto magic_hi = 0x0401000000000000ULL >> (Base::file - 1);
            auto bb = occ & affected_bb;
            return table[(bb.lo * magic_lo | bb.hi * magic_hi) >> 57];
          }
        };

        //
        // White lance
        //

        /**
         * LogicType = 0: Fixed
         */
        template <int LogicType, int Index>
        struct LanceAttack<turn::WHITE, LogicType, Index > {
          typedef LanceAttackBase<turn::WHITE, Index> Base;

          static constexpr BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = Base::make_table();
            return table[0];
          }
        };

        /**
         * LogicType = 1: High shift only
         *
         * e.g.
         *   hi             >> 9
         * ---------      --------a
         * --------a      ---------
         * ---------  =>  ---------
         */
        template <int Index>
        struct LanceAttack<turn::WHITE, 1, Index> {
          typedef LanceAttackBase<turn::WHITE, Index> Base;

          static constexpr BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = Base::make_table();
            constexpr auto affected_bb_hi = Base::affected_bb().hi;
            return table[(occ.hi & affected_bb_hi) >> (Base::file + 8)];
          }
        };

        /**
         * LogicType = 2: High multiply only
         *
         * e.g.
         *   hi * 0x4040000000000000ULL (2^62 + 2^54) >> 62
         * --------b      ---------      -------ab
         * --------a      ---------      ---------
         * ---------  =>  ---------  =>  ---------
         *                ---------
         *                ---------
         *                ---------
         *                b-------b
         *                        a
         */
        template <int Index>
        struct LanceAttack<turn::WHITE, 2, Index> {
          typedef LanceAttackBase<turn::WHITE, Index> Base;

          static constexpr BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = Base::make_table();
            constexpr auto affected_bb_hi = Base::affected_bb().hi;
            constexpr auto magic = 0x4040000000000000ULL >> (Base::file - 1);
            return table[((occ.hi & affected_bb_hi) * magic) >> 62];
          }
        };

        /*
         * LogicType = 3: Low shift and high multiply
         *
         * e.g.
         *   lo                            >> 45  ...(a)
         * ---------                     --------c
         * ---------                     ---------
         * ---------  =>                 ---------
         * ---------                     ---------
         * ---------                     ---------
         * --------c                     ---------
         *
         *   hi * 0x4040000000000000ULL (2^62 + 2^54) >> 61 + (a)
         * --------b      ---------      ------ab-      ------abc
         * --------a      ---------      ---------      ---------
         * ---------  =>  ---------  =>  ---------  =>  ---------
         *                ---------
         *                ---------
         *                ---------
         *                b-------b
         *                        a
         */
        template <int Index>
        struct LanceAttack<turn::WHITE, 3, Index> {
          typedef LanceAttackBase<turn::WHITE, Index> Base;

          static constexpr BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = Base::make_table();
            constexpr auto affected_bb = Base::affected_bb();
            constexpr auto magic = 0x4040000000000000ULL >> (Base::file - 1);
            auto bb = occ & affected_bb;
            return table[((bb.hi * magic) >> 61) | (bb.lo >> (Base::file + 44))];
          }
        };

        /**
         * LogicType = 4: Low and high multiply
         *
         * e.g.
         *   lo * 0x0001010101010000ULL (2^48 + 2^40 + 2^32 + 2^24 + 2^16)  ...(a)
         * ---------      ---------
         * --------g      ---------
         * --------f  =>  -g-------
         * --------e      -fg------
         * --------d      -efg-----
         * --------c      -defg----
         *                -cdefg---
         *                        -
         *
         *   hi * 0x4040000000000000ULL (2^62 + 2^54) + (a) >> 57
         * --------b      ---------      ---------      --abcdefg
         * --------a      ---------      ---------      ---------
         * ---------  =>  ---------  =>  -g-------  =>  ---------
         *                ---------      -fg------
         *                ---------      -efg-----
         *                ---------      -defg----
         *                b-------b      bcdefg--b
         *                        a              a
         */
        template <int Index>
        struct LanceAttack<turn::WHITE, 4, Index> {
          typedef LanceAttackBase<turn::WHITE, Index> Base;

          static constexpr BitBoard get_attack(BitBoard const& occ) {
            constexpr auto table = Base::make_table();
            constexpr auto affected_bb = Base::affected_bb();
            constexpr auto magic_lo = 0x0001010101010000ULL >> (Base::file - 1);
            constexpr auto magic_hi = 0x4040000000000000ULL >> (Base::file - 1);
            auto bb = occ & affected_bb;
            return table[(bb.hi * magic_hi | bb.lo * magic_lo) >> (Base::rank + 56)];
          }
        };

        //
        // Generate array of function pointers to each index.
        //

        template <int Owner>
        struct LanceAttackGenerator {
          template <int... Is>
          static constexpr auto generate(util::seq<Is...>)
            -> util::Array<decltype(&LanceAttack<Owner, 0, 0>::get_attack), sizeof...(Is)> {
            return {{ &LanceAttack<Owner, LanceAttackBase<Owner, Is>::logic_type, Is>::get_attack... }};
          }

          static constexpr auto generate() {
            return generate(util::gen_seq<81>{});
          }
        };

      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_LANCE_HPP_INCLUDED