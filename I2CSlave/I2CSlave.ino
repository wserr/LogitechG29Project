#include <Wire.h>
#include <SPI.h>
#include <MCP4922.h>


// 2 DACs
MCP4922 DAC1(16,15,7,14);
MCP4922 DAC2(16,15,8,14);

//i2c communication setup with RPi
#define SLAVE_ADDRESS 0x08

// used to map incoming values to DAC values
int minimum = 0;
int maximum = 255;

int dacMinimum = 0;
int dacMaximum = 4095;

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

// Threshold for data change (0-4095)
int dataThreshold = 10;



void setup() {
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  SPI.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (dataChanged(prevSteerPosition,steerPosition) || dataChanged(prevThrottlePosition,throttlePosition))
  {
    DAC1.Set(steerPosition,throttlePosition);
    Serial.println("DAC1 set");
    delay(10);
  }

  if (dataChanged(prevAux1Position,aux1Position) || dataChanged(prevAux2Position,aux2Position))
  {
    DAC2.Set(aux1Position,aux2Position);
    Serial.println("DAC2 set");
    delay(10);
  }
}


// Callback for received data from RPi
void receiveData(int byteCount)
 {
    // We expect 5 bytes to return from RPi
    if(Wire.available()>=5) 
    {
        // Command byte (not implemented as of now)
        cmd = Wire.read();

        // Store previous values
        prevSteerPosition = steerPosition;
        prevThrottlePosition = throttlePosition;
        prevAux1Position = aux1Position;
        prevAux2Position = aux2Position;

        // Get new values
        steerPosition = map(Wire.read(),minimum,maximum,dacMinimum,dacMaximum);
        throttlePosition = map(Wire.read(),minimum,maximum,dacMinimum,dacMaximum);
        aux1Position = map(Wire.read(),minimum,maximum,dacMinimum,dacMaximum);
        aux2Position = map(Wire.read(),minimum,maximum,dacMinimum,dacMaximum);
        
        // Print all values (for testing)
        // Serial.print(cmd); Serial.print("  "); Serial.print(steerPosition); Serial.print("  "); Serial.print(throttlePosition); Serial.print("  "); Serial.print(aux1Position); Serial.print("  "); Serial.println(aux2Position);
    }

}

bool dataChanged(int prevValue, int value)
{
  if(abs(prevValue-value)>dataThreshold) return true; else return false;
}
