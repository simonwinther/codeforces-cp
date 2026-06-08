#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t;
  cin >> t;

  while (t--) {
    int n;
    cin >> n;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {
      cin >> a[i];
    }

    sort(a.begin(), a.end());

    long long x = a[n / 2];

    int left = 0;
    int right = 0;

    for (int i = 0; i < n; i++) {
      if (a[i] < x)
        left++;
      else if (a[i] > x)
        right++;
    }

    cout << max(left, right) << '\n';
  }

  return 0;
}
