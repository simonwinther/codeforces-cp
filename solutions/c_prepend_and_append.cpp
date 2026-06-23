#include <bits/stdc++.h>
#include <pthread.h>
#include <unistd.h>

#define ll long long

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t;
  cin >> t;
  while (t--) {
    int n;
    string s;
    cin >> n >> s;
    int l = 0, r = n - 1;
    while ( // clang-format off
            (
              (s.at(l) == '0' && s.at(r) == '1') 
              || (s.at(l) == '1' && s.at(r) == '0')
            )
            &&
            l < r
    ){
            // clang-format on
      l++;
      r--;
    }
    cout << r - l + 1 << endl;
  }

  return 0;
}

int cleaner_main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t;
  cin >> t;
  while (t--) {
    int n;
    string s;
    cin >> n >> s;
    int l = 0, r = n - 1;
    // if they're equal it would be 1 == 1 or 0 == 0, so in case they aren't
    // equal it's literally 1 != 0 or 0 != ! makes sense.
    while (l < r && s[l] != s[r]) {
      l++;
      r--;
    }
    cout << r - l + 1 << "\n";
  }

  return 0;
}
