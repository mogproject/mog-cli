#ifndef MOG_CORE_UTIL_ARRAY_HPP_INCLUDED
#define MOG_CORE_UTIL_ARRAY_HPP_INCLUDED

#include "seq.hpp"

namespace mog {
  namespace core {
    namespace util {

      template <typename T, int N>
      struct Array {
        typedef T* iterator;
        typedef T const* const_iterator;

        T elems[N];

        constexpr bool operator==(Array<T, N> rhs) const {
          for (auto i = 0; i < N; ++i) if (elems[i] != rhs.elems[i]) return false;
          return true;
        }

        constexpr T& operator[](size_t n){ return elems[n]; }
        constexpr T const& operator[](size_t n) const { return elems[n]; }

        constexpr size_t size() const { return N; }

        constexpr iterator begin() noexcept {
          return &elems[0];
        }

        constexpr const_iterator begin() const noexcept {
          return &elems[0];
        }

        constexpr iterator end() noexcept {
          return &elems[0] + N;
        }
        constexpr const_iterator end() const noexcept {
          return &elems[0] + N;
        }
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