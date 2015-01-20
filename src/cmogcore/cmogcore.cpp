#include <boost/python.hpp>
#include "bitboard.hpp"
#include "attack.hpp"

BOOST_PYTHON_MODULE(cmogcore){
  using namespace boost::python;
  using namespace mog::core;

  class_<BitBoard>("BitBoard")
    .def(init<u64, u64>())
    .def(init<int, int, int, int, int, int, int, int, int>())
    .def_readonly("lo", &BitBoard::lo)
    .def_readonly("hi", &BitBoard::hi)
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
    .def("shift_down", &BitBoard::shift_down)
    .def("shift_up", &BitBoard::shift_up)
    ;

  class_<Attack>("Attack")
    .def_readonly("xxx", &attack::xxx)
    ;
}

