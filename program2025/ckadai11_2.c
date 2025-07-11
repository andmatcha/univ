#include <stdio.h>

void swap_array(int *x, int *y)
{
  int temp;
  for (int i = 0; i < 5; i++)
  {
    temp = *(x + i);
    *(x + i) = *(y + i);
    *(y + i) = temp;
  }
}

void input_array(char *name, int *array)
{
  printf("配列%sの要素を5つ入力:\n", name);
  for (int i = 0; i < 5; i++)
  {
    printf("%s[%d]=", name, i);
    scanf("%d", &array[i]);
  }
}

void output_array(char *name, int *array)
{

  printf("%s=[%d,%d,%d,%d,%d]\n", name, array[0], array[1], array[2], array[3], array[4]);
}

int main()
{
  int a[5], b[5];

  // 入力
  input_array("a", a);
  input_array("b", b);

  // 入れ替え前
  printf("\n入れ替え前:\n");
  output_array("a", a);
  output_array("b", b);

  // 入れ替え
  swap_array(a, b);

  // 入れ替え結果
  printf("\n入れ替え後:\n");
  output_array("a", a);
  output_array("b", b);

  return 0;
}
