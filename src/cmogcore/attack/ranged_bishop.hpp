#ifndef MOG_CORE_ATTACK_RANGED_BISHOP_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_BISHOP_HPP_INCLUDED

#include "../util.hpp"
#include "../bitboard.hpp"
#include "direct.hpp"
#include "ranged_base.hpp"


namespace mog {
  namespace core {
    namespace attack {
      namespace ranged {
        //
        // Bishop magic table
        //
        constexpr Magic bishop_magic_table[] = {
          { 0x0002010080402000ULL, 59, 0x0100800000000000ULL, 57, 0, 0xfffffffff0123456ULL },  // P11 (index: 0)
          { 0x0001008040201000ULL, 59,                  1ULL,  2, 0, 0xffffffffff012345ULL },
          { 0x0001002020100800ULL, 58,                  0ULL,  0, 0, 0xffffffffff213450ULL },
          { 0x0000810010080000ULL, 58,                  0ULL,  0, 0, 0xffffffffff253401ULL },
          { 0x0000408210000000ULL, 58,                  0ULL,  0, 0, 0xffffffffff254013ULL },
          { 0x0000204102000000ULL, 58,                  0ULL,  0, 0, 0xffffffffff250134ULL },
          { 0x0000102081020000ULL, 58,                  0ULL,  0, 0, 0xffffffffff201345ULL },
          { 0x0000102040810000ULL, 59,                  1ULL, -4, 0, 0xffffffffff012345ULL },
          { 0x0000081020408000ULL, 59, 0x1020000000000000ULL, 57, 0, 0xfffffffff0123456ULL },
          { 0x0000020100804000ULL, 60, 0x0201000000000000ULL, 58, 0, 0xffffffffff012345ULL },  // P12 (index: 9)
          { 0x0000010080402000ULL, 60, 0x0100800000000000ULL, 58, 0, 0xffffffffff012345ULL },
          { 0x0000010020201000ULL, 59,                  1ULL,  2, 0, 0xffffffffff213450ULL },
          { 0x0000004080080400ULL, 58,                  0ULL,  0, 0, 0xffffffffff253401ULL },
          { 0x0000002041080000ULL, 58,                  0ULL,  0, 0, 0xffffffffff254013ULL },
          { 0x0000001020810000ULL, 58,                  0ULL,  0, 0, 0xffffffffff250134ULL },
          { 0x0000001020810000ULL, 59,                  1ULL, -4, 0, 0xffffffffff201345ULL },
          { 0x0000001020408000ULL, 60, 0x1020000000000000ULL, 58, 0, 0xffffffffff012345ULL },
          { 0x0000000810204000ULL, 60, 0x0810000000000000ULL, 58, 0, 0xffffffffff012345ULL },
          { 0x0020000100804000ULL, 60, 0x0402000000000000ULL, 58, 0, 0xffffffffff301245ULL },  // P13 (index:18)
          { 0x0010000080402000ULL, 60, 0x0201000000000000ULL, 58, 0, 0xffffffffff301245ULL },
          { 0x0001000080402000ULL, 58, 0x0100800000000000ULL, 56, 0, 0xffffffff23456710ULL },
          { 0x0000400081021000ULL, 57,                  1ULL,  0, 0, 0xffffffff25167340ULL },
          { 0x0000200080410010ULL, 56,                  0ULL,  0, 0, 0xffffffff37205461ULL },
          { 0x0000100040082000ULL, 57,                  1ULL, -6, 0, 0xffffffff26541370ULL },
          { 0x0000100008408000ULL, 58, 0x1020000000000000ULL, 56, 0, 0xffffffff23145670ULL },
          { 0x0000200010204000ULL, 60, 0x0810000000000000ULL, 58, 0, 0xffffffffff123450ULL },
          { 0x0000100008102000ULL, 60, 0x0408000000000000ULL, 58, 0, 0xffffffffff123450ULL },
          { 0x0010080000804000ULL, 60, 0x0804000000000000ULL, 58, 0, 0xffffffffff230145ULL },  // P14 (index:27)
          { 0x0008040000402000ULL, 60, 0x0402000000000000ULL, 58, 0, 0xffffffffff230145ULL },
          { 0x0004008000402000ULL, 58, 0x0201000000000000ULL, 56, 0, 0xffffffff25346710ULL },
          { 0x0000801000402000ULL, 56, 0x0100800000000000ULL, 54, 0, 0xffffff2567894301ULL },
          { 0x0000400800201000ULL, 54, 0x2100000000000000ULL, 62, 0, 0xffffff4789165023ULL },
          { 0x0000200400100800ULL, 54, 0x1020000000000000ULL, 62, 0, 0xffffff4789650123ULL },
          { 0x0000400800102000ULL, 58, 0x0810000000000000ULL, 56, 0, 0xffffffff25346701ULL },
          { 0x0000801000102000ULL, 60, 0x0408000000000000ULL, 58, 0, 0xffffffffff234501ULL },
          { 0x0000400800081000ULL, 60, 0x0204000000000000ULL, 58, 0, 0xffffffffff234501ULL },
          { 0x0008040200004000ULL, 60, 0x1008000000000000ULL, 58, 0, 0xffffffffff123045ULL },  // P15 (index:36)
          { 0x0004020100002000ULL, 60, 0x0804000000000000ULL, 58, 0, 0xffffffffff123045ULL },
          { 0x0002010040002000ULL, 58, 0x0402000000000000ULL, 56, 0, 0xffffffff24536710ULL },
          { 0x0000802010004000ULL, 54, 0x0400200000000000ULL, 59, 0, 0xffffff5689417032ULL },
          { 0x0008008004001000ULL, 52, 0x0201100000000000ULL, 58, 0, 0xffff6b3a52810479ULL },
          { 0x0002002004001000ULL, 54, 0x0508000000000000ULL, 61, 0, 0xffffff5892701346ULL },
          { 0x0004002004000800ULL, 58, 0x0408000000000000ULL, 56, 0, 0xffffffff25367014ULL },
          { 0x0002004008001000ULL, 60, 0x0204000000000000ULL, 58, 0, 0xffffffffff345012ULL },
          { 0x0001002004000800ULL, 60, 0x0102000000000000ULL, 58, 0, 0xffffffffff345012ULL },
          { 0x0004020100800000ULL, 60, 0x2010000000000000ULL, 58, 0, 0xffffffffff012345ULL },  // P16 (index:45)
          { 0x0002010080400000ULL, 60, 0x1008000000000000ULL, 58, 0, 0xffffffffff012345ULL },
          { 0x0001008020400000ULL, 59, 0x1002000000000000ULL, 56, 0, 0xffffffff21347650ULL },
          { 0x0000801040080000ULL, 55, 0x2004020000000000ULL, 54, 0, 0xffffff4758019623ULL },
          { 0x0000100100804000ULL, 54, 0x0408040000000000ULL, 57, 0, 0xffffff1236045879ULL },
          { 0x0010020020040000ULL, 54, 0x0102800000000000ULL, 60, 0, 0xffffff6923014578ULL },
          { 0x0010020020040000ULL, 56, 0x0102000000000000ULL, 61, 0, 0xffffffff52013467ULL },
          { 0x0008010020040000ULL, 60, 0x0102000000000000ULL, 58, 0, 0xffffffffff450123ULL },
          { 0x0004008010020000ULL, 60, 0x0081000000000000ULL, 58, 0, 0xffffffffff450123ULL },
          { 0x0002010080402000ULL, 59,                  1ULL,  5, 0, 0xffffffffff012345ULL },  // P17 (index:54)
          { 0x0001008040201000ULL, 59,                  1ULL,  6, 0, 0xffffffffff012345ULL },
          { 0x0000804020081000ULL, 56, 0x0018000000000000ULL, 62, 0, 0xffffffff43567102ULL },
          { 0x0000002010400800ULL, 56, 0x000c000000000000ULL, 62, 0, 0xffffffff47561023ULL },
          { 0x0000000804100800ULL, 56, 0x0006000000000000ULL, 62, 0, 0xffffffff56410327ULL },
          { 0x0000080100100200ULL, 56, 0x0003000000000000ULL, 62, 0, 0xffffffff47102356ULL },
          { 0x0020040080080100ULL, 56, 0x0001800000000000ULL, 62, 0, 0xffffffff41023567ULL },
          { 0x0010020040080100ULL, 59,                  1ULL, 10, 0, 0xffffffffff501234ULL },
          { 0x0008010020040080ULL, 59,                  1ULL, 11, 0, 0xffffffffff501234ULL },
          { 0x0001008040201000ULL, 59,                  1ULL, -4, 0, 0xffffffffff501234ULL },  // P18 (index:63)
          { 0x0000804020100800ULL, 59,                  1ULL, -3, 0, 0xffffffffff501234ULL },
          { 0x0000004020100800ULL, 58, 0x3000000000000000ULL, 62, 0, 0xffffffffff123450ULL },
          { 0x0000000020104800ULL, 58, 0x1800000000000000ULL, 62, 0, 0xffffffffff134502ULL },
          { 0x0000000001102800ULL, 59, 0x1020000000000000ULL, 58, 0, 0xffffffffff034512ULL },
          { 0x0000000801001200ULL, 58, 0x0600000000000000ULL, 62, 0, 0xffffffffff130245ULL },
          { 0x0000100200400800ULL, 58, 0x0300000000000000ULL, 62, 0, 0xffffffffff102345ULL },
          { 0x0020040080100200ULL, 59,                  1ULL,  1, 0, 0xffffffffff501234ULL },
          { 0x0010020040080100ULL, 59,                  1ULL,  2, 0, 0xffffffffff501234ULL },
          { 0x0000804020100800ULL, 59, 0x2010000000000000ULL, 57, 0, 0xfffffffff5601234ULL },  // P19 (index:72)
          { 0x0000004020100800ULL, 60, 0x1008000000000000ULL, 58, 0, 0xffffffffff450123ULL },
          { 0x0000000020100800ULL, 61, 0x0408000000000000ULL, 58, 0, 0xffffffffff540123ULL },
          { 0x0000000000100800ULL, 58, 0x1402000000000000ULL, 60, 0, 0xffffffffff234501ULL },
          { 0x0000000000010800ULL, 58, 0x0a01000000000000ULL, 60, 0, 0xffffffffff235014ULL },
          { 0x0000000004008000ULL, 58, 0x0500800000000000ULL, 60, 0, 0xffffffffff230145ULL },
          { 0x0000000801002000ULL, 61, 0x0400800000000000ULL, 58, 0, 0xffffffffff534012ULL },
          { 0x0000100200400800ULL, 60, 0x0400800000000000ULL, 58, 0, 0xffffffffff450123ULL },
          { 0x0020040080100200ULL, 59, 0x0200400000000000ULL, 57, 0, 0xfffffffff5601234ULL },
        };

