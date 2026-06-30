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

  int t;
  cin >> t;

  vector<char> gt = {'y', 'e', 's'};

  while (t--) {
    string s;
    cin >> s;

    int ok = true;
    for (std::string::size_type i = 0; i < s.length(); i++) {
      ok &= (gt.at(i) == tolower(s.at(i)));
    }

    cout << (ok ? "YES" : "NO") << "\n";
  }

  return 0;
}
