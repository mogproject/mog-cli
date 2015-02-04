#ifndef MOG_CORE_ATTACK_RANGED_LANCE_WHITE_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_LANCE_WHITE_HPP_INCLUDED

#include <array>
#include <boost/preprocessor.hpp>
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
        constexpr BitBoard make_wlance_table(int const index, size_t const mask) {
          return BitBoard().set_repeat(
            pos::get_file(index), pos::get_rank(index), 0, 1, ntz(mask) + 1);
        }

// todo: refactor to be DRY
/** fixed attack bitboard */
#define WHITE_LANCE_FIXED(z, n, text) BitBoard text##n(BitBoard const& notuse) { \
          constexpr auto bb = BitBoard().set_repeat(pos::get_file(n), pos::get_rank(n), 0, 1, 8); \
          return bb; \
        }

/*
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
#define WHITE_LANCE_MAGIC_LOW(z, n, text) inline BitBoard text##n(BitBoard const& occ) { \
          constexpr auto table = util::transform<1 << (8 - pos::get_rank(n))>(util::bind1st(&make_wlance_table, n)); \
          constexpr auto magic_lo = 0x0001010101010000ULL >> (pos::get_file(n) - 1); \
          constexpr auto magic_hi = 0x4040000000000000ULL >> (pos::get_file(n) - 1); \
          constexpr auto affected_bb = table[0] & ~bitboard::rank9; \
          auto bb = occ & affected_bb; \
          return table[(bb.hi * magic_hi | bb.lo * magic_lo) >> BOOST_PP_ADD(56, POS_INDEX_TO_RANK(n))]; \
        }

#define WHITE_LANCE_RANK_1(z, n, text) WHITE_LANCE_MAGIC_LOW(z, n, text)
#define WHITE_LANCE_RANK_2(z, n, text) WHITE_LANCE_MAGIC_LOW(z, n, text)
#define WHITE_LANCE_RANK_3(z, n, text) WHITE_LANCE_MAGIC_LOW(z, n, text)
#define WHITE_LANCE_RANK_4(z, n, text) WHITE_LANCE_MAGIC_LOW(z, n, text)

/*
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
#define WHITE_LANCE_RANK_5(z, n, text) inline BitBoard text##n(BitBoard const& occ) { \
          constexpr auto table = util::transform<1 << (8 - pos::get_rank(n))>(util::bind1st(&make_wlance_table, n)); \
          constexpr auto magic = 0x4040000000000000ULL >> (pos::get_file(n) - 1); \
          constexpr auto affected_bb = table[0] & ~bitboard::rank9; \
          auto bb = occ & affected_bb; \
          return table[((bb.hi * magic) >> 61) | (bb.lo >> BOOST_PP_ADD(POS_INDEX_TO_FILE(n), 44))]; \
        }

/*
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
#define WHITE_LANCE_RANK_6(z, n, text) inline BitBoard text##n(BitBoard const& occ) { \
          constexpr auto table = util::transform<1 << (8 - pos::get_rank(n))>(util::bind1st(&make_wlance_table, n)); \
          constexpr auto magic = 0x4040000000000000ULL >> (pos::get_file(n) - 1); \
          constexpr auto affected_bb = table[0] & ~bitboard::rank9; \
          return table[((occ & affected_bb).hi * magic) >> 62]; \
        }

/*
 * e.g.
 *   hi             >> 9
 * ---------      --------a
 * --------a      ---------
 * ---------  =>  ---------
 */
#define WHITE_LANCE_RANK_7(z, n, text) inline BitBoard text##n(BitBoard const& occ) { \
          constexpr auto table = util::transform<1 << (8 - pos::get_rank(n))>(util::bind1st(&make_wlance_table, n)); \
          constexpr auto affected_bb = table[0] & ~bitboard::rank9; \
          return table[(occ & affected_bb).hi >> BOOST_PP_ADD(POS_INDEX_TO_FILE(n), 8)]; \
        }

#define WHITE_LANCE_RANK_8(z, n, text) WHITE_LANCE_FIXED(z, n, text)
#define WHITE_LANCE_RANK_9(z, n, text) WHITE_LANCE_FIXED(z, n, text)

#define MAKE_WHITE_LANCE(z, n, text) BOOST_PP_CAT(WHITE_LANCE_RANK_, POS_INDEX_TO_RANK(n))(z, n, text)

        BOOST_PP_REPEAT(81, MAKE_WHITE_LANCE, attack_white_lance_);
      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_LANCE_WHITE_HPP_INCLUDED