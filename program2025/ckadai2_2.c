#include <stdio.h>

int main(void)
{
  int a, b, c, d, e;

  printf("a=");
  scanf("%d", &a);
  printf("b=");
  scanf("%d", &b);
  printf("c=");
  scanf("%d", &c);
  printf("d=");
  scanf("%d", &d);
  printf("e=");
  scanf("%d", &e);

  int f = ((a + b) - (c / d)) * e;

  printf("%d\n", f);

  return 0;
}
