#ifndef MOG_CORE_UTIL_SEQ_HPP_INCLUDED
#define MOG_CORE_UTIL_SEQ_HPP_INCLUDED

namespace mog {
  namespace core {
    namespace util {
      template <int... Is>
      struct seq {};

      template <int N, int... Is>
      struct gen_seq: gen_seq<N - 1, N - 1, Is...> {};

      /**
       * e.g. gen_seq<5> -> seq<0, 1, 2, 3, 4>
       */
      template <int... Is>
      struct gen_seq<0, Is...>: seq<Is...> {};
    }
  }
}
#endif  // MOG_CORE_UTIL_SEQ_HPP_INCLUDED