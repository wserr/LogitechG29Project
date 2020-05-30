import Config
import NumberHelper

class JoystickValueManager:
    def __init__(self):
        self._prevThrottleValue = 0
        self._throttleValue = 0

        self._prevSteeringValue = 0
        self._steeringValue = 0

        self._prevPanValue = 0
        self._panValue = 0

        self._prevTiltValue = 0
        self._tiltValue = 0

        self.HasChanged = False
        self.Initialization = True

        self.MappedThrottleValue = 0
        self.MappedSteeringValue = 0
        self.MappedPanValue = 0
        self.MappedTiltValue = 0

    def UpdateValues(self, thr, ste, pan=None,tlt=None):
        self.HasChanged = False
        self._updateCarControlValues(thr,ste)

        if(pan!=None and tlt!=None):
            self._updatePanTiltvalues(pan, tlt)

        if(self.Initialization):
            self.Initialization = False

    def _updateCarControlValues(self,thr,ste):
        self._prevThrottleValue = self._throttleValue
        self._prevSteeringValue = self._steeringValue
        self._throttleValue = thr
        self._steeringValue = ste
        self.MappedThrottleValue = self._mapIfNecessary(self.MappedThrottleValue,self._throttleValue, self._prevThrottleValue, Config.MINVALUEMAPINPUT_THROTTLE, Config.MAXVALUEMAPINPUT_THROTTLE)
        self.MappedSteeringValue = self._mapIfNecessary(self.MappedSteeringValue,self._steeringValue, self._prevSteeringValue, Config.MINVALUEMAPINPUT_STEERING,Config.MAXVALUEMAPINPUT_STEERING)

    def _updatePanTiltvalues(self, pan,tlt):
        self._prevTiltValue = self._tiltValue
        self._prevPanValue = self._panValue
        self._panValue = pan
        self._tiltValue = tlt
        self.MappedPanValue = self._mapIfNecessary(self.MappedPanValue,self._panValue, self._prevPanValue)
        self.MappedTiltValue = self._mapIfNecessary(self.MappedTiltValue,self._tiltValue, self._prevTiltValue)

    def _mapIfNecessary(self,mapTo, value, prevValue, customMinValueInput=None, customMaxValueInput=None):
        minInput = self._getValue2IfValue1None(customMinValueInput,Config.MINVALUEMAPINPUT)
        maxInput = self._getValue2IfValue1None(customMaxValueInput,Config.MAXVALUEMAPINPUT)
        if(self.Initialization or NumberHelper.NumberHasChanged(value,prevValue,Config.JOYSTICKRESOLUTION)):
            mapTo = NumberHelper.Translate(value,minInput,maxInput,Config.MINVALUEMAPOUTPUT,Config.MAXVALUEMAPOUTPUT)
            self.HasChanged = True
            return mapTo
        return mapTo

    def _getValue2IfValue1None(self,value1,value2):
        if(value1==None):
            return value2
        return value1


if __name__ == '__main__':
    vm = JoystickValueManager()
    vm.UpdateValues(0,0)
    print("{} {}".format(vm.MappedThrottleValue,vm.MappedSteeringValue))
    vm.UpdateValues(-1,-1)
    if(vm.HasChanged):
        print("{} {}".format(vm.MappedThrottleValue,vm.MappedSteeringValue))