        //
        // Bishop attack
        //
        template <int Index>
        class BishopAttackBase {
         public:
          typedef RangedBase<Index, 2> Base;

          /** Magic traits */
          static constexpr auto magic = bishop_magic_table[Index];

          /** bitboard array for all variation */
          static constexpr auto variation_table = Base::make_variation_table(magic);
        };

        //
        // Derived class
        //
        template <bool Promoted, int Index>
        class BishopAttack {
         private:
          typedef BishopAttackBase<Index> Base;

         public:
          static constexpr auto make_table() {
            if (Promoted) {
              util::Array<BitBoard, Base::Base::variation_size> table = {{}};
              constexpr auto additional_bb = bb_table_direct[(Index << 5) + (turn::BLACK << 4) + ptype::KING];

              for (auto i = 0; i < Base::Base::variation_size; ++i) {
                table[i] = Base::variation_table[i] | additional_bb;
              }

              return table;
            } else {
              return Base::variation_table;
            }
          }

          static void save_table(std::string const& path) {
            constexpr auto table = make_table();
            Base::Base::save_variation_table(path, table);
          }

          /**
           * Return attack bitboard from occupancy bitboard.
           */
          static constexpr BitBoard get_attack(BitBoard const& occ) {
            constexpr auto magic = Base::magic;
            constexpr auto affected_bb = Base::Base::affected_bb;
            constexpr auto table = make_table();
            return table[magic.get_index(occ & affected_bb)];
          }
        };

        //
        // Generate array of function pointers to each index.
        //
        template <bool Promoted>
        struct BishopAttackGenerator {
          template <int... Is>
          static constexpr auto generate(util::seq<Is...>)
            -> util::Array<decltype(&BishopAttack<false, 0>::get_attack), sizeof...(Is)> {
            return {{ &BishopAttack<Promoted, Is>::get_attack... }};
          }

          static constexpr auto generate() {
            return generate(util::gen_seq<81>{});
          }
        };

        template <bool Promoted>
        struct BishopAttackSaverGenerator {
          template <int... Is>
          static constexpr auto generate(util::seq<Is...>)
            -> util::Array<decltype(&BishopAttack<false, 0>::save_table), sizeof...(Is)> {
            return {{ &BishopAttack<Promoted, Is>::save_table... }};
          }

          static constexpr auto generate() {
            return generate(util::gen_seq<81>{});
          }
        };

      }
    }
  }
}

#endif  // MOG_CORE_ATTACK_RANGED_BISHOP_HPP_INCLUDED
