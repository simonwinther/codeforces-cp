#include <bits/stdc++.h>
#include <pthread.h>
#include <unistd.h>

using namespace std;

void transform(string &s, int (*casing)(int)) {
  for (size_t i = 0; i < s.length(); i++) {
    char character = s.at(i);
    s[i] = (char)casing((int)character);
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  cin >> s;

  int upper = 0, lower = 0;

  for (size_t i = 0; i < s.length(); i++) {
    char character = s.at(i);
    if (isupper(character))
      upper += 1;
    else
      lower += 1;
  }

  if (upper > lower) {
    transform(s, toupper);
  } else {
    transform(s, tolower);
  }

  cout << s;
  return 0;
}
