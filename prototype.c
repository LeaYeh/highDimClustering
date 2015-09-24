// implement original jclin's <real-time and automatic two-class clustering by analytical formulas>
// with method 1. in page 1921
// prototype code in c language

#include "global.h"

void DatasetRead(char *filePath, float *point);
void PrintDataPoint(float *points);
void setInit_3d(float *points);
double pa, pb;
double avg_x, avg_y, avg_z;
double avg_xy, avg_xz, avg_yz, avg_xyz;
double *centroid_a, *centroid_b;

void DatasetRead(char *filePath, double *point);
void PrintDataPoint(double *points);
void setInit_3d(double *points);

int method_1(void);
int method_2(void);
int main (int argc, char *argv[]) {
  // filePath need able to user input
  char *filePath = "dataset/sipu_dataset/parse_dim3.txt";
  double *points;

  if (argc < 3) {
    printf("required [point_size, dim]\n");
    return -1;
  } else {
    dataPointSize = atoi(argv[1]);
    dataDimension = atoi(argv[2]);
    points = (double *)malloc(sizeof(double) * dataPointSize * dataDimension);
    centroid_a = (double *)malloc(sizeof(double) * dataDimension);
    centroid_b = (double *)malloc(sizeof(double) * dataDimension);
    printf("dataPointSize = %d, dataDimension = %d\n", dataPointSize, dataDimension);
  } /*else if (!argv[1] || argv[2] < 3) {
    printf("point_size can not be 0, and dimension must >= 3\n");
  }*/
  DatasetRead(filePath, points);
  PrintDataPoint(points);
  setInit_3d(points);

  return 0;
}
void PrintDataPoint(double *points) {
  int i, j;

  for (i = 0; i < dataPointSize; i++) {
    for (j = 0; j < dataDimension; j++) {
      printf("%10.2lf ", *(points+(i*dataDimension + j)));//points[i*dataDimension + j]);
    }
    printf("\n");
  }
  printf("[finish] print dataset.\n");
}
void setInit_3d(double *points) {
  double sum_x = 0, sum_y = 0, sum_z = 0;
  double sum_xy = 0, sum_xz = 0, sum_yz = 0;
  double sum_xyz = 0;
  int i, j;

  for (i = 0; i < dataPointSize*dataDimension; i += dataDimension) {
    //if (i % dataDimension == 0) {
      sum_x += points[i];
      sum_y += points[i+1];
      sum_z += points[i+2];
      //sum_xy += points[i] * points[i+1];
      //sum_xz += points[i] * points[i+2];
      //sum_yz += points[i+1] * points[i+2];
      //sum_xyz += points[i] * points[i+1] * points[i+2];
    //}
  }
  avg_x = (double)(sum_x / dataPointSize);
  avg_y = sum_y / dataPointSize;
  avg_z = sum_z / dataPointSize;
  for (i = 0; i < dataPointSize*dataDimension; i += dataDimension) {
    points[i] -= avg_x;
    points[i+1] -= avg_y;
    points[i+2] -= avg_z;
  }
  for (i = 0; i < dataPointSize*dataDimension; i += dataDimension) {
    sum_xy += points[i] * points[i+1];
    sum_xz += points[i] * points[i+2];
    sum_yz += points[i+1] * points[i+2];
    sum_xyz += points[i] * points[i+1] * points[i+2];
  }
  avg_x = avg_y = avg_z = 0;
  avg_xy = sum_xy / dataPointSize;
  avg_xz = sum_xz / dataPointSize;
  avg_yz = sum_yz / dataPointSize;
  avg_xyz = sum_xyz / dataPointSize;
  printf("avg_x = %5.2lf, avg_y = %5.2lf, avg_z = %5.2lf\n", avg_x, avg_y, avg_z);
  printf("avg_xy = %5.2lf, avg_xz = %5.2lf, avg_yz = %5.2lf\n", avg_xy, avg_yz, avg_xz);
  printf("avg_xyz = %5.2lf\n", avg_xyz);

  method_1();
}
int method_1() {
  double delta;
  double abs_avg_xy, abs_avg_xz, abs_avg_yz, abs_avg_xyz;

  abs_avg_xy = abs(avg_xy);
  abs_avg_xz = abs(avg_xz);
  abs_avg_yz = abs(avg_yz);
  abs_avg_xyz = abs(avg_xyz);
  delta = abs_avg_xyz / abs_avg_xy * abs_avg_xyz / abs_avg_xz / abs_avg_yz;
  if (delta < 1) {
    printf("method 1: Have no solution.\n\n");
    return -1;
  }
  pa = 0.5 + 0.5 * sqrt(sqrt(delta*delta + 8*delta) - delta - 2);
  pb = 1 - pa;
  printf("method 1: delta = %5.2lf, pa = %5.2lf\n", delta, pa);

  double pb_dev_pa = (double)(pb / pa);
printf("pb_dev_pa = %lf\n", pb_dev_pa);
printf("pb_dev_pa * abs_avg_xy * abs_avg_xz / abs_avg_yz = %lf\n", pb_dev_pa * abs_avg_xy * abs_avg_xz / abs_avg_yz);

  centroid_a[0] = sqrt(pb_dev_pa * abs_avg_xy * abs_avg_xz / abs_avg_yz);
  centroid_a[1] = sqrt(pb_dev_pa * abs_avg_xy * abs_avg_yz / abs_avg_xz);
  centroid_a[2] = sqrt(pb_dev_pa * abs_avg_xz * abs_avg_yz / abs_avg_xy);
  printf("Xa = %10.2lf, Ya = %10.2lf, Za = %10.2lf\n",  centroid_a[0],  centroid_a[1],  centroid_a[2]);
  printf("Xb = %10.2lf, Yb = %10.2lf, Zb = %10.2lf\n", -centroid_a[0], -centroid_a[1], -centroid_a[2]);
}
int method_2() {
  double tmp;

  if (avg_xy * avg_xz * avg_yz < 0) {
    // have no solution
    printf("method 2: Have no solution.\n\n");
    return -1;
  }
  tmp = 4 * avg_xy / avg_xyz * avg_xz * avg_yz / avg_xyz;
  tmp = 1 / (double)(1 + tmp);
  tmp = sqrt(tmp);
  pa  = 0.5 + 0.5 * tmp;
  printf("method 2: tmp = %lf, pa = %lf\n", tmp, pa);
}
void DatasetRead(char *filePath, double *point) {
  FILE *fp = NULL;
  char input[MAX_DIM*20];
  char *line;
  char *pch = NULL;
  int data_index = 0;
  int i;

  fp = fopen(filePath,"r");
  //point = (double *)malloc(sizeof(double) * dataPointSize * dataDimension);
  while (fgets(input, MAX_DIM*20, fp)) {
    line = strdup(input);
    while (pch = strsep(&line, " ,;\n")) {
      if (strlen(pch) > 0) {
        //printf("%.2lf\n", atof(pch));
        //point[data_index++] = atof(pch);
        point[data_index++] = atof(pch);
        if (data_index == dataPointSize*dataDimension) {
          fclose(fp);
          printf("[success] read dataset.\n");
          return;
        }
        //printf("t1 = %d, t2 = %d\n", data_index, dataDimension*dataPointSize);
        //printf("|%lf|, ", point[data_index-1]);
      }
    }
  }
  fclose(fp);
  printf("[success] read dataset.\n");
}


