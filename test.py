import pygame
import sys
import time
import struct


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
    axes = Joystick.get_numaxes()
    print('Numer of axes: {}'.format(axes))
    name = Joystick.get_name()
    print('Name of joystick: {}'.format(name))
    while True:
        pygame.event.pump()
        axis1 = Joystick.get_axis(0)
        axis2 = Joystick.get_axis(1)
        axis3 = Joystick.get_axis(2)
        axis4 = Joystick.get_axis(3)
        print("{0:.3f} {1:.3f} {2:.3f} {3:.3f}".format(axis1,axis2,axis3,axis4))


except Exception as e:
    print('Error while reading joystick: {}'.format(str(e)))