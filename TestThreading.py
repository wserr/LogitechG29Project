# Program to demonstrate 
# timer objects in python 
  
import threading 
import sys


def RepeatYoSelf():
    timer = threading.Timer(2.0, RepeatYoSelf)
    timer.daemon = True
    timer.start()
    print("Repeat!")

Timer = None

RepeatYoSelf()

try:
    while True:
        print("test")
except:
    print("error")
finally:
    sys.exit()


