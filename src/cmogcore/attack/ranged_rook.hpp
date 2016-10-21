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
// Rook magic table
//
constexpr Magic rook_magic_table[] = {
    {0x8020080200800000ULL, 58, 0x8000020000000000ULL, 50, 0, 0xff6789abc54321d0ULL},  // P11 (index: 0) Special formula
    {0x0040080004000200ULL, 52, 0x4000020000000000ULL, 51, 0, 0xfff4567891a2b3c0ULL},
    {0x0040040002000200ULL, 51, 0x1010000000000000ULL, 62, 0, 0xfff6789a2b3c5014ULL},
    {0x0040020001000200ULL, 51, 0x0808000000000000ULL, 62, 0, 0xfff789a2b3c60154ULL},
    {0x0040010000800200ULL, 51, 0x0404000000000000ULL, 62, 0, 0xfff89a2b3c701654ULL},
    {0x0040008000400200ULL, 51, 0x0202000000000000ULL, 62, 0, 0xfff9a2b3c8017654ULL},
    {0x0040004000200200ULL, 52, 0x0200001000000000ULL, 51, 0, 0xfff91a2b8c076543ULL},
    {0x0040200010000800ULL, 52, 0x0100000800000000ULL, 51, 0, 0xfff91a2bc0876543ULL},
    {0x0080200802008000ULL, 58, 0x0080000200000000ULL, 50, 0, 0xff54321d0cba9876ULL},  // Special formula
    {0x0000200004000200ULL, 51, 0x4040000000000000ULL, 62, 0, 0xfff456789ac2b301ULL},  // P12 (index: 9)
    {0x0000400800040400ULL, 53, 0x4000040000000000ULL, 52, 0, 0xffff4567891a23b0ULL},
    {0x0000400400020400ULL, 53, 0x2000020000000000ULL, 52, 0, 0xffff567891a24b03ULL},
    {0x0000400200010400ULL, 53, 0x1000010000000000ULL, 52, 0, 0xffff67891a25b043ULL},
    {0x0000400100008400ULL, 53, 0x0800008000000000ULL, 52, 0, 0xffff7891a26b0543ULL},
    {0x0000400080004400ULL, 53, 0x0400004000000000ULL, 52, 0, 0xffff891a27b06543ULL},
    {0x0000400040002400ULL, 53, 0x0200002000000000ULL, 52, 0, 0xffff91a28b076543ULL},
    {0x0000402000100008ULL, 53, 0x0100001000000000ULL, 52, 0, 0xffff91a2b0876543ULL},
    {0x0000200008000400ULL, 51, 0x0040400000000000ULL, 62, 0, 0xfff2b3c01a987654ULL},
    {0x0000201000020000ULL, 51, 0x4040000000000000ULL, 62, 0, 0xfff456789ac2b013ULL},  // P13 (index:18)
    {0x0000202004000400ULL, 53, 0x4000040000000000ULL, 52, 0, 0xffff4567891a3b02ULL},
    {0x0000204004100080ULL, 53, 0x2000020000000000ULL, 52, 0, 0xffff6789a251b043ULL},
    {0x0000402001000080ULL, 53, 0x1000010000000000ULL, 52, 0, 0xffff67891a2b0435ULL},
    {0x0000402000800040ULL, 53, 0x0800008000000000ULL, 52, 0, 0xffff7891a2b05436ULL},
    {0x0000402000400020ULL, 53, 0x0400004000000000ULL, 52, 0, 0xffff891a2b065437ULL},
    {0x0000402000200010ULL, 53, 0x0200002000000000ULL, 52, 0, 0xffff91a2b0765438ULL},
    {0x0000008000404004ULL, 53, 0x0100001000000000ULL, 52, 0, 0xffff341b0a987652ULL},
    {0x0000001008000400ULL, 53, 0x0040400000000000ULL, 62, 0, 0xfff91abc87654320ULL},  // Special formula
    {0x0020001008000100ULL, 51, 0x4040000000000000ULL, 62, 0, 0xfff456789ac2013bULL},  // P14 (index:27)
    {0x0010000804008000ULL, 53, 0x4000040000000000ULL, 52, 0, 0xffff234567a8b019ULL},
    {0x0000801020020080ULL, 53, 0x2000020000000000ULL, 52, 0, 0xffff6789a21b0435ULL},
    {0x0004001008008000ULL, 53, 0x1000010000000000ULL, 52, 0, 0xffff56781ab03249ULL},
    {0x0002001008004000ULL, 53, 0x0800008000000000ULL, 52, 0, 0xffff6781ab043259ULL},
    {0x0001001008002000ULL, 53, 0x0400004000000000ULL, 52, 0, 0xffff781ab0543269ULL},
    {0x0000801008001000ULL, 53, 0x0200002000000000ULL, 52, 0, 0xffff81ab06543279ULL},
    {0x0000800020001010ULL, 53, 0x0100001000000000ULL, 52, 0, 0xffff23b09876541aULL},
    {0x0000200008000400ULL, 51, 0x0040400000000000ULL, 62, 0, 0xfff3c01a9876542bULL},
    {0x0000100008040000ULL, 52, 0x8000040000000000ULL, 51, 0, 0xfff3456789bc02a1ULL},  // P15 (index:36)
    {0x0010040004020000ULL, 53, 0x4000040000000000ULL, 52, 0, 0xffff234567ab0189ULL},
    {0x0000800808100080ULL, 53, 0x2000020000000000ULL, 52, 0, 0xffff6789a1b04325ULL},
    {0x0008000410080040ULL, 53, 0x1000010000000000ULL, 52, 0, 0xffff67891b04352aULL},
    {0x0004000210080020ULL, 53, 0x0800008000000000ULL, 52, 0, 0xffff7891b054362aULL},
    {0x0002000110080010ULL, 53, 0x0400004000000000ULL, 52, 0, 0xffff891b0654372aULL},
    {0x0000400040080010ULL, 53, 0x0200002000000000ULL, 52, 0, 0xffff92b076543a18ULL},
    {0x0000800040100010ULL, 53, 0x0100001000000000ULL, 52, 0, 0xffff3b098765412aULL},
    {0x0000400020080001ULL, 52, 0x0080000400000000ULL, 51, 0, 0xfff1c0a98765423bULL},
    {0x0040000800040200ULL, 51, 0x4040000000000000ULL, 62, 0, 0xfff456789a013b2cULL},  // P16 (index:45)
    {0x0000802008020800ULL, 52, 0x2020000000000000ULL, 62, 0, 0xffff6789ab012345ULL},
    {0x0008000400040200ULL, 53, 0x2000020000000000ULL, 52, 0, 0xffff45678b023a19ULL},
    {0x0004000200040200ULL, 53, 0x1000010000000000ULL, 52, 0, 0xffff5678b0324a19ULL},
    {0x0002000100040200ULL, 53, 0x0800008000000000ULL, 52, 0, 0xffff678b04325a19ULL},
    {0x0001000080040200ULL, 53, 0x0400004000000000ULL, 52, 0, 0xffff78b054326a19ULL},
    {0x0000800040040200ULL, 53, 0x0200002000000000ULL, 52, 0, 0xffff8b0654327a19ULL},
    {0x0000800080200800ULL, 52, 0x0080800000000000ULL, 62, 0, 0xffff01a98765234bULL},
    {0x0000200010000200ULL, 51, 0x0040400000000000ULL, 62, 0, 0xfff01a9876542c3bULL},
    {0x0040100401004000ULL, 58, 0x0100040000000000ULL, 51, 0, 0xfff6789abc012345ULL},  // P17 (index:54)
    {0x0020080200802000ULL, 58, 0x0100040000000000ULL, 52, 0, 0xffff6789ab012345ULL},
    {0x0010020080200800ULL, 57, 0x0100020000000000ULL, 52, 0, 0xffff789ab0512346ULL},
    {0x0008004010040100ULL, 56, 0x0100100000000000ULL, 52, 0, 0xffff89ab46501237ULL},
    {0x0004010040100400ULL, 56, 0x1000800000000000ULL, 52, 0, 0xffff0128ba934567ULL},
    {0x0002000401004010ULL, 54, 0x0100040000000000ULL, 52, 0, 0xffffab4876501239ULL},
    {0x0001004010040100ULL, 54, 0x2002010000000000ULL, 52, 0, 0xffff43210ba56789ULL},
    {0x0000802008020080ULL, 58, 0x0200001000000000ULL, 52, 0, 0xffff0ba987612345ULL},
    {0x0000401004010040ULL, 58, 0x0100000400000000ULL, 51, 0, 0xfff0cba987612345ULL},
    {0x0040100401004000ULL, 59, 0x0100800000000000ULL, 51, 0, 0xfff6789abc501234ULL},  // P18 (index:63)
    {0x0020080200802000ULL, 59, 0x0100800000000000ULL, 52, 0, 0xffff6789ab501234ULL},
    {0x0010040100401000ULL, 59, 0x0100800000000000ULL, 52, 0, 0xffff789ab5601234ULL},
    {0x0008020080200800ULL, 59, 0x0100800000000000ULL, 52, 0, 0xffff89ab65701234ULL},
    {0x0004010040100400ULL, 59, 0x0100800000000000ULL, 52, 0, 0xffff9ab765801234ULL},
    {0x0002008020080100ULL, 56, 0x0004002000000000ULL, 52, 0, 0xffff01ba98324567ULL},
    {0x0001004010020080ULL, 57, 0x0002001000000000ULL, 52, 0, 0xffff0ba987312456ULL},
    {0x0000802004010040ULL, 58, 0x0001000000000000ULL, 52, 0, 0xffffba9876301245ULL},
    {0x0000400802008020ULL, 58, 0x0000800000000000ULL, 51, 0, 0xfffcba9876401235ULL},
    {0x0040100401004000ULL, 59, 0x0100404000000000ULL, 50, 0, 0xff789abcd5601234ULL},  // P19 (index:72)
    {0x0020080200802000ULL, 59, 0x0100404000000000ULL, 51, 0, 0xfff789abc5601234ULL},
    {0x0010040100401000ULL, 59, 0x0100204000000000ULL, 51, 0, 0xfff89abc65701234ULL},
    {0x0008020080200800ULL, 54, 0x0400080020000000ULL, 51, 0, 0xfff0123cb4a56789ULL},
    {0x0004010040100400ULL, 58, 0x0100004000000000ULL, 51, 0, 0xfffabc8760912345ULL},
    {0x0002008020080100ULL, 58, 0x0100004000000000ULL, 51, 0, 0xfffbc98761a02345ULL},
    {0x0001004010020080ULL, 58, 0x0100004000000000ULL, 51, 0, 0xfffca98762b01345ULL},
    {0x0000802004010040ULL, 58, 0x0100004000000000ULL, 51, 0, 0xfffba98763c01245ULL},
    {0x0000401004010040ULL, 59, 0x0001004000000000ULL, 50, 0, 0xffdcba9875601234ULL},
};

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
  inline static constexpr int get_index(Magic const& magic, BitBoard const& bb) {
    // Use special magic formula for these 3 indices.
    if (Index == 0 || Index == 8 || Index == 26) {
      if (Index == 26) {
        return ((rshift(bb.lo * magic.magic_lo, magic.shift_lo)) | (rshift(bb.hi * magic.magic_hi, magic.shift_hi) << 11)) >>
               magic.shift_final;
      }
      return (rshift((bb.lo >> 9) * magic.magic_lo, magic.shift_lo) | rshift((bb.lo << 55) | (bb.hi * magic.magic_hi), magic.shift_hi)) >>
             magic.shift_final;
    }
    return magic.get_index(bb);
  }

  /** Magic traits */
  static constexpr auto magic = rook_magic_table[Index];

  /** bitboard array for all variation */
  static constexpr auto variation_table = Base::make_variation_table(magic);

