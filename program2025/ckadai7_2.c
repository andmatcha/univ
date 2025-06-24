#include <stdio.h>
#include <math.h>

int main()
{
  int angle;
  double rad, sin_val, cos_val;

  printf("angle[deg]\t sin\t\t cos\n");

  for (angle = 0; angle <= 360; angle += 10)
  {
    // 度->ラジアン変換
    rad = angle * M_PI / 180.0;
    // 三角関数の計算
    sin_val = sin(rad);
    cos_val = cos(rad);
    // 出力
    printf("%3d\t\t %.6f\t %.6f\n", angle, sin_val, cos_val);
  }

  return 0;
}
