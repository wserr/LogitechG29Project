from inputs import get_gamepad
import sys
from time import sleep
import serial
import struct
import json
import threading
import smbus
import time

# Global variables
UseArduino = 0
PrintValuesToConsole = 0
ArduinoDeviceName = ""
ControllerIndex = 0
SteeringWheelCode = ""
GasPedalCode = ""

ABS_X = ""
ABS_Y = ""
ABS_RX = ""
ABS_RY = ""

ev = None
bus = None

address = 0x08

class ExportValues:
    def __init__(self, x,y,rx,ry):
        self.x = x
        self.y = y
        self.rx = rx
        self.ry = ry


def Export():
    timer = threading.Timer(0.05, Export)
    timer.daemon = True
    timer.start()
    global ev
    global bus
    global address


    if (ev != None):
        if PrintValuesToConsole:
            print(ev.x,ev.y,ev.rx,ev.ry)

        if UseArduino:
            bus.write_i2c_block_data(address,255,[ev.x,ev.y,ev.rx,ev.ry])


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

try:
    with open('config.json') as config_file:
        data = json.load(config_file)
    UseArduino = data['UseArduino']
    PrintValuesToConsole = data['PrintValuesToConsole']
    ArduinoDeviceName = data['ArduinoDeviceName']
    ControllerIndex = data['ControllerIndex']
    SteeringWheelCode = data['SteeringWheelCode']
    GasPedalCode = data ['GasPedalCode']
    ABS_X = data['ABS_X']
    ABS_Y = data['ABS_Y']
    ABS_RX = data['ABS_RX']
    ABS_RY = data['ABS_RY']

except:
    print(sys.exc_info())
    sys.exit()

if UseArduino:
    try:
        bus = smbus.SMBus(1)       
    except Exception as e:
        print(e)
        sys.exit()


    
try:   
    Value_X = 128
    Value_Y = 128
    Value_RX = 128
    Value_RY = 128
    Export()
    while True:
        Events  = get_gamepad()
        for event in Events:
            if event.code == ABS_X:
                Value_X = event.state
            elif event.code == ABS_Y:
                Value_Y = event.state
            elif event.code == ABS_RX:
                Value_RX = event.state
            elif event.code == ABS_RY:
                Value_RY = event.state
            ev = ExportValues(Value_X,Value_Y,Value_RX,Value_RY)
except:
    print(sys.exc_info())






            
    