#ifdef SAVE_ATTACK_TABLE
  static std::vector<BitBoard> get_variation() {
    constexpr auto table = variation_table;
    std::vector<BitBoard> v;
    for (auto x: table) v.push_back(x);
    return std::move(v);
  } 
#endif

};

//
// Derived class
//
template <bool Promoted, int Index>
class RookAttack {
 public:
  typedef RookAttackBase<Index> Base;

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

  /**
   * Return attack bitboard from occupancy bitboard.
   */
  static constexpr BitBoard get_attack(BitBoard const& occ) {
    constexpr auto magic = Base::magic;
    constexpr auto affected_bb = Base::Base::affected_bb;
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
  static constexpr auto generate(util::seq<Is...>) -> util::Array<decltype(&RookAttack<false, 0>::get_attack), sizeof...(Is)> {
    return {{&RookAttack<Promoted, Is>::get_attack...}};
  }

  static constexpr auto generate() { return generate(util::gen_seq<81>{}); }
};

#ifdef SAVE_ATTACK_TABLE
/**
 * Generate the array of variation tables.
 */
template <bool Promoted>
struct RookAttackTableGenerator {
  template <int... Is>
  static constexpr auto generate(util::seq<Is...>) -> util::Array<decltype(&RookAttack<false, 0>::Base::get_variation), sizeof...(Is)> {
    return {{&RookAttack<Promoted, Is>::Base::get_variation...}};
  }

  static constexpr auto generate() { return generate(util::gen_seq<81>{}); }
};
#endif
}
}
}
}

#endif  // MOG_CORE_ATTACK_RANGED_ROOK_HPP_INCLUDED
