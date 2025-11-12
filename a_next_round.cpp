#include <bits/stdc++.h>
#include <cstdio>

using namespace std;

int main() {
  ios::sync_with_stdio(0);
  cin.tie(0);

  int n, k;
  cin >> n >> k;
  vector<int> contests_scores;

  while (n--) {
    int x;
    cin >> x;
    contests_scores.push_back(x);
  }
  k -= 1; // zero indexed
  int thr = contests_scores[k];
  int r = 0;
  for (int i = 0; i < contests_scores.size(); i++) {
    if (contests_scores[i] >= thr && contests_scores[i] != 0) {
      r += 1;
      continue;
    }
  }
  cout << r << endl;
  return 0;
}
