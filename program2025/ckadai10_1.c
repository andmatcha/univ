#include <stdio.h>

int main()
{
  // ポインタpcへの加算
  char c;
  char *pc = &c;

  for (int j = 0; j < 6; j++)
  {
    if (j == 0)
    {
      printf("pc: ");
    }
    else
    {
      printf("pc+%d: ", j);
    }
    printf("%p\n", pc + j);
  }

  // ポインタpiへの減算
  int i;
  int *pi = &i;

  for (int j = 0; j < 6; j++)
  {
    if (j == 0)
    {
      printf("pi: ");
    }
    else
    {
      printf("pi-%d: ", j);
    }
    printf("%p\n", pi - j);
  }

  return 0;
}
