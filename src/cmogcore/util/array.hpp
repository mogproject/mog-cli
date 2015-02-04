#ifndef MOG_CORE_UTIL_ARRAY_HPP_INCLUDED
#define MOG_CORE_UTIL_ARRAY_HPP_INCLUDED

#include "seq.hpp"

namespace mog {
  namespace core {
    namespace util {

      template <typename T, int N>
      struct Array {
        T v[N];
        constexpr T& operator[](size_t n){ return v[n]; }
        constexpr T const& operator[](size_t n) const { return v[n]; }
      };

      namespace array {
        /**
         * Make N-element array of [f(0), f(1), ... f(N-1)] from unary function f.
         */
        template <int N, typename Fn>
        constexpr auto iterate(Fn fn) -> util::Array<decltype(fn(0)), N> {
          util::Array<decltype(fn(0)), N> xs = {{}};
          for (int i = 0; i < N; ++i) xs[i] = fn(i);
          return xs;
        }

        /**
         * Make N-element array with filling the given value.
         */
        template <int N, typename T>
        constexpr util::Array<T, N> fill(T value) {
          util::Array<T, N> xs = {{}};
          for (int i = 0; i < N; ++i) xs[i] = value;
          return xs;
        }
      }

     }
   }
 }

 #endif  // MOG_CORE_UTIL_ARRAY_HPP_INCLUDED