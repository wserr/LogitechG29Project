import pygame
import sys
import time
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
    ser = serial.Serial('COM5', 115200)
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
    maxValue = 4095
    axes = Joystick.get_numaxes()
    print('Numer of axes: {}'.format(axes))
    name = Joystick.get_name()
    print('Name of joystick: {}'.format(name))
    while True:
        pygame.event.pump()
        ser.flushInput()
        ser.flushOutput()
        axis2 = Joystick.get_axis(0)
        axis1 = Joystick.get_axis(1)
        axis1Value = (translate(axis1,-6,6,0,maxValue))
        axis2Value = (translate(axis2,-2,2,0,maxValue))
        # Throttle
        sendValues1 = (axis1Value).to_bytes(2,'little') #struct.pack('>B',axis1Value)
        ser.write(sendValues1)

        # Steering
        sendValues2 = (axis2Value).to_bytes(2,'little')#struct.pack('>B',axis2Value)
        ser.write(sendValues2)

        time.sleep(0.03)
        print(ser.readline())

except Exception as e:
    print('Error while reading joystick: {}'.format(str(e)))
finally:
    ser.close()

    
    
    


            
    

