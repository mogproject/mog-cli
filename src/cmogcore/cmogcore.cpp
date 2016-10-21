#include <boost/python.hpp>
#include "bitboard.hpp"
#include "attack.hpp"
#include "state/move.hpp"
#include "state/state.hpp"
#include "state/extended_state.hpp"

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
    for (auto x : xs) ret.append(x);
    return py::incref(ret.ptr());
  }

  static PyTypeObject const* get_pytype() { return &PyList_Type; }
};
}  // namespace cmogcore::detail

template <typename Seq>
void expose_seq_to_list() {
  py::to_python_converter<Seq, detail::seq_to_list<Seq>, true>();
}

/*
 * Converter for list parameter (pylist => mog::core::util::Array)
 */
template <typename T, int N>
void expose_pylist_to_array() {
  typedef mog::core::util::Array<T, N> A;

  auto convertible = [](PyObject* obj_ptr) -> void* {
    return PySequence_Check(obj_ptr) && (PySequence_Size(obj_ptr) == N) ? obj_ptr : NULL;
  };

  auto construct = [](PyObject* obj_ptr, py::converter::rvalue_from_python_stage1_data* data) {
    A* storage = new (reinterpret_cast<py::converter::rvalue_from_python_storage<A>*>(data)->storage.bytes) A();
    for (py::ssize_t i = 0; i < N; ++i) {
      storage->operator[](i) = py::extract<typename boost::range_value<A>::type>(PySequence_GetItem(obj_ptr, i));
    }
    data->convertible = storage;
  };

  py::converter::registry::push_back(convertible, construct, py::type_id<A>());
}

// exceptions
void translateRuntimeError(mog::core::RuntimeError const& e) { PyErr_SetString(PyExc_RuntimeError, e.what()); }
}  // namespace cmogcore

// constants
constexpr mog::core::util::Array<mog::core::u64, 8> mog::core::state::State::piece_masks;
constexpr mog::core::util::Array<mog::core::u64, mog::core::state::State::NUM_PIECES> mog::core::state::State::__raw_piece_types;
constexpr mog::core::util::Array<mog::core::u64, mog::core::state::ExtendedState::HASH_SEED_BOARD_SIZE>
    mog::core::state::ExtendedState::__hash_seed_board;
constexpr mog::core::util::Array<mog::core::u64, mog::core::state::ExtendedState::HASH_SEED_HAND_SIZE>
    mog::core::state::ExtendedState::__hash_seed_hand;
constexpr mog::core::util::Array<int, 8> mog::core::state::State::__piece_offsets;

BOOST_PYTHON_MODULE(cmogcore) {
  using namespace boost::python;
  using namespace mog::core;
  using namespace cmogcore;

  // exception handling
  py::register_exception_translator<RuntimeError>(&translateRuntimeError);

  // expose converters
  expose_seq_to_list<std::vector<int>>();
  expose_seq_to_list<state::State::PositionList>();
  expose_seq_to_list<state::ExtendedState::LegalMoveList>();
  expose_seq_to_list<state::ExtendedState::AttackBBList>();
  expose_seq_to_list<state::ExtendedState::BoardTable>();
  expose_seq_to_list<state::ExtendedState::OccBBList>();
  expose_pylist_to_array<u64, 5>();
  expose_pylist_to_array<BitBoard, 40>();  // state::ExtendedState::AttackBBList
  expose_pylist_to_array<int, 81>();       // state::ExtendedState::BoardTable
  expose_pylist_to_array<BitBoard, 2>();   // state::ExtendedState::OccBBList

// expose functions
#ifdef SAVE_ATTACK_TABLE
  def("save_attack_tables", &attack::ranged::save_attack_tables);
#endif

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
      .def("flip_by_turn", &BitBoard::flip_by_turn)
      .def("spread_all_file", &BitBoard::spread_all_file)
      .def("ident", &bitboard::ident)
      .staticmethod("ident");

  class_<state::Move>("Move", init<int, int, int, int>())
      .def_readonly("_turn", &state::Move::turn)
      .def_readonly("_from", &state::Move::from)
      .def_readonly("_to", &state::Move::to)
      .def_readonly("_piece_type", &state::Move::piece_type);

  class_<state::State>("State", init<int, u64, u64, u64, u64, BitBoard, state::State::PositionList>())
      .def_readonly("_turn", &state::State::turn)
      .def_readonly("owner_bits", &state::State::owner_bits)
      .def_readonly("hand_bits", &state::State::hand_bits)
      .def_readonly("promoted_bits", &state::State::promoted_bits)
      .def_readonly("unused_bits", &state::State::unused_bits)
      .def_readonly("_board", &state::State::board)
      .add_property("position", py::make_getter(&state::State::position, py::return_value_policy<py::return_by_value>()))
      .def("validate", &state::State::validate)
      .def("is_used", &state::State::is_used)
      .def("get_owner", &state::State::get_owner)
      .def("get_raw_piece_type", &state::State::get_raw_piece_type)
      .def("get_piece_type", &state::State::get_piece_type)
      .def("get_position", &state::State::get_position)
      .def("get_num_hand", &state::State::get_num_hand)
      .def("set_turn", &state::State::set_turn)
      .def("set_piece", &state::State::set_piece)
      .def("set_all_hand", &state::State::set_all_hand)
      .def("move", &state::State::move)
      .def(self == self);

  class_<state::ExtendedState>("ExtendedState", init<state::State>())
      .def(init<state::State>())
      .def(init<state::State, state::ExtendedState::AttackBBList, state::ExtendedState::BoardTable, state::ExtendedState::OccBBList,
                state::ExtendedState::OccBBList, u64>())
      .def_readonly("state", &state::ExtendedState::state)
      .add_property("attack_bbs", py::make_getter(&state::ExtendedState::attack_bbs, py::return_value_policy<py::return_by_value>()))
      .add_property("board_table", py::make_getter(&state::ExtendedState::board_table, py::return_value_policy<py::return_by_value>()))
      .add_property("occ", py::make_getter(&state::ExtendedState::occ, py::return_value_policy<py::return_by_value>()))
      .add_property("occ_pawn", py::make_getter(&state::ExtendedState::occ_pawn, py::return_value_policy<py::return_by_value>()))
      .def_readonly("hash_value", &state::ExtendedState::hash_value)
      .def("get_attack_bb", &state::ExtendedState::get_attack_bb)
      .def("get_legal_moves", &state::ExtendedState::get_legal_moves)
      .def("move", &state::ExtendedState::move)
      .def(self == self);

  class_<Attack>("Attack")
      .def("get_attack", static_cast<BitBoard (*)(int, int, int)>(&attack::get_attack))
      .def("get_attack", static_cast<BitBoard (*)(int, int, int, BitBoard const&)>(&attack::get_attack))
      .def("get_attack", static_cast<BitBoard (*)(int, BitBoard const&, BitBoard const&)>(&attack::get_attack))
      .def("get_attack", static_cast<BitBoard (*)(int, int, BitBoard const&)>(&attack::get_attack));
}
