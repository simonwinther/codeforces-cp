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

  int n, t;
  cin >> n >> t;

  vll num(n);
  for (ll &x : num)
    cin >> x;

  return 0;
}
