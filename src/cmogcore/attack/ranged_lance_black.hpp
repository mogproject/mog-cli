#ifndef MOG_CORE_ATTACK_RANGED_LANCE_BLACK_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_LANCE_BLACK_HPP_INCLUDED

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
        constexpr BitBoard make_blance_table(int const index, size_t const mask) {
          return BitBoard().set_repeat(
            pos::get_file(index), pos::get_rank(index), 0, -1, ntz(mask) + 1);
        }

/** fixed attack bitboard */
#define BLACK_LANCE_FIXED(z, n, text) BitBoard text##n(BitBoard const& notuse) { \
          constexpr auto bb = BitBoard().set_repeat(pos::get_file(n), pos::get_rank(n), 0, -1, 8); \
          return bb; \
        }


#define BLACK_LANCE_RANK_1(z, n, text) BLACK_LANCE_FIXED(z, n, text)
#define BLACK_LANCE_RANK_2(z, n, text) BLACK_LANCE_FIXED(z, n, text)

/*
 * e.g.
 *   lo >> 9
 * ---------      --------a
 * --------a      ---------
 * ---------  =>  ---------
 * ---------      ---------
 * ---------      ---------
 * ---------      ---------
 */
#define BLACK_LANCE_RANK_3(z, n, text) inline BitBoard text##n(BitBoard const& occ) { \
          constexpr auto table = util::transform<1 << (pos::get_rank(n) - 2)>(util::bind1st(&make_blance_table, n)); \
          constexpr auto affected_bb = table[0] & ~bitboard::rank1; \
          return table[(occ & affected_bb).lo >> BOOST_PP_ADD(POS_INDEX_TO_FILE(n), 8)]; \
        }

/*
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
/*
  for debug
          std::cout << n << ": " << bitboard::repr(table[0]) << " " << bitboard::repr(table[(1 << (pos::get_rank(n) - 2)) - 1]) << std::endl; \
          std::cout << n << ": occ = " << bitboard::repr(occ) << std::endl; \
          std::cout << n << ": occ & max_attack = " << bitboard::repr(occ & max_attack) << std::endl; \
          std::cout << n << ": (occ & max_attack).lo = " << (occ & max_attack).lo << std::endl; \
          std::cout << n << ": (occ & max_attack).lo * magic = " << ((occ & max_attack).lo * magic) << std::endl; \
          std::cout << n << ": magic :" << (((occ & max_attack).lo * magic) >> BOOST_PP_SUB(66, POS_INDEX_TO_RANK(n))) << std::endl; \
 */
#define BLACK_LANCE_MAGIC_LOW(z, n, text) inline BitBoard text##n(BitBoard const& occ) { \
          constexpr auto table = util::transform<1 << (pos::get_rank(n) - 2)>(util::bind1st(&make_blance_table, n)); \
          constexpr auto affected_bb = table[0] & ~bitboard::rank1; \
          constexpr auto magic = 0x0040100401004000ULL >> (pos::get_file(n) - 1); \
          return table[((occ & affected_bb).lo * magic) >> BOOST_PP_SUB(66, POS_INDEX_TO_RANK(n))]; \
        }

#define BLACK_LANCE_RANK_4(z, n, text) BLACK_LANCE_MAGIC_LOW(z, n, text)
#define BLACK_LANCE_RANK_5(z, n, text) BLACK_LANCE_MAGIC_LOW(z, n, text)
#define BLACK_LANCE_RANK_6(z, n, text) BLACK_LANCE_MAGIC_LOW(z, n, text)
#define BLACK_LANCE_RANK_7(z, n, text) BLACK_LANCE_MAGIC_LOW(z, n, text)

/*
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
#define BLACK_LANCE_RANK_8(z, n, text) inline BitBoard text##n(BitBoard const& occ) { \
          constexpr auto table = util::transform<1 << (pos::get_rank(n) - 2)>(util::bind1st(&make_blance_table, n)); \
          constexpr auto affected_bb = table[0] & ~bitboard::rank1; \
          constexpr auto magic = 0x0040100401004000ULL >> (pos::get_file(n) - 1); \
          auto bb = occ & affected_bb; \
          return table[((bb.lo * magic) >> 58) | (bb.hi >> BOOST_PP_SUB(POS_INDEX_TO_FILE(n), 1))]; \
        }

/*
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
#define BLACK_LANCE_RANK_9(z, n, text) inline BitBoard text##n(BitBoard const& occ) { \
          constexpr auto table = util::transform<1 << (pos::get_rank(n) - 2)>(util::bind1st(&make_blance_table, n)); \
          constexpr auto affected_bb = table[0] & ~bitboard::rank1; \
          constexpr auto magic_lo = 0x0040100401004000ULL >> (pos::get_file(n) - 1); \
          constexpr auto magic_hi = 0x0401000000000000ULL >> (pos::get_file(n) - 1); \
          auto bb = occ & affected_bb; \
          return table[(bb.lo * magic_lo | bb.hi * magic_hi) >> 57]; \
        }

#define MAKE_BLACK_LANCE(z, n, text) BOOST_PP_CAT(BLACK_LANCE_RANK_, POS_INDEX_TO_RANK(n))(z, n, text)

        BOOST_PP_REPEAT(81, MAKE_BLACK_LANCE, attack_black_lance_);
      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_LANCE_BLACK_HPP_INCLUDED