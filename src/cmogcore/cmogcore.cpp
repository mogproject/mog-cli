#include <boost/python.hpp>
#include "game.hpp"

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
constexpr mog::core::util::Array<mog::core::u64, 8> mog::core::state::SimpleState::piece_masks;
constexpr mog::core::util::Array<mog::core::u64, mog::core::state::SimpleState::NUM_PIECES>
    mog::core::state::SimpleState::__raw_piece_types;
constexpr mog::core::util::Array<mog::core::u64, mog::core::state::State::HASH_SEED_BOARD_SIZE>
    mog::core::state::State::__hash_seed_board;
constexpr mog::core::util::Array<mog::core::u64, mog::core::state::State::HASH_SEED_HAND_SIZE>
    mog::core::state::State::__hash_seed_hand;
constexpr mog::core::util::Array<int, 8> mog::core::state::SimpleState::__piece_offsets;

BOOST_PYTHON_MODULE(cmogcore) {
  using namespace boost::python;
  using namespace mog::core;
  using namespace cmogcore;

  // exception handling
  py::register_exception_translator<RuntimeError>(&translateRuntimeError);

  // expose converters
  expose_seq_to_list<std::vector<int>>();
  expose_seq_to_list<state::SimpleState::PositionList>();
  expose_seq_to_list<state::State::LegalMoveList>();
  expose_seq_to_list<state::State::AttackBBList>();
  expose_seq_to_list<state::State::BoardTable>();
  expose_seq_to_list<state::State::OccBBList>();
  expose_seq_to_list<Game::StateList>();
  expose_seq_to_list<Game::MoveList>();
  expose_pylist_to_array<u64, 5>();
  expose_pylist_to_array<BitBoard, 40>();  // state::State::AttackBBList
  expose_pylist_to_array<int, 81>();       // state::State::BoardTable
  expose_pylist_to_array<BitBoard, 2>();   // state::State::OccBBList

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

  class_<state::SimpleMove>("SimpleMove", init<int, int, int, int>())
      .def_readonly("_turn", &state::SimpleMove::turn)
      .def_readonly("_from", &state::SimpleMove::from)
      .def_readonly("_to", &state::SimpleMove::to)
      .def_readonly("_piece_type", &state::SimpleMove::piece_type);

  class_<state::Move>("Move", init<int, int, int, int, int, int, int>())
      .def_readonly("_turn", &state::Move::turn)
      .def_readonly("_from", &state::Move::from)
      .def_readonly("_to", &state::Move::to)
      .def_readonly("_piece_type", &state::Move::piece_type)
      .def_readonly("elapsed_time", &state::Move::elapsed_time)
      .def_readonly("move_type", &state::Move::move_type)
      .def_readonly("judge", &state::Move::judge)
      .def(self == self);

  class_<state::Resign>("Resign", init<int>())
      .def_readonly("elapsed_time", &state::Resign::elapsed_time)
      .def(self == self);

  class_<state::TimeUp>("TimeUp", init<int>())
      .def_readonly("elapsed_time", &state::TimeUp::elapsed_time)
      .def(self == self);

  class_<state::IllegalMove>("IllegalMove", init<int>())
      .def_readonly("elapsed_time", &state::IllegalMove::elapsed_time)
      .def(self == self);

  class_<state::PerpetualCheck>("PerpetualCheck", init<>())
      .def_readonly("elapsed_time", &state::PerpetualCheck::elapsed_time)
      .def(self == self);

  class_<state::DeclareWin>("DeclareWin", init<int>())
      .def_readonly("elapsed_time", &state::DeclareWin::elapsed_time)
      .def(self == self);

  class_<state::ThreefoldRepetition>("ThreefoldRepetition", init<>())
      .def_readonly("elapsed_time", &state::ThreefoldRepetition::elapsed_time)
      .def(self == self);

  class_<state::SimpleState>("SimpleState", init<int, u64, u64, u64, u64, BitBoard, state::SimpleState::PositionList>())
      .def_readonly("_turn", &state::SimpleState::turn)
      .def_readonly("owner_bits", &state::SimpleState::owner_bits)
      .def_readonly("hand_bits", &state::SimpleState::hand_bits)
      .def_readonly("promoted_bits", &state::SimpleState::promoted_bits)
      .def_readonly("unused_bits", &state::SimpleState::unused_bits)
      .def_readonly("_board", &state::SimpleState::board)
      .add_property("position", py::make_getter(&state::SimpleState::position, py::return_value_policy<py::return_by_value>()))
      .def("validate", &state::SimpleState::validate)
      .def("is_used", &state::SimpleState::is_used)
      .def("get_owner", &state::SimpleState::get_owner)
      .def("get_raw_piece_type", &state::SimpleState::get_raw_piece_type)
      .def("get_piece_type", &state::SimpleState::get_piece_type)
      .def("get_position", &state::SimpleState::get_position)
      .def("get_num_hand", &state::SimpleState::get_num_hand)
      .def("set_turn", &state::SimpleState::set_turn)
      .def("set_piece", &state::SimpleState::set_piece)
      .def("set_all_hand", &state::SimpleState::set_all_hand)
      .def("move", &state::SimpleState::move)
      .def(self == self);

  class_<Attack>("Attack")
      .def("get_attack", static_cast<BitBoard (*)(int, int, int)>(&attack::get_attack))
      .def("get_attack", static_cast<BitBoard (*)(int, int, int, BitBoard const&)>(&attack::get_attack))
      .def("get_attack", static_cast<BitBoard (*)(int, BitBoard const&, BitBoard const&)>(&attack::get_attack))
      .def("get_attack", static_cast<BitBoard (*)(int, int, BitBoard const&)>(&attack::get_attack));

  class_<state::State>("State", init<state::SimpleState>())
      .def(init<state::SimpleState>())
      .def(init<state::SimpleState, state::State::AttackBBList, state::State::BoardTable, state::State::OccBBList,
                state::State::OccBBList, u64>())
      .def_readonly("state", &state::State::state)
      .add_property("attack_bbs", py::make_getter(&state::State::attack_bbs, py::return_value_policy<py::return_by_value>()))
      .add_property("board_table", py::make_getter(&state::State::board_table, py::return_value_policy<py::return_by_value>()))
      .add_property("occ", py::make_getter(&state::State::occ, py::return_value_policy<py::return_by_value>()))
      .add_property("occ_pawn", py::make_getter(&state::State::occ_pawn, py::return_value_policy<py::return_by_value>()))
      .def_readonly("hash_value", &state::State::hash_value)
      .def("is_checked", &state::State::is_checked)
      .def("is_king_alive", &state::State::is_king_alive)
      .def("get_attack_bb", &state::State::get_attack_bb)
      .def("get_legal_moves", &state::State::get_legal_moves)
      .def("move", &state::State::move)
      .def(self == self);

  class_<Game>("Game", init<state::SimpleState>())
      .def("move", &Game::move)
      .def("move", &Game::move_<state::Resign>)
      .def("move", &Game::move_<state::TimeUp>)
      .def("move", &Game::move_<state::IllegalMove>)
      .def("move", &Game::move_<state::PerpetualCheck>)
      .def("move", &Game::move_<state::DeclareWin>)
      .def("move", &Game::move_<state::ThreefoldRepetition>)
      .add_property("states", py::make_getter(&Game::states, py::return_value_policy<py::return_by_value>()))
      .add_property("moves", py::make_getter(&Game::moves, py::return_value_policy<py::return_by_value>()))
      .def("is_finished", &Game::is_finished);
}
