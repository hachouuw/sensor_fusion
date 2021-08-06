/*
sliderUSBOut()
When serial is available, the arduino will print a time stamp and 12-bit potentiometer position at the sampling rate.
Eatai Roth, 2017
*/

//unsigned int sensorValue;        // value read from the pot
float startTime;
union{float asFloat; byte asBytes[4];}t;
union{unsigned int asUInt; byte asBytes[4];}sensorValue;
char serInput;

#define MAX 150     //maximum posible reading. TWEAK THIS VALUE!!
int reading[10];
int finalReading;
byte multiplier = 1;

void setup() {
  // initialize serial communications:
  SerialUSB.begin(115200);
  while(!Serial);
  
//  analogReadResolution(12);

  startTime = micros();
  t.asFloat = 0;
}

void loop() {
  for(int i = 0; i < 10; i++){    //take ten readings in ~0.02 seconds
    reading[i] = analogRead(A0) * multiplier;
    delay(2);
  }
  for(int i = 0; i < 10; i++){   //average the ten readings
    finalReading += reading[i];
  }
  finalReading /= 10;
  
  if (SerialUSB.available()){
    serInput = SerialUSB.read();

    // If read value is 'g', serial is expecting Data to be written
    if (serInput == 0x67){
      t.asFloat = (micros()-startTime)/1000000.0; 
      sensorValue.asUInt = finalReading;
      SerialUSB.write(t.asBytes, 4);
      SerialUSB.write(sensorValue.asBytes, 4);
    }

    // If read value is 'a', restart timer
    else if (serInput == 0x61){
      //clearUSBRecBuffer();
      startTime = micros();
    }
}

//void clearUSBRecBuffer(){
//  while(SerialUSB.available()){
//    SerialUSB.read();
//  }
}
