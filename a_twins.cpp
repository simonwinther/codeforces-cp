#include <bits/stdc++.h>
#include <cstddef>
#include <pthread.h>
#include <string>
#include <unistd.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n;
  cin >> n;

  string s;
  // vector<int> a;       // size 0: []
  // vector<int> b(3);    // size 3: [0, 0, 0]
  // vector<int> c(3, 7); // size 3: [7, 7, 7]
  // vector<int> d{3};    // size 1: [3]
  // vector<int> e{3, 7}; // size 2: [3, 7]
  vector<int> val;
  int num;

  while (cin >> num) {
    val.push_back(num);
  }

  int total = 0;
  for (int c : val) {
    total += c;
  }

  int left = 0;
  int right = total;

  int cnt = 0;

  for (int c : val) {
    left += c;
    right -= c;
    cnt++;
    if (left > right) {
      cout << cnt;
      break;
    }
  }

  return 0;
}
