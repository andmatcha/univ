#include <stdio.h>

int main()
{
  int id;

  printf("学籍番号を入力してください: ");
  scanf("%d", &id);

  if (id < 10000000 || id > 99999999)
  {
    printf("8桁の整数を入力してください。\n");
    return 1;
  }

  int upper = id / 10000;
  int lower = id % 10000;

  printf("上4桁: %04d\n", upper);
  printf("下4桁: %04d\n", lower);

  return 0;
}
