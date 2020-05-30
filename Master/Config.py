
PRINTVALUESTOCONSOLE = True
SERIALENABLED = True

if(SERIALENABLED):
    # The serial port of the arduino
    PORT = 'COM5'

    # The baud rate with which the serial connection will communicate
    BAUD_RATE = 115200


# Input controller device
DEVICE = 'Wireless Controller'
if(DEVICE=='Wireless Controller'):
    THROTTLEINDEX = 1
    STEERINGINDEX = 0
elif(DEVICE=='PS4CONTROLLER'):
    THROTTLEINDEX = 1
    STEERINGINDEX = 0

# Enable joystick for pan-tilt system

PANTILTENABLED = True

if(PANTILTENABLED):
    PANTILTDEVICE = 'Wireless Controller'
    if(PANTILTDEVICE=='Wireless Controller'):
        PANINDEX = 2
        TILTINDEX = 3

# (Between 0 and 1) minimum value that controller needs to be changed in order to send changes to arduino
JOYSTICKRESOLUTION = 10e-3

# Min and max value for mapping output values to
MINVALUEMAPOUTPUT = 0
MAXVALUEMAPOUTPUT = 4096

# Min and max value for mapping input values to
MINVALUEMAPINPUT = -1
MAXVALUEMAPINPUT = 1

MINVALUEMAPINPUT_STEERING = -4
MAXVALUEMAPINPUT_STEERING = 4

MINVALUEMAPINPUT_THROTTLE = -5
MAXVALUEMAPINPUT_THROTTLE = 5






