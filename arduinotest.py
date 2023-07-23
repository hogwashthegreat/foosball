"""
from Arduino import Arduino
import time

board = Arduino(port="COM3")
board.pinMode(6,"OUTPUT")

while True:
    print("hi")
    board.digitalWrite(6,"LOW")
    time.sleep(1)
    board.digitalWrite(6,"HIGH")
    time.sleep(1)
"""

import pyfirmata
import time

if __name__ == "__main__":
    board = pyfirmata.Arduino("COM4")
    print("hi")
    while True:
        board.digital[10].write(1)
        time.sleep(0.1)
        board.digital[10].write(0)
        time.sleep(0.1)