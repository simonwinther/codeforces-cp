#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(0);
  cin.tie(0);

  set<char> s1;
  string s;
  cin >> s;

  for (auto c : s) {
    s1.insert(c);
  }

  cout << (s1.size() % 2 == 0 ? "CHAT WITH HER!" : "IGNORE HIM!") << endl;

  return 0;
}
