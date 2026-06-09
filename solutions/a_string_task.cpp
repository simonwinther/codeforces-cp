#include <bits/stdc++.h>
#include <cstddef>
using namespace std;

const vector<char> is_vowel = {'a', 'o', 'y', 'e', 'u', 'i'};

int vowel(char x) {
  for (size_t i = 0; i < is_vowel.size(); i++) {
    if (x == is_vowel[i]) {
      return 1;
    }
  }
  return 0;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s;
  cin >> s;

  for (size_t i = 0; i < s.length(); i++) {
    char letter = (char)tolower(s.at(i));
    if (vowel(letter)) {
      continue;
    }
    cout << "." << letter;
  }

  return 0;
}
