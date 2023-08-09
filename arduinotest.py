"""
from Arduino import Arduino
import time

board = Arduino()
board.pinMode(10,"OUTPUT")

while True:
    print("hi")
    board.digitalWrite(10,"LOW")
    time.sleep(1)
    board.digitalWrite(10,"HIGH")
    time.sleep(1)


#run StandardFirmata if broken to reset firmware
import pyfirmata
import time

if __name__ == "__main__":
    board = pyfirmata.Arduino("COM4")
    print("hi")
    while True:
        input("")
        t1 = time.time()
        board.digital[10].write(1)
        print(time.time()-t1)
        time.sleep(0.001)
        board.digital[10].write(0)
        

from Arduino import Arduino
import time

board = Arduino()
board.pinMode(10,"OUTPUT")

while True:
    print("hi")
    board.digitalWrite(10,"LOW")
    time.sleep(1)
    board.digitalWrite(10,"HIGH")
    time.sleep(1)

"""
#run StandardFirmata if broken to reset firmware
import pyfirmata
import time


board = pyfirmata.Arduino("COM5")
steps = 200
rotations = 4
times = 2
delayTime = .0000001*1
print("hi")

dirPin = board.get_pin("d:9:o")
stepPin = board.get_pin("d:6:o")
print("pins")
def rotate(steps):
    print("rotate")
    for a in range(steps):
        stepPin.write(1)
        #time.sleep(delayTime)
        stepPin.write(0)
        #time.sleep(delayTime)
    
while True:
    for x in range(times):
        for y in range(rotations):
            dirPin.write(0)
            rotate(steps)
        time.sleep(0.05)
        for z in range(rotations):
            dirPin.write(1)
            rotate(steps)
        print("done")    
    break
    

    
