#include <bits/stdc++.h>
using namespace std;

// Trial division
// Main article: Trial division
//
// The most basic method of checking the primality of a given integer (n) is
// called trial division. This method divides (n) by each integer from 2 up to
// the square root of (n). Any such integer that divides (n) evenly establishes
// (n) as composite. Otherwise, (n) is prime.
//
// Integers larger than the square root do not need to be checked because,
// whenever (n = a \cdot b), one of the two factors (a) and (b) is less than or
// equal to the square root of (n).
//
// Another optimization is to check only prime numbers as factors in this range.
// For instance, to check whether 37 is prime, this method divides it by the
// primes in the range from 2 to (\sqrt{37}), which are 2, 3, and 5. Each
// division produces a nonzero remainder, so 37 is indeed prime.
//
// Although this method is simple to describe, it is impractical for testing the
// primality of large integers because the number of tests it performs grows
// exponentially as a function of the number of digits of these integers.
// However, trial division is still used with a smaller limit than the square
// root on the divisor size to quickly discover composite numbers with small
// factors before using more complicated methods on the numbers that pass this
// filter.
//
int is_prime(long long n) {
  if (n <= 1)
    return 0;
  for (int i = 2; i <= sqrt(n); i++) {
    if (n % i == 0) {
      // evenly divides means composite, o.w. prime
      return 0;
    }
  }
  // no evenly divides from [2, sqrt(n)], means prime
  return 1;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t;
  cin >> t;

  while (t--) {
    int x, k;
    cin >> x >> k;

    long long y = 0;
    // 52 * 10^4 + 52 * 10^2 + 52
    for (int i = 0; i < k; i++) {
      // If 0-9 steps=1, if 10-99 then steps=2, if 100-999 then steps=3, ...
      // x * 10^(ceil(log_10(x+1)))=ceil((x+1))
      int steps = ceil(log10(x + 1));
      //
      y += x * pow(10, steps * i);
    }
    if (is_prime(y))
      cout << "YES" << endl;
    else
      cout << "NO" << endl;
  }

  return 0;
}
