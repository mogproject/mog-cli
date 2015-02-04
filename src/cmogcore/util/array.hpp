#ifndef MOG_CORE_UTIL_ARRAY_HPP_INCLUDED
#define MOG_CORE_UTIL_ARRAY_HPP_INCLUDED

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
        template <typename T, int N>
        constexpr util::Array<T, N> iterate(T (*f)(int)) {
          util::Array<T, N> xs = {{}};
          for (int i = 0; i < N; ++i) xs[i] = f(i);
          return xs;
        }

        /**
         * Make N-element array with filling the given value.
         */
        template <typename T, int N>
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