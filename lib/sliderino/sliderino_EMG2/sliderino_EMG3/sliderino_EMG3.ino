// 070121
/*
sliderUSBOut()
When serial is available, the arduino will print a time stamp and 12-bit potentiometer position at the sampling rate.
Eatai Roth, 2017
*/

// const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to

// //unsigned int sensorValue;        // value read from the pot
// float startTime;
// union{float asFloat; byte asBytes[4];}t;
// union{unsigned int asUInt; byte asBytes[4];}sensorValue;
// char serInput;

// void setup() {
//   // initialize serial communications:
//   Serial.begin(115200);
//   while(!Serial);
  
// //  analogReadResolution(12);

//   startTime = micros();
//   t.asFloat = 0;
// }

// void loop() {
//   if (Serial.available()){
//     serInput = Serial.read();

//     // If read value is 'g', serial is expecting Data to be written
//     if (serInput == 0x67){
//       t.asFloat = (micros()-startTime)/1000000.0; 
//       sensorValue.asUInt = analogRead(analogInPin);
//       Serial.write(t.asBytes, 4);
//       Serial.write(sensorValue.asBytes, 4);
//     }

//     // If read value is 'a', restart timer
//     else if (serInput == 0x61){
//       //clearUSBRecBuffer();
//       startTime = micros();
//     }
// }

// //void clearUSBRecBuffer(){
// //  while(SerialUSB.available()){
// //    SerialUSB.read();
// //  }
// }



// 060321 
#define MAX 150     //maximum posible reading. TWEAK THIS VALUE!!
int reading[10];
int finalReading;
byte multiplier = 1;

float startTime;
union{float asFloat; byte asBytes[4];}t;
union{unsigned int asUInt; byte asBytes[4];}sensorValue;
char serInput;

void setup(){
 Serial.begin(9600); //begin serial communications
 while(!Serial);
 startTime = micros();
 t.asFloat = 0;
}

void loop(){
 for(int i = 0; i < 10; i++){    //take ten readings in ~0.02 seconds
   reading[i] = analogRead(A0) * multiplier;
   delay(10);
 }
 for(int i = 0; i < 10; i++){   //average the ten readings
   finalReading += reading[i];
 }
 finalReading /= 100;

 if (!Serial.available()){
//    serInput = Serial.read();

//    if (serInput == 0x67){
 
     t.asFloat = (micros()-startTime)/1000000.0; 
     sensorValue.asUInt = finalReading;
     Serial.write(t.asBytes, 4);
     Serial.write(sensorValue.asBytes, 4);
   
     Serial.println(finalReading);
//    }

   // If read value is 'a', restart timer
//    else if (serInput == 0x61){
//     clearUSBRecBuffer();
//     startTime = micros();

//    }

 }

}

// 060321 another try
    
///*
//sliderUSBOut()
//When serial is available, the arduino will print a time stamp and 12-bit potentiometer position at the sampling rate.
//Eatai Roth, 2017
//*/
//
//#define MAX 150     //maximum posible reading. TWEAK THIS VALUE!!
//int reading[10];
//int finalReading;
//byte multiplier = 1;
//
//const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
//
////unsigned int sensorValue;        // value read from the pot
//float startTime;
//union{float asFloat; byte asBytes[4];}t;
//union{unsigned int asUInt; byte asBytes[4];}sensorValue;
//char serInput;
//
//void setup() {
//  // initialize serial communications:
//  Serial.begin(9600);
////  while(!Serial);
//  
////  analogReadResolution(12);
//
//  startTime = micros();
//  t.asFloat = 0;
//}
//
//void loop() {
//  for(int i = 0; i < 10; i++){    //take ten readings in ~0.02 seconds
//    reading[i] = analogRead(A0) * multiplier;
//    delay(2);
//  }
//  for(int i = 0; i < 10; i++){   //average the ten readings
//    finalReading += reading[i];
//  }
//  finalReading /= 100;
////  finalReading = constrain(finalReading, 0, MAX);
//  Serial.print(finalReading);
//  Serial.print("\t");
//  finalReading = constrain(finalReading, 0, MAX);
////  if (Serial.available()){
////    serInput = Serial.read();
//
//    // If read value is 'g', serial is expecting Data to be written
////    if (serInput == 0x67){
////      t.asFloat = (micros()-startTime)/1000000.0; 
////      sensorValue.asUInt = finalReading;
////      sensorValue.asUInt = analogRead(analogInPin);
////      Serial.write(t.asBytes, 4);
////      Serial.write(sensorValue.asBytes, 4);
////      Serial.print(sensorValue.asUInt);
//
//      
//      
//      
////    }
//
////    // If read value is 'a', restart timer
////    else if (serInput == 0x61){
////      //clearUSBRecBuffer();
////      startTime = micros();
////    }
////}
//
////void clearUSBRecBuffer(){
////  while(SerialUSB.available()){
////    SerialUSB.read();
////  }
//}
