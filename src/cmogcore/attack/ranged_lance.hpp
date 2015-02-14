#ifndef MOG_CORE_ATTACK_RANGED_LANCE_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_LANCE_HPP_INCLUDED

#include "../util.hpp"
#include "../bitboard.hpp"
#include "ranged_base.hpp"


namespace mog {
  namespace core {
    namespace attack {
      namespace ranged {
        //
        // Lance attack
        //
        template <int Owner, int Index>
        class LanceAttack {
         private:
          typedef RangedBase<Index, Owner> Base;

          /** Make attack bitboard with the specified mask */
          static constexpr BitBoard __make_attack(int const mask) {
            return BitBoard().set_repeat(Base::file, Base::rank, 0, -1 + Owner * 2, ntz(mask) + 1);
          }

         public:
          /** Make affected bitboard */
          static constexpr auto get_affected_bb() { return __make_attack(0) & Base::affected_mask; }

          /**
           * Get magic traits
           */
          static constexpr Magic get_magic() {
            constexpr auto m1 = 0x0040100401004000ULL >> (Base::file - 1);
            constexpr auto m2 = 0x4040000000000000ULL >> (Base::file - 1);

            switch (Owner * 10 + Base::rank) {
              // black lance
              case  3:
                // Low shift only
                //
                // e.g.
                //   lo >> 9
                // ---------      --------a
                // --------a      ---------
                // ---------  =>  ---------
                // ---------      ---------
                // ---------      ---------
                // ---------      ---------
                //
                return { 1ULL, 0, 0ULL, 0, Base::file + 8 }; break;
              case  4: case  5: case  6: case  7:
                // Low multiply only
                //
                // e.g.
                //   lo * 0x0040100401004000ULL (2^54 + 2^44 + 2^34 + 2^24 + 2^14) >> 59
                // ---------      ---------      ----abcde
                // --------a      ---------      ---------
                // --------b  =>  ---a-----  =>  ---------
                // --------c      --ab-----      ---------
                // --------d      -abc-----      ---------
                // --------e      abcd-----      ---------
                //                bcde-----
                //                        a
                //
                return { m1, 0, 0ULL, 0, 66 - Base::rank }; break;
              case  8:
                // Low multiply and high shift
                //
                // e.g.
                //   lo * 0x0040100401004000ULL (2^54 + 2^44 + 2^34 + 2^24 + 1^14) >> 58
                // ---------      ---------      ---abcde-
                // --------a      ---------      ---------
                // --------b  =>  ---a-----  =>  ---------
                // --------c      --ab-----      ---------
                // --------d      -abc-----      ---------
                // --------e      abcd-----      ---------
                //                bcde-----
                //                        a
                //
                //   hi
                // --------f                                    ---abcdef
                // ---------                                =>  ---------
                // ---------                                    ---------
                //
                return { m1, 58, 1ULL, Base::file - 1, 0 }; break;
              case  9:
                // Low and high multiply
                //
                // e.g.
                //   lo * 0x0040100401004000ULL (2^54 + 2^44 + 2^34 + 2^24 + 1^14) ... (a)
                // ---------      ---------
                // --------a      ---------
                // --------b  =>  ---a-----
                // --------c      --ab-----
                // --------d      -abc-----
                // --------e      abcd-----
                //                bcde-----
                //                        a
                //
                //   hi * 0x0401000000000000ULL (2^58 + 2^48) + (a) >> 57
                // --------f      ---------      ---------      --abcdefg
                // --------g      ---------      ---------      ---------
                // ---------  =>  ---------  =>  ---a-----  =>  ---------
                //                ---------      --ab-----      ---------
                //                ---------      -abc-----      ---------
                //                -----f---      abcd-f---      ---------
                //                ----fg---      bcdefg---      ---------
                //                        -              a              -
                //
                return { m1, 0, 0x0401000000000000ULL >> (Base::file - 1), 0, 57, 0ULL }; break;
              // white lance
              case 11: case 12: case 13: case 14:
                // Low and high multiply
                //
                // e.g.
                //   lo * 0x0001010101010000ULL (2^48 + 2^40 + 2^32 + 2^24 + 2^16)  ...(a)
                // ---------      ---------
                // --------g      ---------
                // --------f  =>  -g-------
                // --------e      -fg------
                // --------d      -efg-----
                // --------c      -defg----
                //                -cdefg---
                //                        -
                //
                //   hi * 0x4040000000000000ULL (2^62 + 2^54) + (a) >> 57
                // --------b      ---------      ---------      --abcdefg
                // --------a      ---------      ---------      ---------
                // ---------  =>  ---------  =>  -g-------  =>  ---------
                //                ---------      -fg------
                //                ---------      -efg-----
                //                ---------      -defg----
                //                b-------b      bcdefg--b
                //                        a              a
                //
                return { 0x0001010101010000ULL >> (Base::file - 1), 0, m2, 0, Base::rank + 56, 0ULL }; break;
              case 15:
                // Low shift and high multiply
                //
                // e.g.
                //   lo                            >> 45  ...(a)
                // ---------                     --------c
                // ---------                     ---------
                // ---------  =>                 ---------
                // ---------                     ---------
                // ---------                     ---------
                // --------c                     ---------
                //
                //   hi * 0x4040000000000000ULL (2^62 + 2^54) >> 61 + (a)
                // --------b      ---------      ------ab-      ------abc
                // --------a      ---------      ---------      ---------
                // ---------  =>  ---------  =>  ---------  =>  ---------
                //                ---------
                //                ---------
                //                ---------
                //                b-------b
                //                        a
                //
                return { 1ULL, Base::file + 44, m2, 61, 0, 0ULL }; break;
              case 16:
                // High multiply only
                //
                // e.g.
                //   hi * 0x4040000000000000ULL (2^62 + 2^54) >> 62
                // --------b      ---------      -------ab
                // --------a      ---------      ---------
                // ---------  =>  ---------  =>  ---------
                //                ---------
                //                ---------
                //                ---------
                //                b-------b
                //                        a
                //
                return { 0ULL, 0, m2, 0, 62, 0ULL}; break;
              case 17:
                // High shift only
                //
                // e.g.
                //   hi             >> 9
                // ---------      --------a
                // --------a      ---------
                // ---------  =>  ---------
                //
                return { 0ULL, 0, 1ULL, 0, Base::file + 8, 0ULL}; break;
              default:
                //
                // Fixed
                //
                return { 0ULL, 0, 0ULL, 0, 0, 0ULL };
            }
          }

          /** Make bitboard array for all variation */
          static constexpr auto make_table() {
            return util::array::iterate<Base::variation_size>(&__make_attack);
          }

          /**
           * Return attack bitboard from occupancy bitboard.
           */
          static constexpr BitBoard get_attack(BitBoard const& occ) {
            constexpr auto magic = get_magic();
            constexpr auto affected_bb = get_affected_bb();
            constexpr auto table = make_table();
            return table[magic.get_index(occ & affected_bb)];
          }

        };

        //
        // Generate array of function pointers to each index.
        //

        template <int Owner>
        struct LanceAttackGenerator {
          template <int... Is>
          static constexpr auto generate(util::seq<Is...>)
            -> util::Array<decltype(&LanceAttack<Owner, 0>::get_attack), sizeof...(Is)> {
            return {{ &LanceAttack<Owner, Is>::get_attack... }};
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