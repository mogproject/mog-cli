#ifndef MOG_CORE_UTIL_PREPROCESSOR_HPP_INCLUDED
#define MOG_CORE_UTIL_PREPROCESSOR_HPP_INCLUDED

#include <boost/preprocessor.hpp>

namespace mog {
  namespace core {
    namespace util {

//#define POW2_ARRAY (16, (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536))
//#define POW2(n) BOOST_PP_ARRAY_ELEM(n, POW2_ARRAY)

    }
  }
}

#endif  // MOG_CORE_UTIL_PREPROCESSOR_HPP_INCLUDED