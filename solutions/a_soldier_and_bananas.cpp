#include <iostream>
using namespace std;

int main() {
  long long k, n, w;
  cin >> k >> n >> w;

  long long total = k * w * (w + 1) / 2;
  long long borrow = total - n;

  if (borrow < 0)
    borrow = 0;

  cout << borrow << '\n';

  return 0;
}
