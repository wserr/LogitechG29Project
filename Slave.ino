#include <MCP4922.h>
#include <SPI.h>


// 2 DACs
MCP4922 DAC1(16,15,7,14);
MCP4922 DAC2(16,15,8,14);

union ArrayToInteger {
  byte array[2];
  int output;
};

// used to map incoming values to DAC values
int minimum = 0;
int maximum = 4095;

//Values that will be read from RPi
int cmd = 0;
int steerPosition = 0;
int throttlePosition = 0;
int aux1Position = 0;
int aux2Position = 0;

// Store previous values as well; set DAC only when difference
int prevSteerPosition = 0;
int prevThrottlePosition = 0;
int prevAux1Position = 0;
int prevAux2Position = 0;

// Threshold for data change (range: 0-4095)
int dataThreshold = 1;

ArrayToInteger converter;



void setup() {
  Serial.begin(115200);
  SPI.begin();
}

void loop() {
  receiveData();
  setDACs();


}

void setDACs()
{
  if (dataChanged(prevSteerPosition,steerPosition) || dataChanged(prevThrottlePosition,throttlePosition))
  {
    DAC1.Set(steerPosition,throttlePosition);
    delay(10);
  }

  if (dataChanged(prevAux1Position,aux1Position) || dataChanged(prevAux2Position,aux2Position))
  {
    DAC2.Set(aux1Position,aux2Position);
    delay(10);
  }
}

void receiveData()
 {
    // We expect 5 bytes to return from RPi
    while(Serial.available()) 
    {

        // Store previous values
        prevSteerPosition = steerPosition;
        prevThrottlePosition = throttlePosition;
        prevAux1Position = aux1Position;
        prevAux2Position = aux2Position;

        converter = {Serial.read(),Serial.read()};

        steerPosition = converter.output; //map(Serial.read(),minimum,maximum,dacMinimum,dacMaximum);
        
        converter = {Serial.read(),Serial.read()};

        throttlePosition = converter.output; //map(Serial.read(),minimum,maximum,dacMinimum,dacMaximum);
        //aux1Position = map(Serial.read(),minimum,maximum,dacMinimum,dacMaximum);
        //aux2Position = map(Serial.read(),minimum,maximum,dacMinimum,dacMaximum);
        
        Serial.println(throttlePosition);
        Serial.flush();
    }
}

bool dataChanged(int prevValue, int value)
{
  return true;
  if(abs(prevValue-value)>dataThreshold) return true; else return false;
}