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
        // Define calculation functions.
        //
        constexpr BitBoard make_blance_table(int const index, int const mask) {
          return BitBoard().set_repeat(
            pos::get_file(index), pos::get_rank(index), 0, -1, ntz(mask) + 1);
        }

        /** Number of the bitboard variation for each index. */
        constexpr int num_pattern(int const index) { return 1 << util::max(0, pos::get_rank(index) - 2); }

        /** Make array of the attack bitboards corresponding to each occupancy pattern. */
        template <int Index>
        constexpr auto make_table() {
          return util::array::iterate<num_pattern(Index)>(util::bind1st(&make_blance_table, Index));
        }

        /**
         * Fixed
         */
        template <int Index>
        BitBoard blance_magic_fixed(BitBoard const& occ) {
          constexpr auto bb = BitBoard().set_repeat(pos::get_file(Index), pos::get_rank(Index), 0, -1, 8);
          return bb;
        }

        /**
         * Low shift only
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
        BitBoard blance_magic_low_shift(BitBoard const& occ) {
          constexpr auto table = make_table<Index>();
          constexpr auto affected_bb_lo = (table[0] & ~bitboard::rank1).lo;
          constexpr auto shift_width = pos::get_file(Index) + 8;
          return table[(occ.lo & affected_bb_lo) >> shift_width];
        }

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
        BitBoard blance_magic_low_multiply(BitBoard const& occ) {
          constexpr auto table = make_table<Index>();
          constexpr auto affected_bb_lo = (table[0] & ~bitboard::rank1).lo;
          constexpr auto magic = 0x0040100401004000ULL >> (pos::get_file(Index) - 1);
          constexpr auto shift_width = util::min(63, 66 - pos::get_rank(Index));
          return table[((occ.lo & affected_bb_lo) * magic) >> shift_width];
        }

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
        BitBoard blance_magic_low_multiply_high_shift(BitBoard const& occ) {
          constexpr auto table = make_table<Index>();
          constexpr auto affected_bb = table[0] & ~bitboard::rank1;
          constexpr auto magic = 0x0040100401004000ULL >> (pos::get_file(Index) - 1);
          constexpr auto shift_width = pos::get_file(Index) - 1;
          auto bb = occ & affected_bb;
          return table[((bb.lo * magic) >> 58) | (bb.hi >> shift_width)];
        }

        /**
         * Low and high multiply
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
        BitBoard blance_magic_both_multiply(BitBoard const& occ) {
          constexpr auto table = make_table<Index>();
          constexpr auto affected_bb = table[0] & ~bitboard::rank1;
          constexpr auto magic_lo = 0x0040100401004000ULL >> (pos::get_file(Index) - 1);
          constexpr auto magic_hi = 0x0401000000000000ULL >> (pos::get_file(Index) - 1);
          auto bb = occ & affected_bb;
          return table[(bb.lo * magic_lo | bb.hi * magic_hi) >> 57];
        }

        /**
         * Return function pointer to each index.
         */
        //todo: refactor to single template function (reduce 81 x 5 instances -> 81)
        template <int Index>
        constexpr MagicCalculator blance_magic() {
          if (pos::get_rank(Index) <= 2) return &blance_magic_fixed<Index>;
          if (pos::get_rank(Index) <= 3) return &blance_magic_low_shift<Index>;
          if (pos::get_rank(Index) <= 7) return &blance_magic_low_multiply<Index>;
          if (pos::get_rank(Index) <= 8) return &blance_magic_low_multiply_high_shift<Index>;
          return &blance_magic_both_multiply<Index>;
        }

        template <int... Is>
        constexpr auto generate_blance_fp_impl(util::seq<Is...>)
          -> util::Array<decltype(blance_magic<0>()), sizeof...(Is)> {
          return {{ blance_magic<Is>()... }};
        }

        constexpr auto generate_blance_fp() -> decltype(generate_blance_fp_impl(util::gen_seq<81>{})) {
          return generate_blance_fp_impl(util::gen_seq<81>{});
        }

      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_LANCE_BLACK_HPP_INCLUDED