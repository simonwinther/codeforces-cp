#include <bits/stdc++.h>
#include <pthread.h>
#include <unistd.h>

using ll = long long;

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll n;
  cin >> n;

  // 4744000695826
  // log10(n)=12.67614474=13.

  int times = (int)ceil(log10(n));
  int cnt = 0;

  for (int i = 0; i < times; i++) {
    ll digit = n % 10;
    cnt += (digit == 4 || digit == 7);
    n /= 10;
  }
  if (cnt == 4 || cnt == 7) {
    cout << "YES" << endl;
  } else {
    cout << "NO" << endl;
  }
  return 0;
}

int without_log10() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll n;
  cin >> n;

  int cnt = 0;

  while (n > 0) {
    int digit = n % 10;
    if (digit == 4 || digit == 7)
      cnt++;
    n /= 10;
  }

  cout << (cnt == 4 || cnt == 7 ? "YES" : "NO") << '\n';

  return 0;
}
