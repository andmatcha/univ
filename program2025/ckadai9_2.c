#include <stdio.h>
#include <math.h>

// 面積を計算する関数
double Area(int n, double a)
{
  if (n <= 2)
    return -1; // 不可能な場合
  return (n * a * a) / (4 * tan(M_PI / n));
}

int main()
{
  int n;
  double a, s;

  // 入力
  printf("正n角形 n = ");
  scanf("%d", &n);
  printf("1辺の長さ a = ");
  scanf("%lf", &a);

  // 面積計算
  s = Area(n, a);

  // 出力
  if (s < 0)
  {
    printf("impossible\n");
  }
  else
  {
    printf("面積: %.6f\n", s);
  }

  return 0;
}
