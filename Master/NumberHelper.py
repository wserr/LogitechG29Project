import Config

def Translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

def NumberHasChanged(value,prevValue,resolution):
    return (abs(value-prevValue)>resolution)


if __name__ == '__main__':
    print(NumberHasChanged(1e-5,1,1))
    print(NumberHasChanged(0.003,0.004,0.02))
    print(NumberHasChanged(0.003,0.004,0.0005))
    print(Translate(0.5,0,1,0,10))