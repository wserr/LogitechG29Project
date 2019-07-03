import smbus
import time

bus = smbus.SMBus(1)
address = 0x08

def writeNumber(a,b,c,d):
    bus.write_i2c_block_data(address, a, [b, c, d])
    return -1


while True:
    try:   
        writeNumber(512,180,60,10)
        time.sleep(1)                    #delay one second

    except KeyboardInterrupt:
        quit()