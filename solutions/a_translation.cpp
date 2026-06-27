// {{{ Imports
#include <bits/stdc++.h> // vector, string, algorithm, iostream, thread, etc.
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

  string s;
  getline(cin, s);

  string t;
  getline(cin, t);

  reverse(t.begin(), t.end());
  cout << (t.compare(s) == 0 ? "YES" : "NO");
}
