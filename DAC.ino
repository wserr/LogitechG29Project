//
//Dit is een test voor de RC auto met besturing dmv stuurwiel.
//Het potentiometer signaal wordt in de arduino binnengelezen en dan omgezet in een analoog signaal dmv de DAC.
//Hier met 2 potentiometers


#include <SPI.h>

const int dacChipSelectPin1 = 7;
const int dacChipSelectPin2 = 8;


long minimum = 0;
long maximum = 255;

long steerPosition;
long throttlePosition;

long aux1Position;
long aux2Position;

int i = 200;
int x = 5;



void setup() 
{
  pinMode(dacChipSelectPin1,OUTPUT);
  pinMode(dacChipSelectPin2,OUTPUT);
  digitalWrite(dacChipSelectPin1,HIGH);
  digitalWrite(dacChipSelectPin2,HIGH);


  SPI.begin();
  SPI.setBitOrder(MSBFIRST);
  SPI.setDataMode(SPI_MODE0);

  Serial.begin(9600);

}

void loop() 
{
  if (Serial.available() > 0)
  {
    steerPosition = Serial.read();
    Serial.write(steerPosition);
    
  }

/*  while (Serial.available())
 { 
    steerPosition = Serial.parseInt();
    throttlePosition = Serial.parseInt();
    aux1Position = Serial.parseInt();
    aux2Position = Serial.parseInt();
    steerPosition = map(steerPosition,minimum,maximum,0,4095);
    throttlePosition = map(throttlePosition,maximum,minimum,0,4095);
    aux1Position = map(aux1Position,maximum,minimum,0,4095);
    aux2Position = map(aux2Position,maximum,minimum,0,4095);
    setDac(steerPosition,0,dacChipSelectPin1);
    setDac(throttlePosition,1,dacChipSelectPin1);

    setDac(aux1Position,0,dacChipSelectPin2);
    setDac(aux2Position,1,dacChipSelectPin2);

    Serial.println(steerPosition);
    Serial.println(throttlePosition);
    Serial.println(aux1Position);
    Serial.println(aux2Position);
 } */
}

// test method
// void loop()
// {
//   for(int i = 0 ; i < 4096 ; i++)
//   {
//    setDac(4095-i,0,dacChipSelectPin1); 
//    setDac(i,1,dacChipSelectPin1); 
//    setDac(4095-i,0,dacChipSelectPin2); 
//    setDac(i,1,dacChipSelectPin2); 
//    Serial.print (analogRead(A0)); Serial.print("  "); Serial.print (analogRead(A1)); Serial.print("  "); Serial.print (analogRead(A2)); Serial.print("  "); Serial.println (analogRead(A3));
//   }
// }
  
  




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

  
  noInterrupts();
  digitalWrite(chipSelect,LOW);
  SPI.transfer(dacPrimaryByte);
  SPI.transfer(dacSecondaryByte);
  digitalWrite(chipSelect,HIGH);
  interrupts();
  
}