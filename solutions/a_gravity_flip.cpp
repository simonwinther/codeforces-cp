// {{{ Imports
#include <bits/stdc++.h>
// }}}
// {{{ Aliases
using ll = long long;
using vi = std::vector<int>;
using vll = std::vector<ll>;
// }}}

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cols;
  cin >> cols;

  vll colval(cols);
  for (auto& x : colval) cin >> x;

  sort(colval.begin(), colval.end());

  for (auto& x : colval) cout << x << " ";

  return 0;
}
