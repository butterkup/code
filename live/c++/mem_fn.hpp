#ifndef SNN_MEMBER_FUNCTION_POINTER
#define SNN_MEMBER_FUNCTION_POINTER

#include <concepts>
#include <type_traits>
#include <utility>

namespace snn::functional {
  template <typename Sign, typename Class>
    requires std::is_member_function_pointer_v<Sign Class::*>
  class MemFunc {
    using function_sig = Sign Class::*;
    template <typename... Args>
    using return_t = std::invoke_result_t<Sign, Args...>;
    function_sig member_function;

  public:
    MemFunc() = delete;

    MemFunc(Sign Class::*const &memfn): member_function{memfn} { }

    MemFunc(Sign Class::*&&memfn): member_function{std::move(memfn)} { }

    template <typename Cls, typename... Args>
      requires(std::same_as<return_t<Args...>, void>)
    void operator()(Cls &&instance, Args &&...args) {
      (std::forward<Cls>(instance).*
       this->member_function)(std::forward<Args>(args)...);
    }

    template <typename Cls, typename... Args>
      requires(not std::same_as<return_t<Args...>, void>)
    return_t<Args...> operator()(Cls &&instance, Args &&...args) {
      return (std::forward<Cls>(instance).*
              this->member_function)(std::forward<Args>(args)...);
    }
  };

  template <typename Sig, typename Class, typename Cls, typename... Args>
    requires std::same_as<std::invoke_result_t<Sig, Args...>, void>
  void call_member(Sig Class::*&&memfn, Cls &&instance, Args &&...args) {
    (std::forward<Class>(instance).*memfn)(std::forward<Args>(args)...);
  }

  template <typename Sig, typename Class, typename Cls, typename... Args>
    requires(not std::same_as<std::invoke_result_t<Sig, Args...>, void>)
  decltype(auto) call_member(Sig Class::*&&memfn, Cls &&instance,
                             Args &&...args) {
    return (std::forward<Cls>(instance).*memfn)(std::forward<Args>(args)...);
  }

  template <typename Sign, typename Class>
  MemFunc<Sign, Class> mem_fn(Sign Class::*&&memfn) {
    return std::forward<Sign Class::*>(memfn);
  }
} // namespace snn::functional

#endif // SNN_MEMBER_FUNCTION_POINTER
