#include <Chirale_TensorFlowLite.h>
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "rep_counting_model.cc"  // your .tflite model converted as C array

void setup() {
  Serial.begin(9600);
  Serial.println("TensorFlow Lite Micro is set up!");
}

void loop() {}
