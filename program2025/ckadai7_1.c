#include <stdio.h>
#include <math.h>

// 標準偏差を計算
double SD(double x, double y, double z)
{
  double mean = (x + y + z) / 3.0; // 平均
  double variance = ((x - mean) * (x - mean) +
                     (y - mean) * (y - mean) +
                     (z - mean) * (z - mean)) /
                    3.0; // 分散
  return sqrt(variance);
}

int main()
{
  double x, y, z, s;

  // 入力
  printf("x = ");
  scanf("%lf", &x);
  printf("y = ");
  scanf("%lf", &y);
  printf("z = ");
  scanf("%lf", &z);
  // 計算
  s = SD(x, y, z);
  // 出力
  printf("標準偏差: %.6f\n", s);

  return 0;
}
