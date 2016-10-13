#ifndef MOG_CORE_UTIL_RANDOM_HPP_INCLUDED
#define MOG_CORE_UTIL_RANDOM_HPP_INCLUDED

namespace mog {
namespace core {
namespace util {

/*
 * Random number generator
 *
 * @see https://en.wikipedia.org/wiki/Lehmer_random_number_generator
 */
namespace parkmiller {
const uint32_t M = 2147483647; /* 2^31 - 1 (A large prime number) */
const uint32_t A = 16807;      /* Prime root of M, passes statistical tests and produces a full cycle */
const uint32_t Q = 127773;     /* M / A (To avoid overflow on A * seed) */
const uint32_t R = 2836;       /* M % A (To avoid overflow on A * seed) */
}

constexpr uint32_t lcg_parkmiller(uint32_t seed) {
  uint32_t hi = seed / parkmiller::Q;
  uint32_t lo = seed % parkmiller::Q;
  int32_t test = parkmiller::A * lo - parkmiller::R * hi;
  if (test <= 0) test += parkmiller::M;
  return test;
}
}
}
}
#endif  // MOG_CORE_UTIL_RANDOM_HPP_INCLUDED