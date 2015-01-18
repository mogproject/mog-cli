#include <boost/python.hpp>
#include "bitboard.hpp"

BOOST_PYTHON_MODULE(cmogcore){
  using namespace boost::python;
  using namespace mog::core;

  class_<BitBoard>("BitBoard")
    .def(init<u64, u64>())
    .def(init<BitBoard>())
    .def(self == self)
    .def("get", &BitBoard::get)
    .def("set", &BitBoard::set)
    ;

}

