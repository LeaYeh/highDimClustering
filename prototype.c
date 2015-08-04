#include "golbal.h"

void DatasetRead (char *filename, const int &dataNum, const int &dimNum);

int main (int argc, char *argv[]) {
  float pa, pb;
  int dataPointSize, dataDimension;

  DatasetRead('a', dataPointSize, dataDimension);  

  return 0;
}

void DatasetRead (char *filename, const int &dataNum, const int &dimNum) {
  dataNum = 1;

}
