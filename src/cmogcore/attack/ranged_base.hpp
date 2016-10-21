#ifndef MOG_CORE_ATTACK_RANGED_BASE_HPP_INCLUDED
#define MOG_CORE_ATTACK_RANGED_BASE_HPP_INCLUDED

#include <iostream>
#include <fstream>
#include "../util.hpp"
#include "../bitboard.hpp"
#include "./ranged_magic.hpp"

#ifdef LOAD_ATTACK_TABLE
#include "./data/preset_data.hpp"
#endif

namespace mog {
namespace core {
namespace attack {
namespace ranged {
/**
 * Base class for ranged piece types
 *
 * @tparam MagicType 0: black lance, 1: white lance, 2: bishop or promoted bishop, 3: rook or promoted rook
 */
template <int Index, int MagicType>
class RangedBase {
 public:
  /** File and rank (1-indexed) */
  static constexpr auto file = pos::get_file(Index);
  static constexpr auto rank = pos::get_rank(Index);

  /** Affected mask bitboard */
  static constexpr auto affected_mask =
      ~(((rank != 1) ? bitboard::rank1 : bitboard::EMPTY) | ((rank != 9) ? bitboard::rank9 : bitboard::EMPTY) |
        ((file != 1) ? bitboard::file1 : bitboard::EMPTY) | ((file != 9) ? bitboard::file9 : bitboard::EMPTY));

 private:
  /** Generate directions. */
  static constexpr util::Array<std::pair<int, int>, 4> get_directions() {
    switch (MagicType) {
      case 0:
        return {{{0, -1}}};
        break;
      case 1:
        return {{{0, 1}}};
        break;
      case 2:
        return {{{-1, -1}, {-1, 1}, {1, 1}, {1, -1}}};
        break;
      case 3:
        return {{{0, -1}, {-1, 0}, {0, 1}, {1, 0}}};
        break;
    }
  }

  /** max attack bitboard */
  static constexpr BitBoard get_max_attack() {
    auto bb = BitBoard();
    for (auto d : directions) {
      bb = bb.set_repeat(file, rank, d.first, d.second, 8);
    }
    return bb;
  }

 public:
  /** directions */
  static constexpr auto directions = get_directions();

  /** Make affected bitboard */
  static constexpr auto affected_bb = get_max_attack() & affected_mask;

 private:
  static constexpr auto get_affected_sizes() {
    util::Array<int, directions.size()> ret = {{}};

    for (size_t i = 0; i < directions.size(); ++i) {
      auto df = directions[i].first, dr = directions[i].second;
      auto a = df == 0 ? 7 : util::max((2 - file) / df, (8 - file) / df);
      auto b = dr == 0 ? 7 : util::max((2 - rank) / dr, (8 - rank) / dr);
      ret[i] = util::max(0, util::min(a, b));
    }

    return ret;
  }

 public:
  /** size of the variation table */
  static constexpr int variation_size = 1 << affected_bb.count();

  /** array of length of the affected bits for each direction */
  static constexpr auto affected_sizes = get_affected_sizes();

  /**
   * Make variation table
   */
  static constexpr auto make_variation_table(Magic const& magic) {
#ifdef LOAD_ATTACK_TABLE
    // load preset data
    return mog::core::attack::ranged::data::PresetData<Index, MagicType>::variation_table;
#else
    util::Array<BitBoard, variation_size> table = {{}};

    // max length
    auto mi = affected_sizes[0];
    auto mj = affected_sizes[1];
    auto mk = affected_sizes[2];
    auto ml = affected_sizes[3];

    // shift width
    auto si = 0;
    auto sj = mi;
    auto sk = sj + mj;
    auto sl = sk + mk;

    auto bb = BitBoard();
    for (int di = 1; di <= mi + 1; ++di) {
      bb = bb.set(file + directions[0].first * di, rank + directions[0].second * di);
      auto bb1(bb);
      for (int dj = 1; dj <= mj + 1; ++dj) {
        bb1 = bb1.set(file + directions[1].first * dj, rank + directions[1].second * dj);
        auto bb2(bb1);
        for (int dk = 1; dk <= mk + 1; ++dk) {
          bb2 = bb2.set(file + directions[2].first * dk, rank + directions[2].second * dk);
          auto bb3(bb2);
          for (int dl = 1; dl <= ml + 1; ++dl) {
            bb3 = bb3.set(file + directions[3].first * dl, rank + directions[3].second * dl);
            for (int xi = 1 << mi >> di; xi < (1 << (mi + 1 - di)); ++xi) {
              for (int xj = 1 << mj >> dj; xj < (1 << (mj + 1 - dj)); ++xj) {
                for (int xk = 1 << mk >> dk; xk < (1 << (mk + 1 - dk)); ++xk) {
                  for (int xl = 1 << ml >> dl; xl < (1 << (ml + 1 - dl)); ++xl) {
                    int ordered = (xi << si) | (xj << sj) | (xk << sk) | (xl << sl);
                    table[magic.convert_mapping(ordered)] = bb3;
                  }
                }
              }
            }
          }
        }
      }
    }
    return std::move(table);

#endif  // FLAG_USE_PRESET_DATA
  }
};
}
}
}
}

#endif  // MOG_CORE_ATTACK_RANGED_BISHOP_HPP_INCLUDED