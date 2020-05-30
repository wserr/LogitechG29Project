import pygame
import Config

# Controls devices through pygame
# Possible controllers: one to control the car, one to control the camera pan-tilt system
# The pan-tilt controller is optional. You can disable it in the config settings
class ControllerManager:
    def __init__(self):
        self._initialize()
        self._initializeCarController()
        self._initializePanTiltController()

    def _initialize(self):
        pygame.init()
        pygame.joystick.init()
        self.JoystickCount = pygame.joystick.get_count()
        print("Number of joysticks connected: {}".format(self.JoystickCount))

    def  _initializeCarController(self):
        self._CarController = self._getJoystickByName(Config.DEVICE)

        if(self._CarController==None):
            raise Exception("_CarController '{}' was not found in the list of connected controllers.".format(Config.DEVICE))

        print("CarController connected: '{}'".format(self._CarController.get_name()))
        self._CarController.init()
        self.ThrottleValue = 0
        self.SteeringValue = 0

    def _initializePanTiltController(self):
        if(Config.PANTILTENABLED):
            self._PanTiltController = self._getJoystickByName(Config.PANTILTDEVICE)

            if (self._PanTiltController==None):
                raise Exception("PanTilt Control is enabled, but controller '{}' was not found in the list of connected controllers.".format(Config.PANTILTDEVICE))
            print("PanTiltController connected: '{}'".format(self._PanTiltController.get_name()))
            self._PanTiltController.init()
            self.PanValue = 0
            self.TiltValue = 0
        else:
            self.PanValue = None
            self.TiltValue = None


    def _getJoystickByName(self,name):
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for device in joysticks:
            if(device.get_name()==name):
                return device
        return None

    def ReadJoystickValues(self):
        pygame.event.pump()
        self.ThrottleValue = self._CarController.get_axis(Config.THROTTLEINDEX)
        self.SteeringValue = self._CarController.get_axis(Config.STEERINGINDEX)

        if(Config.PANTILTENABLED==True):
            self.PanValue = self._PanTiltController.get_axis(Config.PANINDEX)
            self.TiltValue = self._PanTiltController.get_axis(Config.TILTINDEX)

    def Dispose(self):
        pygame.joystick.quit()

if __name__ == '__main__':
    cm = ControllerManager()

    while True:
        cm.ReadJoystickValues()
        print("{} {} {} {}".format(cm.ThrottleValue,cm.SteeringValue,cm.PanValue,cm.TiltValue))