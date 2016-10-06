#include <boost/python.hpp>
#include "bitboard.hpp"
#include "attack.hpp"
#include "state/simplestate.hpp"
#include "state/parsedstate.hpp"

namespace cmogcore {
  namespace py = boost::python;

  /*
   * Converter of {std::array, std::vector} => python list
   */
  namespace detail {
    template <typename Seq>
    struct seq_to_list {
      static PyObject* convert(Seq const& xs) {
        py::list ret;
        for (auto x: xs) ret.append(x);
        return py::incref(ret.ptr());
      }

      static PyTypeObject const* get_pytype() { return &PyList_Type; }
    };
  }

  template <typename Seq>
  void expose_seq_to_list() {
    py::to_python_converter<Seq, detail::seq_to_list<Seq>, true>();
  }
}


BOOST_PYTHON_MODULE(cmogcore){
  using namespace boost::python;
  using namespace mog::core;
  using namespace cmogcore;

  // expose converters
  expose_seq_to_list<state::ParsedState::LegalMoveList>();
  expose_seq_to_list<std::vector<int>>();

  // expose classes
  class_<BitBoard>("BitBoard")
    .def(init<u64, u64>())
    .def(init<int, int, int, int, int, int, int, int, int>())
    .def_readonly("lo", &BitBoard::lo)
    .def_readonly("hi", &BitBoard::hi)
    .def_readonly("EMPTY", &bitboard::EMPTY)
    .def_readonly("FULL", &bitboard::FULL)
    .def_readonly("rank1", &bitboard::rank1)
    .def_readonly("rank2", &bitboard::rank2)
    .def_readonly("rank3", &bitboard::rank3)
    .def_readonly("rank4", &bitboard::rank4)
    .def_readonly("rank5", &bitboard::rank5)
    .def_readonly("rank6", &bitboard::rank6)
    .def_readonly("rank7", &bitboard::rank7)
    .def_readonly("rank8", &bitboard::rank8)
    .def_readonly("rank9", &bitboard::rank9)
    .def_readonly("file1", &bitboard::file1)
    .def_readonly("file2", &bitboard::file2)
    .def_readonly("file3", &bitboard::file3)
    .def_readonly("file4", &bitboard::file4)
    .def_readonly("file5", &bitboard::file5)
    .def_readonly("file6", &bitboard::file6)
    .def_readonly("file7", &bitboard::file7)
    .def_readonly("file8", &bitboard::file8)
    .def_readonly("file9", &bitboard::file9)
    .def(self == self)
    .def(self & self)
    .def(self | self)
    .def(self ^ self)
    .def(~self)
    .def("__repr__", &bitboard::repr)
    .def("get", static_cast<bool (BitBoard::*)(int const) const>(&BitBoard::get))
    .def("get", static_cast<bool (BitBoard::*)(int const, int const) const>(&BitBoard::get))
    .def("set", static_cast<BitBoard (BitBoard::*)(int const) const>(&BitBoard::set))
    .def("set", static_cast<BitBoard (BitBoard::*)(int const, int const) const>(&BitBoard::set))
    .def("reset", static_cast<BitBoard (BitBoard::*)(int const) const>(&BitBoard::reset))
    .def("reset", static_cast<BitBoard (BitBoard::*)(int const, int const) const>(&BitBoard::reset))
    .def("set_repeat", &BitBoard::set_repeat)
    .def("count", &BitBoard::count)
    .def("to_list", &BitBoard::to_list)
    .def("files", &BitBoard::files)
    .staticmethod("files")
    .def("ranks", &BitBoard::ranks)
    .staticmethod("ranks")
    .def("shift_left", &BitBoard::shift_left)
    .def("shift_right", &BitBoard::shift_right)
    .def("shift_down", &BitBoard::shift_down)
    .def("shift_up", &BitBoard::shift_up)
    .def("flip_vertical", &BitBoard::flip_vertical)
    .def("flip_horizontal", &BitBoard::flip_horizontal)
    .def("spread_all_file", &BitBoard::spread_all_file)
    .def("ident", &bitboard::ident)
    .staticmethod("ident")
    ;

  class_<state::SimpleState>("SimpleState", init<int, list>())
    .def_readonly("turn", &state::SimpleState::turn)
    .def("get_piece", &state::SimpleState::get_piece)
    .def(self == self)
    ;

  class_<state::ParsedState>("ParsedState", init<state::SimpleState>())
    .def_readonly("turn", &state::ParsedState::turn)
    .def("get_piece", &state::ParsedState::get_piece)
    .def("get_attack_bb", &state::ParsedState::get_attack_bb)
    .def("get_legal_moves", &state::ParsedState::get_legal_moves)
    .def("move_next", &state::ParsedState::move_next)
    ;

  class_<Attack>("Attack")
    .def("get_attack", static_cast<BitBoard (*)(int, int, int)>(&attack::get_attack))
    .def("get_attack", static_cast<BitBoard (*)(int, int, int, BitBoard const&)>(&attack::get_attack))
    .def("get_attack", static_cast<BitBoard (*)(int, BitBoard const&, BitBoard const&)>(&attack::get_attack))
    .def("get_attack", static_cast<BitBoard (*)(int, int, BitBoard const&)>(&attack::get_attack))
    ;
}
