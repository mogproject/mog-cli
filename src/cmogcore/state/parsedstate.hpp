#ifndef MOG_CORE_STATE_PARSEDSTATE_HPP_INCLUDED
#define MOG_CORE_STATE_PARSEDSTATE_HPP_INCLUDED

#include <cassert>
#include <algorithm>
#include "../util.hpp"
#include "../bitboard.hpp"
#include "./simplestate.hpp"
#include "../attack.hpp"


namespace mog {
  namespace core {
    namespace state {
      /*
       * State class with calculated attack bitboards
       */
      constexpr int EMPTY_CELL = -1;

      struct ParsedState {
        typedef util::Array<BitBoard, NUM_PIECES * 2> LegalMoveList;

        int turn;
        PieceList pieces;
        util::Array<BitBoard, NUM_PIECES> attack_bbs;

        util::Array<int, 81> boards;  // pos -> piece_id

        BitBoard occ_all;
        BitBoard occ[2];
        BitBoard occ_pawn[2];

        ParsedState(SimpleState const&ss) {
          turn = ss.turn;
          pieces = ss.pieces;
          
          std::fill(boards.begin(), boards.end(), EMPTY_CELL);

          // prepare occupancy bitboards and initialize boards array
          for (auto i = 0; i < NUM_PIECES; ++i) {
            auto p = pieces[i];
            if (p == PIECE_NOT_AVAILABLE) continue;

            auto ps = SimpleState::get_pos(p);
            if (ps == pos::HAND) continue;

            auto o = SimpleState::get_owner(p);
            auto is_pawn = SimpleState::get_ptype(i, p) == ptype::PAWN;

            occ[o] = occ[o].set(ps);
            if (is_pawn) occ_pawn[o] = occ_pawn[o].set(ps);

            boards[ps] = i;
          }
          occ_all = occ[turn::BLACK] | occ[turn::WHITE];

          // prepare attack bitboards
          for (auto i = 0; i < NUM_PIECES; ++i) {
            auto p = pieces[i];
            if (p == PIECE_NOT_AVAILABLE) continue;

            auto ps = SimpleState::get_pos(p);
            if (ps == pos::HAND) continue;

            auto o = SimpleState::get_owner(p);
            auto pt = SimpleState::get_ptype(i, p);

            attack_bbs[i] =
                ptype::is_ranged(pt)
                    ? attack::get_attack(o, pt, ps, occ_all)
                    : attack::get_attack(o, pt, ps);
          }
        }

        /**
         index 0-39: raw moves
         index 40-79: promoted moves
         */
        LegalMoveList get_legal_moves() {
          LegalMoveList ret;

          int hand_used = 0;

          for (auto i = 0; i < NUM_PIECES; ++i) {
            auto p = pieces[i];
            if (p == PIECE_NOT_AVAILABLE) continue;

            auto o = SimpleState::get_owner(p);
            if (o != turn) continue;

            auto pt = SimpleState::get_ptype(i, p);
            auto ps = SimpleState::get_pos(p);

            if (ps == 81) { // hand
              if (hand_used & RAW_PTYPE[i]) {
                if (i >= 22) { // pawn
                  ret[i] = attack::get_attack(o, occ_all, occ_pawn[turn]);
                } else {
                  ret[i] = attack::get_attack(o, pt, occ_all);
                }
                hand_used |= 1 << RAW_PTYPE[i];
              }
            } else {  // board
              auto base = ((ptype::is_ranged(pt)) ? attack::get_attack(o, pt, ps, occ_all) : attack::get_attack(o, pt, ps)) & ~occ[turn];

              if (ptype::is_promoted(pt)) { // already promoted
                ret[i + NUM_PIECES] = base;
              } else if (!ptype::can_promote(pt)) { // cannot promote
                ret[i] = base;
              } else {
                auto promo_zone = get_promotion_zone(o);
                auto restriction = get_restriction(o, pt);
                if (promo_zone.get(ps)) {  // in the promotion zone
                  ret[i] = base & restriction;
                  ret[i + NUM_PIECES] = base;
                } else {
                  ret[i] = base & restriction;
                  ret[i + NUM_PIECES] = base & promo_zone;
                }
              }
            }
          }
          return ret;
        }

        void move_next(int piece_id, int to, bool promote) {
          assert(0 <= piece_id && piece_id < NUM_PIECES);

          // captured piece
          if (boards[to] != EMPTY_CELL) {
            auto captured_id = boards[to];
            auto is_captured_pawn = SimpleState::get_ptype(captured_id, pieces[captured_id]) == ptype::PAWN;
            pieces[captured_id] = turn << 8 | 81;  // 81=HAND
            occ[turn ^ 1] = occ[turn ^ 1].reset(to);
            if (is_captured_pawn) occ_pawn[turn ^ 1] = occ_pawn[turn ^ 1].reset(to);
          }

          // moved piece
          auto p = pieces[piece_id];
          auto from_ptype = SimpleState::get_ptype(piece_id, p);
          auto to_ptype = from_ptype | (promote ? 8 : 0);
          auto from = SimpleState::get_pos(p);
        
          occ[turn] = occ[turn].reset(from);
          occ[turn] = occ[turn].set(to);
          occ_all = occ_all.reset(from);
          occ_all = occ_all.set(to);
          if (from_ptype == ptype::PAWN) occ_pawn[turn] = occ_pawn[turn].reset(from);
          if (to_ptype == ptype::PAWN) occ_pawn[turn] = occ[turn].set(to);
          boards[to] = piece_id;

          attack_bbs[piece_id] =
              ptype::is_ranged(to_ptype)
                  ? attack::get_attack(to_ptype, to_ptype, to, occ_all)
                  : attack::get_attack(to_ptype, to_ptype, to);

          pieces[piece_id] = (p & 0xff80) | (promote ? 128 : 0) | to; 

          // ranged pieces
          BitBoard from_and_to;
          from_and_to = from_and_to.set(from);
          from_and_to = from_and_to.set(to);

          for (auto i = 2; i < 10; ++i) {
            auto p2 = pieces[i];
            if (p2 == PIECE_NOT_AVAILABLE) continue;

            auto o = SimpleState::get_owner(p2);
            auto pt2 = SimpleState::get_ptype(i, p2);
            if (pt2 == ptype::PLANCE) continue;

            auto ps = SimpleState::get_pos(p2);
            attack_bbs[i] = attack::get_attack(o, pt2, ps, occ_all);
          }

          // flip turn
          turn ^= 1;
        }

        /** get piece value */
        constexpr int get_piece(size_t index) const { return index < NUM_PIECES ? pieces[index] : PIECE_NOT_AVAILABLE; }

        /** get attack bitboards */
        constexpr BitBoard get_attack_bb(size_t index) const { return index < NUM_PIECES ? attack_bbs[index] : bitboard::EMPTY; }

       private:
         inline constexpr static BitBoard get_promotion_zone(int const owner) {
           return (bitboard::rank1 | bitboard::rank2 | bitboard::rank3).flip_by_turn(owner);
         }

         inline constexpr static BitBoard get_restriction(int const owner, int const piece_type) {
           if (piece_type == ptype::PAWN || piece_type == ptype::LANCE) {
            return (~bitboard::rank1).flip_by_turn(owner);
          } else if (piece_type == ptype::KNIGHT) {
            return (~(bitboard::rank1 | bitboard::rank2)).flip_by_turn(owner);
          } else {
            return bitboard::FULL;
          }
        }
      };
    }
  }
}

#endif // MOG_CORE_STATE_PARSEDSTATE_HPP_INCLUDED