#include <stdio.h>

int main()
{
  int a[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
  int *p = &a[0];
  int s = 0;

  // ポインタ演算で配列の要素を加算
  for (int i = 0; i < 10; i++)
  {
    s += *(p + i);
  }
  printf("s = %d\n", s);
}
