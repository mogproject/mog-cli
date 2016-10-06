#ifndef MOG_CORE_STATE_SIMPLESTATE_HPP_INCLUDED
#define MOG_CORE_STATE_SIMPLESTATE_HPP_INCLUDED

#include "../util.hpp"


namespace mog {
  namespace core {
    namespace state {
      constexpr size_t NUM_PIECES = 40;
      constexpr int PIECE_NOT_AVAILABLE = -1;

      typedef util::Array<int, NUM_PIECES> PieceList;
      constexpr PieceList RAW_PTYPE = {{
          ptype::KING, ptype::KING,
          ptype::ROOK, ptype::ROOK,
          ptype::BISHOP, ptype::BISHOP,
          ptype::LANCE, ptype::LANCE, ptype::LANCE, ptype::LANCE,
          ptype::GOLD, ptype::GOLD, ptype::GOLD, ptype::GOLD,
          ptype::SILVER, ptype::SILVER, ptype::SILVER, ptype::SILVER,
          ptype::KNIGHT, ptype::KNIGHT, ptype::KNIGHT, ptype::KNIGHT,
          ptype::PAWN, ptype::PAWN, ptype::PAWN, ptype::PAWN, ptype::PAWN, ptype::PAWN, ptype::PAWN, ptype::PAWN,
          ptype::PAWN, ptype::PAWN, ptype::PAWN, ptype::PAWN, ptype::PAWN, ptype::PAWN, ptype::PAWN, ptype::PAWN,
          ptype::PAWN, ptype::PAWN,
      }};

      /*
       * State class before parsing
       *
       * @param turn 0 -> black, 1 -> white
       * @param pieces array of integers (slot is fixed by raw piece type)
       *
       *   Usage of integer
       *
       *   -------- -------- -------- --------
       *                               ******* position (0-80 -> board, 81 -> hand)
       *                              *        is promoted (0 -> raw, 1 -> promoted)
       *                            *          owner (0 -> black, 1 -> white)
       *
       *   Slot usage
       *   0-1: king, 2-3: rook, 4-5: bishop, 6-9: lance, 10-13: gold, 14-17: silver, 18-21: knight, 22-39: pawn
       *
       *   Note: If the piece is unused, should be set -1
       */
      struct SimpleState {
        int turn;
        PieceList pieces;

        constexpr SimpleState(int turn, PieceList const& pieces): turn(turn), pieces(pieces) {}

        // constructor for Python
        SimpleState(int turn, boost::python::list const& pieces): turn(turn) {
          auto n = boost::python::len(pieces);
          assert(n <= NUM_PIECES);  // Length of the pieces should be less than or equal 40.

          for (auto i = 0; i < NUM_PIECES; ++i) {
            this->pieces[i] = i < n ? boost::python::extract<int>(pieces[i]) : PIECE_NOT_AVAILABLE;
          }
        }

        /** get piece value */
        constexpr int get_piece(size_t index) const { return index < NUM_PIECES ? pieces[index] : PIECE_NOT_AVAILABLE; }

        /** extract owner from int value */
        inline static constexpr int get_owner(int value) { return (value >> 8) & 1; }

        /** extract piece type fron int value */
        inline static constexpr int get_ptype(int index, int value) { return RAW_PTYPE[index] | ((value >> 4) & 8); }

        /** extract position from int value */
        inline static constexpr int get_pos(int value) { return value & 127; }

        /**
         * Sort and compare in each raw piece types
         */
        bool operator==(SimpleState const& rhs) const {
          if (turn != rhs.turn) return false;

          // sort for each piece types
          static int thres[] = {0, 2, 4, 6, 10, 14, 18, 22, 40};
          PieceList a(pieces), b = (rhs.pieces);

          // todo: can be more efficient?
          for (auto ptype = 0; ptype < 8; ++ptype) {
            std::sort(a.begin() + thres[ptype], a.begin() + thres[ptype + 1]);
            std::sort(b.begin() + thres[ptype], b.begin() + thres[ptype + 1]);
          }
          return a == b;
        }

      };
    }
  }
}

#endif  // MOG_CORE_STATE_SIMPLESTATE_HPP_INCLUDED
