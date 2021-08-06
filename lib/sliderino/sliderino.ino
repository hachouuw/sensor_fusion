
//Slider setup (A2)
unsigned long timer = 0;
long loopTime = 10000;   // microseconds
const int analogInPinSlider = A2;

//EMG1 setup (A0)
double reading[100];
double finalReading;
const int analogInPinEMG1 = A0; //bicep

//EMG2 setup (A1)
double reading2[100];
double finalReading2;
const int analogInPinEMG2 = A1; //tricep

void setup() {
  Serial.begin(115200);
  timer = micros();
}

void loop() {
  timeSync(loopTime);

  //Slider
  double val = analogRead(analogInPinSlider); //Slider min 0-max 674

  //EMG1, A0
  for(int i = 0; i < 100; i++){    //take ten readings in ~0.02 seconds
    reading[i] = analogRead(analogInPinEMG1);
    delay(2);
  }
  for(int i = 0; i < 100; i++){   //average the ten readings
    finalReading += reading[i];
  }
  finalReading = finalReading /100; 
  

  //EMG2, A1
  for(int i = 0; i < 100; i++){    //take ten readings in ~0.02 seconds
    reading2[i] = analogRead(analogInPinEMG2);
    delay(2);
  }
  for(int i = 0; i < 100; i++){   //average the ten readings
    finalReading2 += reading2[i];
  }
  finalReading2 = finalReading2 /100;  
 
  //sendToPC(&fusion);

  sendToPC(&finalReading, &finalReading2, &val); //A0, A1. A2
}

//void sendToPC(double* data)
//{
//  byte* byteData = (byte*)(data);
//  Serial.write(byteData, 4);
//  //Serial.write(buf, sizeof(buf)); //an array to send as a series of bytes
//}

void sendToPC(double* data1, double* data2, double* data3)
{
  byte* byteData1 = (byte*)(data1);
  byte* byteData2 = (byte*)(data2);
  byte* byteData3 = (byte*)(data3);
  byte buf[12] = {byteData1[0], byteData1[1], byteData1[2], byteData1[3],
                 byteData2[0], byteData2[1], byteData2[2], byteData2[3],
                 byteData3[0], byteData3[1], byteData3[2], byteData3[3]};
  Serial.write(buf, 12);
}

void timeSync(unsigned long deltaT)
{
  unsigned long currTime = micros();
  long timeToDelay = deltaT - (currTime - timer);
  if (timeToDelay > 5000)
  {
    delay(timeToDelay / 1000);
    delayMicroseconds(timeToDelay % 1000);
  }
  else if (timeToDelay > 0)
  {
    delayMicroseconds(timeToDelay);
  }
  else
  {
      // timeToDelay is negative so we start immediately
  }
  timer = currTime + timeToDelay;
}
