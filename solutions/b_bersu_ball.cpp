#include <bits/stdc++.h>
#include <pthread.h>
#include <unistd.h>

// {{{ Aliases
using ll = long long;
using vi = std::vector<int>;
using vll = std::vector<ll>;
// }}}

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n;
  cin >> n;
  vi boys(n);
  for (auto& x : boys) cin >> x;

  int m;
  cin >> m;
  vi girls(m);
  for (auto& x : girls) cin >> x;

  sort(girls.begin(), girls.end());
  sort(boys.begin(), boys.end());

  int b = 0, g = 0, cnt = 0;

  while (b < n && g < m) {
    if (abs(boys[b] - girls[g]) <= 1) {
      b++, g++, cnt++;
      continue;
    }
    (boys[b] <= girls[g] ? b : g)++;
  }

  cout << cnt << "\n";

  return 0;
}
