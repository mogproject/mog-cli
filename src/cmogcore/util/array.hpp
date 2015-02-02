#ifndef MOG_CORE_UTIL_ARRAY_HPP_INCLUDED
#define MOG_CORE_UTIL_ARRAY_HPP_INCLUDED

namespace mog {
  namespace core {
    namespace util {

      template <typename T, int N>
       struct array{
         T v[N];
         constexpr T& operator[](size_t n){ return v[n]; }
         constexpr T const& operator[](size_t n) const { return v[n]; }
       };

     }
   }
 }

 #endif  // MOG_CORE_UTIL_ARRAY_HPP_INCLUDED