#include <MCP4922.h>
#include <SPI.h>

// 2 DACs
MCP4922 DAC1(16, 15, 7, 14);
MCP4922 DAC2(16, 15, 8, 14);

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
int panPosition = 0;
int tiltPosition = 0;

// Store previous values as well; set DAC only when difference
int prevSteerPosition = 0;
int prevThrottlePosition = 0;
int prevPanPosition = 0;
int prevTiltPosition = 0;

// Threshold for data change (range: 0-4095)
int dataThreshold = 1;

ArrayToInteger converter;

void setup()
{
  Serial.begin(115200);
  SPI.begin();
}

void loop()
{
  receiveData();
  delay(10);
  setDACsWithoutChecks();
  delay(10);
}

void setDACsWithoutChecks()
{
  DAC1.Set(steerPosition,throttlePosition);
  DAC2.Set(panPosition, tiltPosition);
}

void setDACs()
{
  if (dataChanged(prevSteerPosition, steerPosition) || dataChanged(prevThrottlePosition, throttlePosition))
  {
    DAC1.Set(steerPosition, throttlePosition);
    delay(10);
  }

  if (dataChanged(prevPanPosition, panPosition) || dataChanged(prevTiltPosition, tiltPosition))
  {
    DAC2.Set(panPosition, tiltPosition);
    delay(10);
  }
}

void receiveData()
{
  // We expect 4 bytes to return from RPi
  while (Serial.available())
  {

    // Store previous values
    prevSteerPosition = steerPosition;
    prevThrottlePosition = throttlePosition;
    prevPanPosition = panPosition;
    prevTiltPosition = tiltPosition;

    converter = {Serial.read(), Serial.read()};
    throttlePosition = converter.output;

    delay(2);

    converter = {Serial.read(), Serial.read()};
    steerPosition = converter.output;

    delay(2);


    converter = {Serial.read(), Serial.read()};
    panPosition = converter.output;

    delay(2);

    converter = {Serial.read(), Serial.read()};
    tiltPosition = converter.output;

    delay(2);


    Serial.print(throttlePosition);
    Serial.print(" ");
    Serial.print(steerPosition);
    Serial.print("  ");
    Serial.print(panPosition);
    Serial.print("  ");
    Serial.println(tiltPosition);
    Serial.flush();
  }
}

bool dataChanged(int prevValue, int value)
{
  return true;
  if (abs(prevValue - value) > dataThreshold)
    return true;
  else
    return false;
}