#include <algorithm>
#include <cstddef>
#include <iostream>
#include <vector>

using namespace std;

vector<vector<int>> merge_intervals(vector<vector<int>> xss) {
  sort(xss.begin(), xss.end());
  vector<vector<int>> r;
  for (size_t i = 0; i < xss.size() - 1; i++) {
    vector<int> xs = xss[i];
    vector<int> next = xss[i + 1];
    if (next[0] < xs[1]) {
      // Merge
      // New interval becomes [xs[0], next[1]]
      r.push_back({xs[0], next[1]});
      i++;
    } else {
      r.push_back({xs[0], xs[1]});
    }
  }
  return r;
}

void pp(vector<vector<int>> xss) {
  cout << "[";
  for (vector<int> &xs : xss) {
    cout << "[";
    for (int &x : xs) {
      cout << x;
      if (&x == &xs.back())
        continue;
      cout << ", ";
    }
    cout << "]";
    if (&xs == &xss.back())
      continue;
    cout << ", ";
  }
  cout << "]";
}

int main() {
  pp(merge_intervals({{1, 3}, {2, 6}, {8, 10}, {15, 18}}));
  return 0;
}
