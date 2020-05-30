import Config
from ArduinoConnector import ArduinoConnector
from JoystickValueManager import JoystickValueManager
from ControllerManager import ControllerManager
import time


cm = ControllerManager()

if(Config.SERIALENABLED):
    ac = ArduinoConnector()

jvm = JoystickValueManager()

while True:
    cm.ReadJoystickValues()
    if(Config.PANTILTENABLED):
        jvm.UpdateValues(cm.ThrottleValue,cm.SteeringValue, cm.PanValue, cm.TiltValue)
    else:
        jvm.UpdateValues(cm.ThrottleValue,cm.SteeringValue)
    
    if(Config.SERIALENABLED):
        if(jvm.HasChanged):
            if(Config.PANTILTENABLED):
                ac.SendValuesToArduino(jvm.MappedThrottleValue,jvm.MappedSteeringValue,jvm.MappedPanValue,jvm.MappedTiltValue)
            else:
                ac.SendValuesToArduino(jvm.MappedThrottleValue,jvm.MappedSteeringValue)
    
    if(Config.PRINTVALUESTOCONSOLE):
        if(jvm.HasChanged):
            if(Config.SERIALENABLED):
                print("Feedback from Arduino: {}".format(ac.GetFeedbackFromArduino()))
            else:
                print("Values from python: {} {} {} {}".format(jvm.MappedThrottleValue, jvm.MappedSteeringValue, jvm.MappedPanValue, jvm.MappedTiltValue))
