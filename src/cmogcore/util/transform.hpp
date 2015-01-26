#ifndef MOG_CORE_UTIL_TRANSFORM_HPP_INCLUDED
#define MOG_CORE_UTIL_TRANSFORM_HPP_INCLUDED

#include <array>
#include "seq.hpp"

namespace mog {
  namespace core {
    namespace util {

      // for unary function
      template <typename F, int... Is>
      constexpr auto transform(F f, seq<Is...>) -> std::array<decltype(f(0)), sizeof...(Is)> {
        return {{ f(Is)... }};
      }

      template <int N, typename F>
      constexpr auto transform(F f) -> decltype(transform(f, gen_seq<N>{})) {
        return transform(f, gen_seq<N>{});
      }

      // for binary function
      template <typename F, typename T, int... Is>
      constexpr auto transform_bind1(F f, T x, seq<Is...>) -> std::array<decltype(f(x, 0)), sizeof...(Is)> {
        return {{ f(x, Is)... }};
      }

      template <int N, typename F, typename T>
      constexpr auto transform_bind1(F f, T x) -> decltype(transform_bind1(f, x, gen_seq<N>{})) {
        return transform_bind1(f, x, gen_seq<N>{});
      }

    }
  }
}
#endif  // MOG_CORE_UTIL_TRANSFORM_HPP_INCLUDED