#ifndef MOG_CORE_ATTACK_RANGED_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_HPP_INCLUDED

#include <iostream>
#include <fstream>
#include "ranged_lance.hpp"
#include "ranged_bishop.hpp"
#include "ranged_rook.hpp"

namespace mog {
namespace core {
namespace attack {
//
// ranged piece types
//
namespace ranged {
//
// utilities
//
typedef BitBoard (*MagicCalculator)(BitBoard const&);

//
// Create array of functions.
//
constexpr BitBoard empty_magic(BitBoard const& notuse) { return bitboard::EMPTY; }

constexpr auto empty = util::array::fill<81>(&empty_magic);
constexpr auto rook = RookAttackGenerator<false>::generate();
constexpr auto prook = RookAttackGenerator<true>::generate();
constexpr auto bishop = BishopAttackGenerator<false>::generate();
constexpr auto pbishop = BishopAttackGenerator<true>::generate();
constexpr auto blance = LanceAttackGenerator<turn::BLACK>::generate();
constexpr auto wlance = LanceAttackGenerator<turn::WHITE>::generate();

constexpr util::Array<util::Array<MagicCalculator, 81>, 32> bb_table_ranged = {{
    rook,  bishop,  blance, empty, empty, empty, empty, empty,  //
    prook, pbishop, empty,  empty, empty, empty, empty, empty,  //
    rook,  bishop,  wlance, empty, empty, empty, empty, empty,  //
    prook, pbishop, empty,  empty, empty, empty, empty, empty,  //
}};

#ifdef SAVE_ATTACK_TABLE
/**
 * Generate C++ code including all the variation tables.
 */
void save_attack_tables(std::string const& path) {
  util::Array<util::Array<decltype(&LanceAttack<false, 0>::get_variation), 81>, 4> tables = {{
    LanceAttackTableGenerator<turn::BLACK>::generate(),
    LanceAttackTableGenerator<turn::WHITE>::generate(),
    BishopAttackTableGenerator<false>::generate(),
    RookAttackTableGenerator<false>::generate()
  }};

  std::ofstream f(path, std::ios::out);
  if (f.is_open()) {
    f << "#ifndef MOG_CORE_ATTACK_DATA_PRESET_DATAL_HPP_INCLUDED" << std::endl;
    f << "#define MOG_CORE_ATTACK_DATA_PRESET_DATAL_HPP_INCLUDED" << std::endl;
    f << "#include \"../../util.hpp\"" << std::endl;
    f << "namespace mog{namespace core{namespace attack{namespace ranged{namespace data{" << std::endl;
    f << "template <int Index, int MagicType> struct PresetData {};" << std::endl;

    for (int mtype = 0; mtype < 4; ++mtype) {
      for (int i = 0; i < 81; ++i) {
        auto xs = tables[mtype][i]();
        auto sz = xs.size();
        f << "template <> struct PresetData<" << i << "," << mtype << "> {" << std::endl;
        f << "static constexpr util::Array<BitBoard," << sz << "> variation_table={{" << std::endl;
        for (size_t j = 0; j < sz; ++j) {
          if (j != 0) f << ",";
          f << "BitBoard(" << xs[j].lo << "ULL," << xs[j].hi << "ULL)";
        }
        f << "}};" << std::endl << "};" << std::endl;
      }
    }

    f << "}}}}}" << std::endl;
    f << "#endif  // MOG_CORE_ATTACK_DATA_PRESET_DATAL_HPP_INCLUDED" << std::endl;
    f.close();
  } else {
    throw RuntimeError("Failed to save the variation table.");
  }

  std::cout << "Saved attack tables: " << path << std::endl;
}
#endif
}

constexpr auto bb_table_ranged = ranged::bb_table_ranged;
}
}
}

#endif  // MOG_CORE_ATTACK_RANGED_HPP_INCLUDED