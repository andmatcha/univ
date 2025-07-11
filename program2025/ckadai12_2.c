#include <stdio.h>

typedef struct ex
{
  int n;
  double m;
} ex_t;

void swap_st(ex_t *x, ex_t *y)
{
  ex_t temp = *x;
  *x = *y;
  *y = temp;
}

int main(void)
{
  ex_t a, b;

  // 入力
  printf("aの値を入力:\nn=");
  scanf("%d", &a.n);
  printf("m=");
  scanf("%lf", &a.m);
  printf("bの値を入力:\nn=");
  scanf("%d", &b.n);
  printf("m=");
  scanf("%lf", &b.m);

  // 入れ替え前
  printf("\n入れ替え前\na={n:%d, m=%lf}, b={n:%d, m=%lf}", a.n, a.m, b.n, b.m);

  // 入れ替え
  swap_st(&a, &b);

  // 入れ替え後
  printf("\n入れ替え後\na={n:%d, m=%lf}, b={n:%d, m=%lf}", a.n, a.m, b.n, b.m);

  return 0;
}
