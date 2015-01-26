#ifndef MOG_CORE_UTIL_TRANSFORM_HPP_INCLUDED
#define MOG_CORE_UTIL_TRANSFORM_HPP_INCLUDED

#include <array>
#include "seq.hpp"

namespace mog {
  namespace core {
    namespace util {

      // for unary function
      template <typename Fn, int... Is>
      constexpr auto transform(Fn fn, seq<Is...>) -> std::array<decltype(fn(0)), sizeof...(Is)> {
        return {{ fn(Is)... }};
      }

      template <int N, typename Fn>
      constexpr auto transform(Fn fn) -> decltype(transform(fn, gen_seq<N>{})) {
        return transform(fn, gen_seq<N>{});
      }

    }
  }
}
#endif  // MOG_CORE_UTIL_TRANSFORM_HPP_INCLUDED