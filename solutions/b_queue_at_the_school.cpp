#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(0);
  cin.tie(0);

  int n, t;
  cin >> n >> t;

  string s;
  cin >> s;
  for (int _ = 0; _ < t; _++) {
    for (int j = 0; j < n - 1; j++) {
      if (s[j] == 'B' && s[j + 1] == 'G') {
        s[j] = 'G';
        s[j + 1] = 'B';
        j++;
      }
    }
  }
  cout << s << endl;
  return 0;
}
