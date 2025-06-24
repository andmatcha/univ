#include <stdio.h>

int main()
{
  double A[2][2]; // 入力行列
  double invA[2][2]; // 逆行列
  double det; // 行列式
  int i, j;

  // 入力
  printf("2次行列Aの要素を入力:\n");
  for (i = 0; i < 2; i++)
  {
    for (j = 0; j < 2; j++)
    {
      printf("A[%d][%d] = ", i, j);
      scanf("%lf", &A[i][j]);
    }
  }

  // 行列式
  det = A[0][0] * A[1][1] - A[0][1] * A[1][0];

  if (det == 0)
  {
    printf("impossible\n");
    return 0;
  }

  // 逆行列
  invA[0][0] = A[1][1] / det;
  invA[0][1] = -A[0][1] / det;
  invA[1][0] = -A[1][0] / det;
  invA[1][1] = A[0][0] / det;

  // 出力
  printf("逆行列:\n");
  printf("%.6f %.6f\n", invA[0][0], invA[0][1]);
  printf("%.6f %.6f\n", invA[1][0], invA[1][1]);

  return 0;
}
