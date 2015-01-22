#ifndef MOG_CORE_ATTACK_DIRECT_HPP_INCLUDED
#define MOG_CORE_ATTACK_DIRECT_HPP_INCLUDED

#include <array>
#include "../util.hpp"
#include "../bitboard.hpp"

namespace mog {
  namespace core {
    namespace attack {
      //
      // direct piece types
      //
      constexpr BitBoard attack_bb_king(int const file, int const rank) {
        return BitBoard()
          .set(file - 1, rank - 1).set(file, rank - 1).set(file + 1, rank - 1)
          .set(file - 1, rank).set(file + 1, rank)
          .set(file - 1, rank + 1).set(file, rank + 1).set(file + 1, rank + 1);
      }

      // TODO: refactor to keep DRY
      constexpr BitBoard attack_bb_gold_black(int const file, int const rank) {
        return BitBoard()
          .set(file - 1, rank - 1).set(file, rank - 1).set(file + 1, rank - 1)
          .set(file - 1, rank).set(file + 1, rank)
          .set(file, rank + 1);
      }

      constexpr BitBoard attack_bb_gold_white(int const file, int const rank) {
        return BitBoard()
          .set(file, rank - 1)
          .set(file - 1, rank).set(file + 1, rank)
          .set(file - 1, rank + 1).set(file, rank + 1).set(file + 1, rank + 1);
      }

      constexpr BitBoard attack_bb_silver_black(int const file, int const rank) {
        return BitBoard()
          .set(file - 1, rank - 1).set(file, rank - 1).set(file + 1, rank - 1)
          .set(file - 1, rank + 1).set(file + 1, rank + 1);
      }

      constexpr BitBoard attack_bb_silver_white(int const file, int const rank) {
        return BitBoard()
          .set(file - 1, rank - 1).set(file + 1, rank - 1)
          .set(file - 1, rank + 1).set(file, rank + 1).set(file + 1, rank + 1);
      }

      constexpr BitBoard attack_bb_knight_black(int const file, int const rank) {
        return BitBoard().set(file - 1, rank - 2).set(file + 1, rank - 2);
      }

      constexpr BitBoard attack_bb_knight_white(int const file, int const rank) {
        return BitBoard().set(file - 1, rank + 2).set(file + 1, rank + 2);
      }

      constexpr BitBoard attack_bb_pawn_black(int const file, int const rank) {
        return BitBoard().set(file, rank - 1);
      }

      constexpr BitBoard attack_bb_pawn_white(int const file, int const rank) {
        return BitBoard().set(file, rank + 1);
      }

      constexpr BitBoard attack_bb_king(int const index) {
        return attack_bb_king(index % 9 + 1, index / 9 + 1);
      }

      constexpr BitBoard attack_bb_gold_black(int const index) {
        return attack_bb_gold_black(index % 9 + 1, index / 9 + 1);
      }

      constexpr BitBoard attack_bb_gold_white(int const index) {
        return attack_bb_gold_white(index % 9 + 1, index / 9 + 1);
      }

      constexpr BitBoard attack_bb_silver_black(int const index) {
        return attack_bb_silver_black(index % 9 + 1, index / 9 + 1);
      }

      constexpr BitBoard attack_bb_silver_white(int const index) {
        return attack_bb_silver_white(index % 9 + 1, index / 9 + 1);
      }
      constexpr BitBoard attack_bb_knight_black(int const index) {
        return attack_bb_knight_black(index % 9 + 1, index / 9 + 1);
      }

      constexpr BitBoard attack_bb_knight_white(int const index) {
        return attack_bb_knight_white(index % 9 + 1, index / 9 + 1);
      }

      constexpr BitBoard attack_bb_pawn_black(int const index) {
        return attack_bb_pawn_black(index % 9 + 1, index / 9 + 1);
      }

      constexpr BitBoard attack_bb_pawn_white(int const index) {
        return attack_bb_pawn_white(index % 9 + 1, index / 9 + 1);
      }

      // TODO: refactor to keep DRY
      constexpr auto bb_table_direct = std::array<std::array<BitBoard, 81>, 32> {{
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),  // king
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),  // rook
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),  // bishop
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),  // lance
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_gold_black  )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_silver_black)),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_knight_black)),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_pawn_black  )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_gold_black  )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_gold_black  )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_gold_black  )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_gold_black  )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_gold_white  )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_silver_white)),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_knight_white)),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_pawn_white  )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_gold_white  )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_king        )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_gold_white  )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_gold_white  )),
        util::transform<81>(static_cast<BitBoard (*)(int)>(attack::attack_bb_gold_white  )),
      }};

    }
  }
}

#endif  // MOG_CORE_ATTACK_DIRECT_HPP_INCLUDED