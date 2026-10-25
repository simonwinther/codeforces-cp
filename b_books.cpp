#include <algorithm>
#include <bits/stdc++.h>
#include <pthread.h>
#include <unistd.h>
#include <unordered_map>
#include <vector>

// {{{ Aliases
using ll = long long;
using vi = std::vector<int>;
using vll = std::vector<ll>;
// }}}

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, t;
  cin >> n >> t;

  vll a(n), books_num;
  for (ll& x : a) cin >> x;

  return 0;
}

int too_slow() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, t;
  cin >> n >> t;

  vll a(n), books_num;
  for (ll& x : a) cin >> x;

  for (int i = 0, r = i; i < n; i++, r = i) {
    ll current_t = 0, books = 0;
    while (r < n && current_t + a[r] <= t) {
      current_t += a[r];
      books += 1;
      r += 1;
    }
    books_num.push_back(books);
  }

  if (books_num.empty()) {
    cout << 0 << endl;
    return 0;
  }

  auto it = max_element(books_num.begin(), books_num.end());
  cout << *it << "\n";

  return 0;
}
