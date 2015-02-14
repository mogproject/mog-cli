#ifndef MOG_CORE_ATTACK_RANGED_ROOK_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_ROOK_HPP_INCLUDED

#include "../util.hpp"
#include "../bitboard.hpp"
#include "direct.hpp"
#include "ranged_base.hpp"


namespace mog {
  namespace core {
    namespace attack {
      namespace ranged {
        //
        // Rook attack
        //
        template <int Index>
        class RookAttackBase {
         public:
          typedef RangedBase<Index, 3> Base;

          /**
           * Calculate index of the table
           *
           * @param magic Static magic object
           * @param bb Intersect of the occupancy bitboard and affected area
           */
          inline static constexpr int get_index(Magic const& magic, BitBoard const& bb){

            // Use special magic formula for these 3 indices.
            if (Index == 0 || Index == 8 || Index == 26) {
              if (Index == 26) {
                return (
                  (rshift(bb.lo * magic.magic_lo, magic.shift_lo)) |
                  (rshift(bb.hi * magic.magic_hi, magic.shift_hi) << 11)
                ) >> magic.shift_final;
              }
              return (
                rshift((bb.lo >> 9) * magic.magic_lo, magic.shift_lo) |
                rshift((bb.lo << 55) | (bb.hi * magic.magic_hi), magic.shift_hi)
              ) >> magic.shift_final;
            }
            return magic.get_index(bb);
          }

