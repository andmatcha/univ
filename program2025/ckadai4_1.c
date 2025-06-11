#include <stdio.h>

int main()
{
  int num;

  printf("正の整数を入力してください: ");
  scanf("%d", &num);

  if (num <= 0)
  {
    printf("正の整数を入力してください\n");
    return 1;
  }

  if (num % 6 == 0)
  {
    printf("6の倍数です\n");
  }
  else if (num % 2 == 0)
  {
    printf("2の倍数です\n");
  }
  else if (num % 3 == 0)
  {
    printf("3の倍数です\n");
  }
  else
  {
    printf("2の倍数でも3の倍数でもありません\n");
  }

  return 0;
}
