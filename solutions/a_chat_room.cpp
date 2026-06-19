#include <bits/stdc++.h>
#include <pthread.h>
#include <unistd.h>

#define ll long long

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s;
  cin >> s;
  vector<char> candidates = {'h', 'e', 'l', 'l', 'o'};
  string::reverse_iterator it = s.rbegin();
  while (it != s.rend() && !candidates.empty()) {
    if (candidates.back() == *it)
      candidates.pop_back();
    ++it;
  }
  cout << (candidates.empty() ? "YES" : "NO");
  return 0;
}
