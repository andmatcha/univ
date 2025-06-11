#include <stdio.h>

int main()
{
  int channel;

  printf("チャンネル番号を入力: ");
  scanf("%d", &channel);

  switch (channel)
  {
  case 1:
    printf("NHK-G\n");
    break;
  case 2:
    printf("NHK-E\n");
    break;
  case 3:
    printf("TVK\n");
    break;
  case 4:
    printf("NTV\n");
    break;
  case 5:
    printf("TV Asahi\n");
    break;
  case 6:
    printf("TBS\n");
    break;
  case 7:
    printf("TV Tokyo\n");
    break;
  case 8:
    printf("Fuji TV\n");
    break;
  default:
    printf("NA\n");
    break;
  }

  return 0;
}
