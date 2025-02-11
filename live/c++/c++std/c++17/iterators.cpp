#include <cstdlib>
#include <initializer_list>
#include <iostream>
#include <iterator>
#include <utility>
#include <vector>

template <typename T>
struct Vector {
  typedef T *pointer;
  typedef const T *const_pointer;

  typedef std::ptrdiff_t difference_type;
  typedef pointer iterator;
  typedef const_pointer const_iterator;
  typedef std::reverse_iterator<iterator> reverse_iterator;
  typedef std::reverse_iterator<const_iterator> const_reverse_iterator;
  typedef T value_type;
  typedef std::random_access_iterator_tag iterator_category;
  typedef std::size_t size_type;

  pointer _ptr;
  std::size_t _size, _capacity;

  Vector(): _ptr(nullptr), _size(0), _capacity(0) { }
  Vector(std::initializer_list<T> const &vals)
    : _ptr(nullptr), _size(0), _capacity(0) {
    _grow_if_needed(vals.size());
    for(T const &val : vals) {
      _ptr[_size++] = val;
    }
  }

  size_type size() const { return _size; }
  size_type capacity() const { return _capacity; }
  bool empty() const { return _size > 0; }

  void push_back(T const &ele) {
    _grow_if_needed(1);
    _ptr[_size++] = ele;
  }

  void pop_back() { _ptr[_size--].~T(); }

  template <typename... A>
  void emplace(A &&...args) {
    _grow_if_needed(1);
    new(_ptr + _size++) T(std::forward<A>(args)...);
  }

  iterator begin() const { return _ptr; }
  const_pointer cbegin() const { return begin(); }
  reverse_iterator rbegin() const { return end(); }
  const_reverse_iterator crbegin() const { return rbegin(); }
  iterator end() const { return _ptr + _size; }
  const_pointer cend() const { return end(); }
  reverse_iterator rend() const { return begin(); }
  const_reverse_iterator crend() const { return rend(); }

  void _grow_if_needed(std::size_t n = 1) {
    if(_ptr == nullptr) {
      _ptr = static_cast<T *>(std::malloc(8 * sizeof(T)));
    } else if(_capacity - _size < n) {
      T *buffer =
        static_cast<T *>(std::realloc(_ptr, _capacity * 2 * sizeof(T)));
      if(buffer == _ptr)
        return;
      for(std::size_t i = 0; i < _size; i++) {
        buffer[i] = std::move(_ptr[i]);
        _ptr[i].~T();
      }
      _capacity += n;
      std::free(_ptr);
      _ptr = buffer;
    }
  }
  void clear() {
    for(std::size_t i = 0; i < _size; i++) {
      _ptr[i].~T();
    }
    _size = 0;
  }
  ~Vector() {
    clear();
    if(_ptr) {
      std::free(_ptr);
    }
  }
};

auto main() -> int {
  Vector numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9};
  for(auto start = std::cbegin(numbers); start != std::cend(numbers);
      start = std::next(start)) {
    std::cout << *start << '\n';
  }

  std::iterator_traits<std::vector<int>> h;

  for(auto start : std::reverse_iterator(numbers)) {
    std::cout << start << '\n';
  }
  for(auto i : numbers) {
    std::cout << i << " * " << i << " = " << (i * i) << '\n';
  }
  return 0;
}