         private:
          static constexpr Magic __magic_table[] = {
            { 0x8020080200800000ULL, 58, 0x8000020000000000ULL, 50, 0, 0xffcba98760d12345ULL },  // P11 (index: 0) Special formula
            { 0x0040080004000200ULL, 52, 0x4000020000000000ULL, 51, 0, 0xfff9876540c3b2a1ULL },
            { 0x0040040002000200ULL, 51, 0x1010000000000000ULL, 62, 0, 0xfffa9876105c3b24ULL },
            { 0x0040020001000200ULL, 51, 0x0808000000000000ULL, 62, 0, 0xfffa987106c3b245ULL },
            { 0x0040010000800200ULL, 51, 0x0404000000000000ULL, 62, 0, 0xfffa98107c3b2456ULL },
            { 0x0040008000400200ULL, 51, 0x0202000000000000ULL, 62, 0, 0xfffa9108c3b24567ULL },
            { 0x0040004000200200ULL, 52, 0x0200001000000000ULL, 51, 0, 0xfff90c8b2a134567ULL },
            { 0x0040200010000800ULL, 52, 0x0100000800000000ULL, 51, 0, 0xfff0cb2a19345678ULL },
            { 0x0080200802008000ULL, 58, 0x0080000200000000ULL, 50, 0, 0xff0d123456789abcULL },  // Special formula
            { 0x0000200004000200ULL, 51, 0x4040000000000000ULL, 62, 0, 0xfffa987654103b2cULL },  // P12 (index: 9)
            { 0x0000400800040400ULL, 53, 0x4000040000000000ULL, 52, 0, 0xffff9876540b32a1ULL },
            { 0x0000400400020400ULL, 53, 0x2000020000000000ULL, 52, 0, 0xffff987650b42a13ULL },
            { 0x0000400200010400ULL, 53, 0x1000010000000000ULL, 52, 0, 0xffff98760b52a134ULL },
            { 0x0000400100008400ULL, 53, 0x0800008000000000ULL, 52, 0, 0xffff9870b62a1345ULL },
            { 0x0000400080004400ULL, 53, 0x0400004000000000ULL, 52, 0, 0xffff980b72a13456ULL },
            { 0x0000400040002400ULL, 53, 0x0200002000000000ULL, 52, 0, 0xffff90b82a134567ULL },
            { 0x0000402000100008ULL, 53, 0x0100001000000000ULL, 52, 0, 0xffff0b2a19345678ULL },
            { 0x0000200008000400ULL, 51, 0x0040400000000000ULL, 62, 0, 0xfff10c3b2456789aULL },
            { 0x0000201000020000ULL, 51, 0x4040000000000000ULL, 62, 0, 0xfffa98765410b2c3ULL },  // P13 (index:18)
            { 0x0000202004000400ULL, 53, 0x4000040000000000ULL, 52, 0, 0xffff9876540b3a12ULL },
            { 0x0000204004100080ULL, 53, 0x2000020000000000ULL, 52, 0, 0xffffa98760b15243ULL },
            { 0x0000402001000080ULL, 53, 0x1000010000000000ULL, 52, 0, 0xffff98760b2a1345ULL },
            { 0x0000402000800040ULL, 53, 0x0800008000000000ULL, 52, 0, 0xffff9870b2a13456ULL },
            { 0x0000402000400020ULL, 53, 0x0400004000000000ULL, 52, 0, 0xffff980b2a134567ULL },
            { 0x0000402000200010ULL, 53, 0x0200002000000000ULL, 52, 0, 0xffff90b2a1345678ULL },
            { 0x0000008000404004ULL, 53, 0x0100001000000000ULL, 52, 0, 0xffff0b14356789a2ULL },
            { 0x0000001008000400ULL, 53, 0x0040400000000000ULL, 62, 0, 0xfffcba1923456780ULL },  // Special formula
            { 0x0020001008000100ULL, 51, 0x4040000000000000ULL, 62, 0, 0xfffa987654102cb3ULL },  // P14 (index:27)
            { 0x0010000804008000ULL, 53, 0x4000040000000000ULL, 52, 0, 0xffff7654320b8a91ULL },
            { 0x0000801020020080ULL, 53, 0x2000020000000000ULL, 52, 0, 0xffffa98760b12453ULL },
            { 0x0004001008008000ULL, 53, 0x1000010000000000ULL, 52, 0, 0xffff87650ba12394ULL },
            { 0x0002001008004000ULL, 53, 0x0800008000000000ULL, 52, 0, 0xffff8760ba123495ULL },
            { 0x0001001008002000ULL, 53, 0x0400004000000000ULL, 52, 0, 0xffff870ba1234596ULL },
            { 0x0000801008001000ULL, 53, 0x0200002000000000ULL, 52, 0, 0xffff80ba12345697ULL },
            { 0x0000800020001010ULL, 53, 0x0100001000000000ULL, 52, 0, 0xffff0b32456789a1ULL },
            { 0x0000200008000400ULL, 51, 0x0040400000000000ULL, 62, 0, 0xfff10c3456789ab2ULL },
            { 0x0000100008040000ULL, 52, 0x8000040000000000ULL, 51, 0, 0xfff98765430cb1a2ULL },  // P15 (index:36)
            { 0x0010040004020000ULL, 53, 0x4000040000000000ULL, 52, 0, 0xffff7654320ba981ULL },
            { 0x0000800808100080ULL, 53, 0x2000020000000000ULL, 52, 0, 0xffffa98760b14523ULL },
            { 0x0008000410080040ULL, 53, 0x1000010000000000ULL, 52, 0, 0xffff98760b134a25ULL },
            { 0x0004000210080020ULL, 53, 0x0800008000000000ULL, 52, 0, 0xffff9870b1345a26ULL },
            { 0x0002000110080010ULL, 53, 0x0400004000000000ULL, 52, 0, 0xffff980b13456a27ULL },
            { 0x0000400040080010ULL, 53, 0x0200002000000000ULL, 52, 0, 0xffff90b23456781aULL },
            { 0x0000800040100010ULL, 53, 0x0100001000000000ULL, 52, 0, 0xffff0b3456789a21ULL },
            { 0x0000400020080001ULL, 52, 0x0080000400000000ULL, 51, 0, 0xfff0c1456789ab32ULL },
            { 0x0040000800040200ULL, 51, 0x4040000000000000ULL, 62, 0, 0xfffa98765410c2b3ULL },  // P16 (index:45)
            { 0x0000802008020800ULL, 52, 0x2020000000000000ULL, 62, 0, 0xffffba9876105432ULL },
            { 0x0008000400040200ULL, 53, 0x2000020000000000ULL, 52, 0, 0xffff876540b291a3ULL },
            { 0x0004000200040200ULL, 53, 0x1000010000000000ULL, 52, 0, 0xffff87650b2391a4ULL },
            { 0x0002000100040200ULL, 53, 0x0800008000000000ULL, 52, 0, 0xffff8760b23491a5ULL },
            { 0x0001000080040200ULL, 53, 0x0400004000000000ULL, 52, 0, 0xffff870b234591a6ULL },
            { 0x0000800040040200ULL, 53, 0x0200002000000000ULL, 52, 0, 0xffff80b2345691a7ULL },
            { 0x0000800080200800ULL, 52, 0x0080800000000000ULL, 62, 0, 0xffff1056789ab432ULL },
            { 0x0000200010000200ULL, 51, 0x0040400000000000ULL, 62, 0, 0xfff10456789ab3c2ULL },
            { 0x0040100401004000ULL, 58, 0x0100040000000000ULL, 51, 0, 0xfffcba9876054321ULL },  // P17 (index:54)
            { 0x0020080200802000ULL, 58, 0x0100040000000000ULL, 52, 0, 0xffffba9876054321ULL },
            { 0x0010020080200800ULL, 57, 0x0100020000000000ULL, 52, 0, 0xffffba9870564321ULL },
            { 0x0008004010040100ULL, 56, 0x0100100000000000ULL, 52, 0, 0xffffba9845673210ULL },
            { 0x0004010040100400ULL, 56, 0x1000800000000000ULL, 52, 0, 0xffff21089ab76543ULL },
            { 0x0002000401004010ULL, 54, 0x0100040000000000ULL, 52, 0, 0xffffba4567893210ULL },
            { 0x0001004010040100ULL, 54, 0x2002010000000000ULL, 52, 0, 0xffff43ab01298765ULL },
            { 0x0000802008020080ULL, 58, 0x0200001000000000ULL, 52, 0, 0xffff06789ab54321ULL },
            { 0x0000401004010040ULL, 58, 0x0100000400000000ULL, 51, 0, 0xfff06789abc54321ULL },
            { 0x0040100401004000ULL, 59, 0x0100800000000000ULL, 51, 0, 0xfffcba9876432105ULL },  // P18 (index:63)
            { 0x0020080200802000ULL, 59, 0x0100800000000000ULL, 52, 0, 0xffffba9876432105ULL },
            { 0x0010040100401000ULL, 59, 0x0100800000000000ULL, 52, 0, 0xffffba9875432106ULL },
            { 0x0008020080200800ULL, 59, 0x0100800000000000ULL, 52, 0, 0xffffba9856432107ULL },
            { 0x0004010040100400ULL, 59, 0x0100800000000000ULL, 52, 0, 0xffffba9567432108ULL },
            { 0x0002008020080100ULL, 56, 0x0004002000000000ULL, 52, 0, 0xffff1089ab765423ULL },
            { 0x0001004010020080ULL, 57, 0x0002001000000000ULL, 52, 0, 0xffff0789ab654213ULL },
            { 0x0000802004010040ULL, 58, 0x0001000000000000ULL, 52, 0, 0xffff6789ab542103ULL },
            { 0x0000400802008020ULL, 58, 0x0000800000000000ULL, 51, 0, 0xfff6789abc532104ULL },
            { 0x0040100401004000ULL, 59, 0x0100404000000000ULL, 50, 0, 0xffdcba9874321065ULL },  // P19 (index:72)
            { 0x0020080200802000ULL, 59, 0x0100404000000000ULL, 51, 0, 0xfffcba9874321065ULL },
            { 0x0010040100401000ULL, 59, 0x0100204000000000ULL, 51, 0, 0xfffcba9864321075ULL },
            { 0x0008020080200800ULL, 54, 0x0400080020000000ULL, 51, 0, 0xfff3210bc98765a4ULL },
            { 0x0004010040100400ULL, 58, 0x0100004000000000ULL, 51, 0, 0xfffcba6785432190ULL },
            { 0x0002008020080100ULL, 58, 0x0100004000000000ULL, 51, 0, 0xfffcb678954320a1ULL },
            { 0x0001004010020080ULL, 58, 0x0100004000000000ULL, 51, 0, 0xfffc6789a54310b2ULL },
            { 0x0000802004010040ULL, 58, 0x0100004000000000ULL, 51, 0, 0xfff6789ab54210c3ULL },
            { 0x0000401004010040ULL, 59, 0x0001004000000000ULL, 50, 0, 0xff789abcd4321065ULL },
          };

