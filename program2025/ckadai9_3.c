#include <stdio.h>

int main()
{
  int a[10];
  int i, j, temp;

  // 入力
  printf("10個の整数を入力:\n");
  for (i = 0; i < 10; i++)
  {
    printf("a[%d] = ", i);
    scanf("%d", &a[i]);
  }

  // ソート
  for (i = 0; i < 9; i++)
  {
    for (j = 0; j < 9 - i; j++)
    {
      if (a[j] > a[j + 1])
      {
        temp = a[j];
        a[j] = a[j + 1];
        a[j + 1] = temp;
      }
    }
  }

  // 出力
  printf("\n並び替え結果:\n");
  for (i = 0; i < 10; i++)
  {
    printf("%d ", a[i]);
  }
  printf("\n");

  return 0;
}
