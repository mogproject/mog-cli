#ifndef MOG_CORE_UTIL_BIND_HPP_INCLUDED
#define MOG_CORE_UTIL_BIND_HPP_INCLUDED

namespace mog {
  namespace core {
    namespace util {

      // binder object for binary function
      template <typename Fn, typename T>
      class binder1st {
       public:
        typedef T value_type;

       protected:
        Fn op;
        value_type value;

       public:
        constexpr binder1st(Fn const& fn, value_type const& x): op(fn), value(x) {}

        template <typename U>
        constexpr decltype(std::declval<Fn const&>()(std::declval<value_type const&>(), std::declval<U const&>()))
        operator()(U const& x) const {
          return op(value, x);
        }
      };

      template<typename Fn, typename T>
      inline constexpr binder1st<Fn, T> bind1st(Fn const& fn, T const& x) {
        return binder1st<Fn, T>(fn, typename binder1st<Fn, T>::value_type(x));
      }

    }
  }
}
#endif  // MOG_CORE_UTIL_BIND_HPP_INCLUDED