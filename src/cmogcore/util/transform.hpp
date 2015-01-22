#ifndef MOG_CORE_UTIL_TRANSFORM_HPP_INCLUDED
#define MOG_CORE_UTIL_TRANSFORM_HPP_INCLUDED

#include <array>
#include "seq.hpp"

namespace mog {
  namespace core {
    namespace util {
      template <typename F, int... Is>
      constexpr auto transform(F f, seq<Is...>) -> std::array<decltype(f(0)), sizeof...(Is)> {
        return {{ f(Is)... }};
      }

      template <int N, typename F>
      constexpr auto transform(F f) -> decltype(transform(f, gen_seq<N>{})) {
        return transform(f, gen_seq<N>{});
      }
    }
  }
}
#endif  // MOG_CORE_UTIL_TRANSFORM_HPP_INCLUDED