#include <stdio.h>

int main()
{
  char letter;

  printf("小文字のアルファベットを1文字入力: ");
  scanf("%c", &letter);

  if (letter >= 'a' && letter <= 'z')
  {
    char upper = letter - ('a' - 'A');
    printf("大文字: %c\n", upper);
  }
  else
  {
    printf("小文字のアルファベットではありません\n");
  }

  return 0;
}
