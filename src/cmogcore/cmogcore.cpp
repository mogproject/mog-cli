#include <boost/python.hpp>
#include "bitboard.hpp"

BOOST_PYTHON_MODULE(cmogcore){
  using namespace boost::python;
  using namespace mog::core;

  class_<bitboard::BitBoard>("BitBoard")
    .def(init<u64, u64>())
    .def(self == self)
    .def("get", &bitboard::get)
    .def("set", &bitboard::set)
    ;

}

