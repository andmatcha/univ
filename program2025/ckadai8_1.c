#include <stdio.h>
#include <string.h>

int main()
{
  char input[4];

  // 入力
  printf("yes / no を入力: ");
  scanf("%s", input);

  // 比較と出力
  if (strcmp(input, "yes") == 0)
  {
    printf("good\n");
  }
  else if (strcmp(input, "no") == 0)
  {
    printf("bad\n");
  }

  return 0;
}
