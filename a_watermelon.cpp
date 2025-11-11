#include <stdio.h>

int main() {
  int w;
  scanf("%d", &w);

  printf("%s", w % 2 == 0 && w > 2 ? "YES" : "NO");
}
