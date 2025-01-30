#include <fstream>
#include <gmpxx.h>
#include <iomanip>
#include <iostream>

int main() {
  std::ofstream file("fibs.cpp.txt", std::ios::out | std::ios::trunc);
  mpf_set_default_prec(512);
  mpz_class a = 0, b = 1;
  for (int i = 0; i < 60'000; i++) {
    std::cout << '\r' << i;
    a += b;
    std::swap(a, b);
    file << b << '\n';
  }
  std::cout << "\nGolden Ratio: " << std::setprecision(100) << ((mpf_class)b / a) << '\n';
}
