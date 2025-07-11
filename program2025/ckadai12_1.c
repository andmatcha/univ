#include <stdio.h>
#include <string.h>

int main(void)
{
  typedef struct lecture
  {
    char name[10];
    char day[4]; /*Mon or Tue*/
    int period;  /*1-4*/
  } lecture_t;

  lecture_t lectures[] = {
      {
          "Japanese",
          "Mon",
          1,
      },
      {
          "Math",
          "Mon",
          2,
      },
      {
          "PE",
          "Mon",
          3,
      },
      {
          "PE",
          "Mon",
          4,
      },
      {
          "Science",
          "Tue",
          1,
      },
      {
          "English",
          "Tue",
          2,
      },
      {
          "Society",
          "Tue",
          3,
      },
      {
          "Music",
          "Tue",
          4,
      },
  };

  // 入力
  char day[4];
  printf("曜日を入力(Mon/Tue): ");
  scanf("%3s", day);

  // 絞り込み
  int array_length = sizeof(lectures) / sizeof(lecture_t);
  for (int i = 0; i < array_length; i++)
  {
    if (strcmp(lectures[i].day, day) == 0)
    {
      printf("name: %s, period: %d\n", lectures[i].name, lectures[i].period);
    }
  }

  return 0;
};
