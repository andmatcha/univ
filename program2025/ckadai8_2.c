#include <stdio.h>
#include <math.h>

int main()
{
  FILE *fp;
  int angle;
  double rad, sin_val, cos_val, tan_val;

  fp = fopen("trig_table.dat", "w");

  fprintf(fp, "angle[deg]\tsin\tcos\n");

  for (angle = 0; angle <= 360; angle += 10)
  {
    rad = angle * M_PI / 180.0;
    sin_val = sin(rad);
    cos_val = cos(rad);
    fprintf(fp, "%3d\t%.6f\t%.6f\n", angle, sin_val, cos_val);
  }

  fclose(fp);

  return 0;
}
