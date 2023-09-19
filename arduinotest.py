#run StandardFirmata if broken to reset firmware
import pyfirmata
import time
import numpy as np

try:
    board = pyfirmata.Arduino("COM4")
except:
    board = pyfirmata.Arduino("COM5")
steps = 200
rotations = 2
times = 2
print("hi")

dirPin = [board.get_pin("d:9:o"), board.get_pin("d:10:o")]

stepPin = [board.get_pin("d:6:o"), board.get_pin("d:5:o")]


def rotate(steps, direction, motor):
    dirPin[motor].write(direction)
    for a in range(steps):
        stepPin[motor].write(1)
        stepPin[motor].write(0)


def reset(frame):
    lower = np.array([0,0,0])
    upper = np.array([255,255,10])

rotate(100,0,0)


import keyboard  # using module keyboardljljljlj
while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed("a"):  # if key 'q' is pressed 
            rotate(1,0,0)
              # finishing the loop
        elif keyboard.is_pressed("d"):
            rotate(1,1,0)
        elif keyboard.is_pressed("j"):  # if key 'q' is pressed 
            rotate(1,0,1)
              # finishing the loop
        elif keyboard.is_pressed("l"):
            rotate(1,1,1)
    except:
        break  # if user pressed a key other than the given key the loop will break

input("")




    

    
