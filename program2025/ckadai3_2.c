#include <stdio.h>
#include <math.h>

int main()
{
  double a, b, c;

  printf("2次方程式 ax^2 + bx + c = 0 の係数を入力してください。\n");
  printf("a = ");
  scanf("%lf", &a);
  printf("b = ");
  scanf("%lf", &b);
  printf("c = ");
  scanf("%lf", &c);

  if (a == 0)
  {
    printf("aは0でない値を入力してください。\n");
    return 1;
  }

  double discriminant = b * b - 4 * a * c;

  if (discriminant <= 0)
  {
    printf("判別式が正でないため、2つの実数解は存在しません。\n");
    return 1;
  }

  double sqrt_discriminant = sqrt(discriminant);
  double x1 = (-b + sqrt_discriminant) / (2 * a);
  double x2 = (-b - sqrt_discriminant) / (2 * a);

  printf("2つの実数解は次の通り:\n");
  printf("x1 = %lf\n", x1);
  printf("x2 = %lf\n", x2);

  return 0;
}
