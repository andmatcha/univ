#include <stdio.h>
#include <math.h>

int main()
{
  double data[10];
  double sum = 0.0, mean, variance = 0.0, stddev;
  int i;

  // 入力
  printf("10個の実数を入力:\n");
  for (i = 0; i < 10; i++)
  {
    scanf("%lf", &data[i]);
    sum += data[i];
  }

  // 平均
  mean = sum / 10;

  // 分散
  for (i = 0; i < 10; i++)
  {
    variance += (data[i] - mean) * (data[i] - mean);
  }
  variance /= 10;

  // 標準偏差
  stddev = sqrt(variance);

  // 出力
  printf("平均: %.6f\n", mean);
  printf("分散: %.6f\n", variance);
  printf("標準偏差: %.6f\n", stddev);

  return 0;
}