         public:
          /** Get magic traits */
          inline static constexpr Magic get_magic() { return __magic_table[Index]; }

          /** Make attack bitboard with the specified mask */
          static constexpr BitBoard make_attack(int const mask) {
            auto magic = get_magic();
            auto affected_bb = Base::affected_bb;

            auto bb = BitBoard();
            int p = 0;

            for (auto d: Base::directions) {
              bool stopped = false;

              // todo: be more efficient
              for (int i = 1; i <= 8; ++i) {
                int f = Base::file + d.first * i;
                int r = Base::rank + d.second * i;
                if (pos::make_pos(f, r) < 0) break;

                if (!stopped) bb = bb.set(f, r);
                if ((mask >> magic.get_mapping(p)) & 1) stopped = true;
                if (affected_bb.get(f, r)) ++p;
              }
            }

            return bb;
          }

          /** bitboard array for all variation */
          static constexpr auto variation_table = util::array::iterate<Base::variation_size>(&make_attack);

        };

        //
        // Derived class
        //
        template <bool Promoted, int Index>
        class RookAttack {
         private:
          typedef RookAttackBase<Index> Base;

         public:
          static constexpr auto make_table() {
            util::Array<BitBoard, Base::Base::variation_size> table = {{}};
            constexpr auto additional_bb =
              Promoted ? bb_table_direct[(Index << 5) + (turn::BLACK << 4) + ptype::KING] : BitBoard();

            for (auto i = 0; i < Base::Base::variation_size; ++i) {
              table[i] = Base::variation_table[i] | additional_bb;
            }

            return table;
          }

          /**
           * Return attack bitboard from occupancy bitboard.
           */
          static constexpr BitBoard get_attack(BitBoard const& occ) {
            constexpr auto magic = Base::get_magic();
            constexpr BitBoard affected_bb = Base::Base::affected_bb;
            constexpr auto table = make_table();
            return table[Base::get_index(magic, occ & affected_bb)];
          }
        };

        //
        // Generate array of function pointers to each index.
        //

        template <bool Promoted>
        struct RookAttackGenerator {
          template <int... Is>
          static constexpr auto generate(util::seq<Is...>)
            -> util::Array<decltype(&RookAttack<false, 0>::get_attack), sizeof...(Is)> {
            return {{ &RookAttack<Promoted, Is>::get_attack... }};
          }

          static constexpr auto generate() {
            return generate(util::gen_seq<81>{});
          }
        };

      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_ROOK_HPP_INCLUDED
