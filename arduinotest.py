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
rotations = 2
times = 2
delayTime = .0000001*1
print("hi")

dirPin = board.get_pin("d:9:o")
stepPin = board.get_pin("d:6:o")
def sleep(duration):
    start = time.perf_counter_ns()
    while True:
        elapsed = time.perf_counter_ns()-start
        remaining = duration-elapsed
        if remaining <= 0:
            break
        if remaining > 0.02:
            time.sleep(max(remaining/2, 0.0001))
        else:
            pass
def rotate(steps, direciton):
    dirPin.write(direciton)
    for a in range(steps):
        stepPin.write(1)

        stepPin.write(0)

    
"""
for x in range(times):
    for y in range(rotations):
        dirPin.write(1)
        rotate(50)
    time.sleep(0.05)
"""

input("")

rotate(400, 0)
rotate(200, 1) #200
rotate(322, 0) #522
rotate(144, 0) #666
rotate(555, 1) #111
rotate(700, 0) #811
rotate(10, 0) #821
rotate(32, 1) #789
rotate(776, 1) #13
rotate(100, 0) #113
rotate(660, 0) #773
rotate(222, 1) #551
rotate(551, 1) #0



    

    
