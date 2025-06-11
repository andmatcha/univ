#include <stdio.h>

int main()
{
  int n, sum = 0, i = 1;

  printf("正の整数 n を入力: ");
  scanf("%d", &n);

  if (n <= 0)
  {
    printf("エラー: 正の整数を入力してください\n");
    return 1;
  }

  while (i <= n)
  {
    sum += i;
    i++;
  }

  printf("1 から %d までの和は %d です。\n", n, sum);

  return 0;
}
