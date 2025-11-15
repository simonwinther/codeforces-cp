#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(0);
  cin.tie(0);

  string s;
  cin >> s;
  vector<char> nums;
  for (auto c : s) {
    if (c == '+')
      continue;
    nums.push_back(c);
  }
  sort(nums.begin(), nums.end());
  for (int i = 0; i < nums.size(); i++) {
    cout << nums[i];
    if (i == nums.size() - 1)
      continue;
    cout << "+";
  }
  return 0;
}
