#ifndef MOG_CORE_ATTACK_RANGED_BISHOP_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_BISHOP_HPP_INCLUDED

#include "../util.hpp"
#include "../bitboard.hpp"
#include "ranged_base.hpp"


namespace mog {
  namespace core {
    namespace attack {
      namespace ranged {
        //
        // Bishop attack
        //
        template <int Index>
        class BishopAttack {
         private:
          typedef RangedBase<Index> Base;

          /** four directions of bishop */
          static constexpr util::Array<std::pair<int, int>, 4> ds = {{ { -1, -1}, {-1, 1}, {1, -1}, {1, 1} }};

         public:
          static constexpr BitBoard get_max_attack() {
            auto bb = BitBoard();
            for (auto d: ds) {
              bb = bb.set_repeat(Base::file, Base::rank, d.first, d.second, 8);
            }
            return bb;
          }

          /** Make attack bitboard with the specified mask */
          static constexpr BitBoard make_attack(int const mask) {
            auto magic = get_magic();
            auto affected_bb = get_affected_bb();

            auto bb = BitBoard();
            int p = 0;

            for (auto d: ds) {
              bool stopped = false;

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

          static constexpr Magic __magic_table[] = {
            { 0x0002010080402000ULL, 59, 0x0100800000000000ULL, 57, 0, 0xfffffffff6543210ULL },  // P11 (index: 0)
            { 0x0001008040201000ULL, 59,                  1ULL,  2, 0, 0xffffffffff543210ULL },
            { 0x0001002020100800ULL, 58,                  0ULL,  0, 0, 0xffffffffff543120ULL },
            { 0x0000810010080000ULL, 58,                  0ULL,  0, 0, 0xffffffffff435210ULL },
            { 0x0000408210000000ULL, 58,                  0ULL,  0, 0, 0xffffffffff452310ULL },
            { 0x0000204102000000ULL, 58,                  0ULL,  0, 0, 0xffffffffff524310ULL },
            { 0x0000102081020000ULL, 58,                  0ULL,  0, 0, 0xffffffffff254310ULL },
            { 0x0000102040810000ULL, 59,                  1ULL, -4, 0, 0xffffffffff543210ULL },
            { 0x0000081020408000ULL, 59, 0x1020000000000000ULL, 57, 0, 0xfffffffff6543210ULL },
            { 0x0000020100804000ULL, 60, 0x0201000000000000ULL, 58, 0, 0xffffffffff543210ULL },  // P21 (index: 9)
            { 0x0000010080402000ULL, 60, 0x0100800000000000ULL, 58, 0, 0xffffffffff543210ULL },
            { 0x0000010020201000ULL, 59,                  1ULL,  2, 0, 0xffffffffff543120ULL },
            { 0x0000004080080400ULL, 58,                  0ULL,  0, 0, 0xffffffffff435210ULL },
            { 0x0000002041080000ULL, 58,                  0ULL,  0, 0, 0xffffffffff452310ULL },
            { 0x0000001020810000ULL, 58,                  0ULL,  0, 0, 0xffffffffff524310ULL },
            { 0x0000001020810000ULL, 59,                  1ULL, -4, 0, 0xffffffffff254310ULL },
            { 0x0000001020408000ULL, 60, 0x1020000000000000ULL, 58, 0, 0xffffffffff543210ULL },
            { 0x0000000810204000ULL, 60, 0x0810000000000000ULL, 58, 0, 0xffffffffff543210ULL },
            { 0x0020000100804000ULL, 60, 0x0402000000000000ULL, 58, 0, 0xffffffffff542103ULL },  // P31 (index:18)
            { 0x0010000080402000ULL, 60, 0x0201000000000000ULL, 58, 0, 0xffffffffff542103ULL },
            { 0x0001000080402000ULL, 58, 0x0100800000000000ULL, 56, 0, 0xffffffff76543210ULL },
            { 0x0000400081021000ULL, 57,                  1ULL,  0, 0, 0xffffffff76152430ULL },
            { 0x0000200080410010ULL, 56,                  0ULL,  0, 0, 0xffffffff02736451ULL },
            { 0x0000100040082000ULL, 57,                  1ULL, -6, 0, 0xffffffff56273140ULL },
            { 0x0000100008408000ULL, 58, 0x1020000000000000ULL, 56, 0, 0xffffffff32765410ULL },
            { 0x0000200010204000ULL, 60, 0x0810000000000000ULL, 58, 0, 0xffffffffff543210ULL },
            { 0x0000100008102000ULL, 60, 0x0408000000000000ULL, 58, 0, 0xffffffffff543210ULL },
            { 0x0010080000804000ULL, 60, 0x0804000000000000ULL, 58, 0, 0xffffffffff541032ULL },  // P41 (index:27)
            { 0x0008040000402000ULL, 60, 0x0402000000000000ULL, 58, 0, 0xffffffffff541032ULL },  // P42 (index:28)
            { 0x0004008000402000ULL, 58, 0x0201000000000000ULL, 56, 0, 0xffffffff76435210ULL },  // P43 (index:29)
            { 0x0000801000402000ULL, 56, 0x0100800000000000ULL, 54, 0, 0xffffff9876523410ULL },  // P44 (index:30)
            { 0x0000400800201000ULL, 54, 0x2100000000000000ULL, 62, 0, 0xffffff1987405632ULL },  // P45 (index:31)
            { 0x0000200400100800ULL, 54, 0x1020000000000000ULL, 62, 0, 0xffffff9874105632ULL },
            { 0x0000400800102000ULL, 58, 0x0810000000000000ULL, 56, 0, 0xffffffff52764310ULL },
            { 0x0000801000102000ULL, 60, 0x0408000000000000ULL, 58, 0, 0xffffffffff543210ULL },
            { 0x0000400800081000ULL, 60, 0x0204000000000000ULL, 58, 0, 0xffffffffff543210ULL },
            { 0x0008040200004000ULL, 60, 0x1008000000000000ULL, 58, 0, 0xffffffffff540321ULL },  // P51
            { 0x0004020100002000ULL, 60, 0x0804000000000000ULL, 58, 0, 0xffffffffff540321ULL },
            { 0x0002010040002000ULL, 58, 0x0402000000000000ULL, 56, 0, 0xffffffff76354210ULL },
            { 0x0000802010004000ULL, 54, 0x0400200000000000ULL, 59, 0, 0xffffff1498650723ULL },
            { 0x0008008004001000ULL, 52, 0x0201100000000000ULL, 58, 0, 0xffff25a3b6018974ULL },
            { 0x0002002004001000ULL, 54, 0x0508000000000000ULL, 61, 0, 0xffffff2985107643ULL },
            { 0x0004002004000800ULL, 58, 0x0408000000000000ULL, 56, 0, 0xffffffff52763410ULL },
            { 0x0002004008001000ULL, 60, 0x0204000000000000ULL, 58, 0, 0xffffffffff543210ULL },
            { 0x0001002004000800ULL, 60, 0x0102000000000000ULL, 58, 0, 0xffffffffff543210ULL },
            { 0x0004020100800000ULL, 60, 0x2010000000000000ULL, 58, 0, 0xffffffffff543210ULL },  // P61
            { 0x0002010080400000ULL, 60, 0x1008000000000000ULL, 58, 0, 0xffffffffff543210ULL },
            { 0x0001008020400000ULL, 59, 0x1002000000000000ULL, 56, 0, 0xffffffff67431250ULL },
            { 0x0000801040080000ULL, 55, 0x2004020000000000ULL, 54, 0, 0xffffff1085746932ULL },
            { 0x0000100100804000ULL, 54, 0x0408040000000000ULL, 57, 0, 0xffffff0632154978ULL },
            { 0x0010020020040000ULL, 54, 0x0102800000000000ULL, 60, 0, 0xffffff3296108754ULL },
            { 0x0010020020040000ULL, 56, 0x0102000000000000ULL, 61, 0, 0xffffffff25107643ULL },
            { 0x0008010020040000ULL, 60, 0x0102000000000000ULL, 58, 0, 0xffffffffff543210ULL },
            { 0x0004008010020000ULL, 60, 0x0081000000000000ULL, 58, 0, 0xffffffffff543210ULL },
            { 0x0002010080402000ULL, 59,                  1ULL,  5, 0, 0xffffffffff543210ULL },  // P71
            { 0x0001008040201000ULL, 59,                  1ULL,  6, 0, 0xffffffffff543210ULL },
            { 0x0000804020081000ULL, 56, 0x0018000000000000ULL, 62, 0, 0xffffffff17653402ULL },
            { 0x0000002010400800ULL, 56, 0x000c000000000000ULL, 62, 0, 0xffffffff16574032ULL },
            { 0x0000000804100800ULL, 56, 0x0006000000000000ULL, 62, 0, 0xffffffff14650723ULL },
            { 0x0000080100100200ULL, 56, 0x0003000000000000ULL, 62, 0, 0xffffffff17406532ULL },
            { 0x0020040080080100ULL, 56, 0x0001800000000000ULL, 62, 0, 0xffffffff14076532ULL },
            { 0x0010020040080100ULL, 59,                  1ULL, 10, 0, 0xffffffffff543210ULL },
            { 0x0008010020040080ULL, 59,                  1ULL, 11, 0, 0xffffffffff543210ULL },
            { 0x0001008040201000ULL, 59,                  1ULL, -4, 0, 0xffffffffff432105ULL },  // P81
            { 0x0000804020100800ULL, 59,                  1ULL, -3, 0, 0xffffffffff432105ULL },
            { 0x0000004020100800ULL, 58, 0x3000000000000000ULL, 62, 0, 0xffffffffff543210ULL },
            { 0x0000000020104800ULL, 58, 0x1800000000000000ULL, 62, 0, 0xffffffffff543120ULL },
            { 0x0000000001102800ULL, 59, 0x1020000000000000ULL, 58, 0, 0xffffffffff430215ULL },
            { 0x0000000801001200ULL, 58, 0x0600000000000000ULL, 62, 0, 0xffffffffff315420ULL },
            { 0x0000100200400800ULL, 58, 0x0300000000000000ULL, 62, 0, 0xffffffffff154320ULL },
            { 0x0020040080100200ULL, 59,                  1ULL,  1, 0, 0xffffffffff432105ULL },
            { 0x0010020040080100ULL, 59,                  1ULL,  2, 0, 0xffffffffff432105ULL },
            { 0x0000804020100800ULL, 59, 0x2010000000000000ULL, 57, 0, 0xfffffffff4321065ULL },  // P91
            { 0x0000004020100800ULL, 60, 0x1008000000000000ULL, 58, 0, 0xffffffffff321054ULL },
            { 0x0000000020100800ULL, 61, 0x0408000000000000ULL, 58, 0, 0xffffffffff210453ULL },
            { 0x0000000000100800ULL, 58, 0x1402000000000000ULL, 60, 0, 0xffffffffff543210ULL },
            { 0x0000000000010800ULL, 58, 0x0a01000000000000ULL, 60, 0, 0xffffffffff532410ULL },
            { 0x0000000004008000ULL, 58, 0x0500800000000000ULL, 60, 0, 0xffffffffff325410ULL },
            { 0x0000000801002000ULL, 61, 0x0400800000000000ULL, 58, 0, 0xffffffffff521043ULL },
            { 0x0000100200400800ULL, 60, 0x0400800000000000ULL, 58, 0, 0xffffffffff321054ULL },
            { 0x0020040080100200ULL, 59, 0x0200400000000000ULL, 57, 0, 0xfffffffff4321065ULL },
          };

          /** Make affected bitboard */
          static constexpr auto get_affected_bb() { return get_max_attack() & Base::affected_mask(); }

          /**
           * Get magic traits
           */
          static constexpr Magic get_magic() { return __magic_table[Index]; }

          /** Make bitboard array for all variation */
          static constexpr auto make_table() {
            constexpr int num_bits = get_affected_bb().count();
            return util::array::iterate<1 << num_bits>(&make_attack);
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

        struct BishopAttackGenerator {
          template <int... Is>
          static constexpr auto generate(util::seq<Is...>)
            -> util::Array<decltype(&BishopAttack<0>::get_attack), sizeof...(Is)> {
            return {{ &BishopAttack<Is>::get_attack... }};
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
