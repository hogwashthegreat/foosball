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

"""
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