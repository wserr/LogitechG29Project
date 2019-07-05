#include <Wire.h>
#include <SPI.h>
#include <MCP4922.h>

const int dacChipSelectPin1 = 7;
const int dacChipSelectPin2 = 8;


long minimum = 0;
long maximum = 255;


#define SLAVE_ADDRESS 0x08
int cmd = 0;
int steerPosition = 0;
int throttlePosition = 0;
int aux1Position = 0;
int aux2Position = 0;

int prevSteerPosition = 0;
int prevThrottlePosition = 0;
int prevAux1Position = 0;
int prevAux2Position = 0;


void setup() {
  Serial.begin(9600); // start serial for output
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);
  
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  
  
  Serial.println("Ready!");
  SPI.begin();
}

void loop() 
{
  setDac(0,0,dacChipSelectPin1);
  setDac(0,1,dacChipSelectPin1);
  delay(10);
//  if (dataChanged(prevSteerPosition, steerPosition))
//  {
//    setDac(steerPosition,0,dacChipSelectPin1);
//    Serial.println("SP changed");
//    delay(10);
//  }
//  if (dataChanged(prevThrottlePosition, throttlePosition))
//  {
//    setDac(throttlePosition,1,dacChipSelectPin1);
//    Serial.println("TP changed");
//    delay(10);
//  }
//  if (dataChanged(prevAux1Position, aux1Position))
//  {
//    setDac(aux1Position,0,dacChipSelectPin2);
//    Serial.println("A1 changed");
//    delay(10);
//  }
//  if (dataChanged(prevAux2Position, aux2Position))
//  {
//    setDac(aux2Position,1,dacChipSelectPin2);
//    Serial.println("A2 changed");
//    delay(10);
//  }

}

// callback for received data
void receiveData(int byteCount)
 {
    if(Wire.available()>=5) 
    {
        cmd = Wire.read();
        prevSteerPosition = steerPosition;
        prevThrottlePosition = throttlePosition;
        prevAux1Position = aux1Position;
        prevAux2Position = aux2Position;
        steerPosition = Wire.read();
        throttlePosition = Wire.read();
        aux1Position = Wire.read();
        aux2Position = Wire.read();
        // print al values
        steerPosition = map(steerPosition,minimum,maximum,0,4095);
        throttlePosition = map(throttlePosition,maximum,minimum,0,4095);
        aux1Position = map(aux1Position,maximum,minimum,0,4095);
        aux2Position = map(aux2Position,maximum,minimum,0,4095);
        // Serial.print(cmd); Serial.print("  "); Serial.print(steerPosition); Serial.print("  "); Serial.print(throttlePosition); Serial.print("  "); Serial.print(aux1Position); Serial.print("  "); Serial.println(aux2Position);
    }

}

bool dataChanged(int prevValue, int value)
{
  if(abs(prevValue-value)>10)
  {
    return true;
  }
  else
  {
    return false;
  }
}

void setDac(int value, int channel, const int chipSelect)
{
  byte dacRegister = 0b00110000;
  int dacSecondaryByteMask = 0b0000000011111111;
  byte dacPrimaryByte = (value>>8)|dacRegister;
  byte dacSecondaryByte = value & dacSecondaryByteMask;
  switch(channel)
  {
    case 0:
      dacPrimaryByte &= 127;
    break;
    case 1:
      dacPrimaryByte |= (1<<7);
    break;
  }

  
  //noInterrupts();
  digitalWrite(chipSelect,LOW);
  SPI.transfer(dacPrimaryByte);
  SPI.transfer(dacSecondaryByte);
  digitalWrite(chipSelect,HIGH);
  //interrupts();
  
}
