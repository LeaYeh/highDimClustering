#include "global.h"
#define MAX_DIM 1024 // allow to have up to 1024 dimension
int dataPointSize = 0, dataDimension = 0;

void DatasetRead(char *filePath, float *point);
void PrintDataPoint(float *points);
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
  //printf("%5.2f ", *(points));
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
        *(point+data_index) = atof(pch);
        data_index++;
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





