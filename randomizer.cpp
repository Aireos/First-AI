#include <ctime>
#include <iostream>
using namespace std
// c = current percent
// i = ideal percent
// o = overall percent
// p = percent change

bool isCurrentSecondEven() {
    std::time_t now = std::time(nullptr);
    std::tm* local_time = std::localtime(&now);
    
    // Returns true if even, false if odd
    return (local_time->tm_sec % 2 == 0);
  }

int RandomNumberPicker({) {
  for 
}

bool tof(float i,float p){
  float c = 50;
  float o;
  if (isCurrentSecondEven()){
    if (c >= i){
      c-=p;
    }else{
      c+=p;
    }
  }else{
    if 
  }
}
