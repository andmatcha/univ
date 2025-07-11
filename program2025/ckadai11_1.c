#include <stdio.h>

void swap(int *x, int *y)
{
  int temp = *x;
  *x = *y;
  *y = temp;
}

int main()
{
  int a, b;

  // 入力
  printf("a=");
  scanf("%d", &a);
  printf("b=");
  scanf("%d", &b);

  // 入れ替え
  swap(&a, &b);

  // 出力
  printf("入れ替え結果: a=%d, b=%d\n", a, b);

  return 0;
}
