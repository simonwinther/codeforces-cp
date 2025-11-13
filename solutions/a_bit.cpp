
#include <bits/stdc++.h>
#include <cstddef>
#include <cstdint>
using namespace std;

int main() {
  ios::sync_with_stdio(0);
  cin.tie(0);

  int n;
  cin >> n;
  int r = 0;
  while (n--) {
    string s;
    cin >> s;
    size_t len = s.length();
    if (s[0] == '+' || s[0] == '-') {
      r += s[0] == '+' ? 1 : -1;
    } else {
      // Does not start with +, so check if it ends, otherwise just X? which i
      // don't think is allowed it should always contain a operation
      if (s[len - 1] == '+' || s[len - 1] == '-') {
        r += s[len - 1] == '+' ? 1 : -1;
      }
    }
  }
  cout << r << endl;
  return 0;
}
