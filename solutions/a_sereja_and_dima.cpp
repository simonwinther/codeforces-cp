#include <bits/stdc++.h>
#include <pthread.h>
#include <unistd.h>
#include <unordered_map>

// {{{ Aliases
#define ll long long
using vi = std::vector<int>;
// }}}

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n;
  cin >> n;

  vi arr(n);

  for (int &x : arr) {
    cin >> x;
  }

  // 0 = Dima, 1 is Sereja
  pmr::unordered_map<bool, ll> sums;

  bool sereja_turn = 1; // 0 = Dima, 1 is Sereja

  ll lp = 0;
  ll rp = n - 1;

  while (lp <= rp) {
    if (arr[lp] > arr[rp]) {
      sums[sereja_turn] += arr[lp];
      lp++;
    } else {
      sums[sereja_turn] += arr[rp];
      rp--;
    }
    sereja_turn = !sereja_turn;
  }

  cout << sums[1] << " " << sums[0] << endl;

  return 0;
}

int compact() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n;
  cin >> n;

  vi arr(n);
  for (int &x : arr)
    cin >> x;

  // 0 = Dima, 1 is Sereja
  pmr::unordered_map<bool, ll> sums;

  bool sereja_turn = 1; // 0 = Dima, 1 is Sereja
  ll lp = 0;
  ll rp = n - 1;

  while (lp <= rp) {
    bool left = arr[lp] > arr[rp];
    sums[sereja_turn] += arr[left ? lp++ : rp--];
    sereja_turn = !sereja_turn;
    // (left ? lp : rp) = (left ? lp + 1 : rp - 1);
  }
  cout << sums[1] << " " << sums[0] << endl;

  return 0;
}
