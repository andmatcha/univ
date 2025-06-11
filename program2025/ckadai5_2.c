#include <stdio.h>

int main()
{
  int a = 0;
  int b = 0;

  // (1)
  for (int k = 100; k <= 1000; k++)
  {
    a += 2 * k + 5;
  }

  // (2)
  for (int i = 1; i <= 20; i++)
  {
    for (int j = 1; j <= 50; j++)
    {
      b += 2 * i + 3 * j;
    }
  }

  // 結果
  printf("(a, b) = (%d, %d)\n", a, b);

  return 0;
}
