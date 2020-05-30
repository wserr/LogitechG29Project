import Config
import serial
import time

class ArduinoConnector:
    def __init__(self):
        self.SerialConnection = serial.Serial(Config.PORT, Config.BAUD_RATE)
        print("Serial device connected at '{}' with baud rate {}".format(Config.PORT,Config.BAUD_RATE))

    def SendValuesToArduino(self, throttleValue,steeringValue, panValue = None, tiltValue = None):
        self._flush()
        self._writeValue(throttleValue)
        self._writeValue(steeringValue)

        if(panValue != None and tiltValue != None):
            self._writeValue(panValue)
            self._writeValue(tiltValue)

    def _flush(self):
        self.SerialConnection.flushInput()
        self.SerialConnection.flushOutput()

    def _writeValue(self,value):
        self.SerialConnection.write(value.to_bytes(2,'little'))
        time.sleep(0.001)

    def GetFeedbackFromArduino(self):
        return self.SerialConnection.readline()


if __name__ == '__main__':
    ac = ArduinoConnector()