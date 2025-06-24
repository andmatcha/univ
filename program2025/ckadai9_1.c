#include <stdio.h>

int main()
{
  int A[2][2], B[2][2], C[2][2], D[2][2];
  int i, j, k;

  // 行列Aの入力
  printf("2次行列Aの要素を入力:\n");
  for (i = 0; i < 2; i++)
  {
    for (j = 0; j < 2; j++)
    {
      printf("A[%d][%d] = ", i, j);
      scanf("%d", &A[i][j]);
    }
  }

  // 行列Bの入力
  printf("2次行列Bの要素を入力してください:\n");
  for (i = 0; i < 2; i++)
  {
    for (j = 0; j < 2; j++)
    {
      printf("B[%d][%d] = ", i, j);
      scanf("%d", &B[i][j]);
    }
  }

  // 行列C = A + B
  for (i = 0; i < 2; i++)
  {
    for (j = 0; j < 2; j++)
    {
      C[i][j] = A[i][j] + B[i][j];
    }
  }

  // 行列D = AB
  for (i = 0; i < 2; i++)
  {
    for (j = 0; j < 2; j++)
    {
      D[i][j] = 0;
      for (k = 0; k < 2; k++)
      {
        D[i][j] += A[i][k] * B[k][j];
      }
    }
  }

  // 行列Cの出力
  printf("\n行列C = A + B:\n");
  for (i = 0; i < 2; i++)
  {
    for (j = 0; j < 2; j++)
    {
      printf("%d ", C[i][j]);
    }
    printf("\n");
  }

  // 行列Dの出力
  printf("\n行列D = AB:\n");
  for (i = 0; i < 2; i++)
  {
    for (j = 0; j < 2; j++)
    {
      printf("%d ", D[i][j]);
    }
    printf("\n");
  }

  return 0;
}
