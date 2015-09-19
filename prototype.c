#include "global.h"
float pa, pb;
float avg_x, avg_y, avg_z;
float avg_xy, avg_xz, avg_yz, avg_xyz;

void DatasetRead(char *filePath, float *point);
void PrintDataPoint(float *points);
void setInit_3d(float *points);

int main (int argc, char *argv[]) {
  // filePath need able to user input 
  char *filePath = "dataset/sipu_dataset/dim3.txt";
  float *points;
  
  if (argc < 3) {
    printf("required [point_size, dim]\n");
    return -1;
  } else {
    dataPointSize = atoi(argv[1]);
    dataDimension = atoi(argv[2]);
    points = (float *)malloc(sizeof(float) * dataPointSize * dataDimension);
    printf("dataPointSize = %d, dataDimension = %d\n", dataPointSize, dataDimension);
  } /*else if (!argv[1] || argv[2] < 3) {
    printf("point_size can not be 0, and dimension must >= 3\n");
  }*/
  DatasetRead(filePath, points);
  PrintDataPoint(points);
  setInit_3d(points);

  return 0;
}
void PrintDataPoint(float *points) {
  int i, j;

  for (i = 0; i < dataPointSize; i++) {
    for (j = 0; j < dataDimension; j++) {
      printf("%10.2f ", *(points+(i*dataDimension + j)));//points[i*dataDimension + j]);
    }
    printf("\n");
  }
  printf("[finish] print dataset.\n");
}
void setInit_3d(float *points) {
  float sum_x = 0, sum_y = 0, sum_z = 0;
  float sum_xy = 0, sum_xz = 0, sum_yz = 0;
  float sum_xyz = 0;
  int i, j;

  for (i = 0; i < dataPointSize*dataDimension; i += dataDimension) {
    //if (i % dataDimension == 0) {
      sum_x += points[i];
      sum_y += points[i+1];
      sum_z += points[i+2];
      sum_xy += points[i] * points[i+1];
      sum_xz += points[i] * points[i+2];
      sum_yz += points[i+1] * points[i+2];
      sum_xyz += points[i] * points[i+1] * points[i+2];
    //} 
  }
  avg_x = (float)(sum_x / dataPointSize);
  avg_y = sum_y / dataPointSize;
  avg_z = sum_z / dataPointSize;
  avg_xy = sum_xy / dataPointSize;
  avg_xz = sum_xz / dataPointSize;
  avg_yz = sum_yz / dataPointSize;
  avg_xyz = sum_xyz / dataPointSize;
  printf("avg_x = %5.2f, avg_y = %5.2f, avg_z = %5.2f\n", avg_x, avg_y, avg_z);
  printf("avg_xy = %5.2f, avg_xz = %5.2f, avg_yz = %5.2f\n", avg_xy, avg_yz, avg_xz);
  printf("avg_xyz = %5.2f\n", avg_xyz);
}
void DatasetRead(char *filePath, float *point) {
  FILE *fp = NULL;
  char input[MAX_DIM*20];
  char *line;
  char *pch = NULL;
  int data_index = 0;
  int i;
  
  fp = fopen(filePath,"r");
  //point = (float *)malloc(sizeof(float) * dataPointSize * dataDimension);
  while (fgets(input, MAX_DIM*20, fp)) {
    line = strdup(input);
    while (pch = strsep(&line, " ,;\n")) {
      if (strlen(pch) > 0) { 
        //printf("%.2f\n", atof(pch));
        //point[data_index++] = atof(pch);
        point[data_index++] = atof(pch);
        if (data_index == dataPointSize*dataDimension) {
          fclose(fp);
          printf("[success] read dataset.\n");
          return;
        }
        //printf("t1 = %d, t2 = %d\n", data_index, dataDimension*dataPointSize);
        //printf("|%f|, ", point[data_index-1]);
      }
    }
  }
  fclose(fp);
  printf("[success] read dataset.\n");
}





