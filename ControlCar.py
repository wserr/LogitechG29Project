import pygame
import sys
from time import sleep
import serial
import struct

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

try:
    ser = serial.Serial('COM3', 115200, timeout=0)
    print('Serial device connected')
except Exception as e:
    print('No serial connection found')
    print(e)
    sys.exit()

try:
    pygame.init()
    pygame.joystick.init()

    Joystick = pygame.joystick.Joystick(0)
    Joystick.init()

    print('Joystick enabled')
except:
    print('No Joystick found')
    sys.exit()
    
try:
    maxValue = 255
    axes = Joystick.get_numaxes()
    print('Numer of axes: {}'.format(axes))
    name = Joystick.get_name()
    print('Name of joystick: {}'.format(name))
    while True:
        pygame.event.pump()
        ser.flushInput()
        ser.flushOutput()
        axis1 = Joystick.get_axis(1)
        axis2 = Joystick.get_axis(0)
        axis1Value = (translate(axis1,-6,6,0,255))
        axis2Value = (translate(axis2,1,-1,0,maxValue))
        sendValues1 = struct.pack('>B',axis1Value)
        ser.write(sendValues1)
        sendValues2 = struct.pack('>B',axis2Value)
        ser.write(sendValues2)
        print('{}     {}'.format(axis1Value,axis2Value))

except Exception as e:
    print('Error while reading joystick: {}'.format(str(e)))
finally:
    ser.close()

    
    
    


            
    

