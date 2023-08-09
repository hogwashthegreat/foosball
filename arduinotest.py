#run StandardFirmata if broken to reset firmware
import pyfirmata
import time


board = pyfirmata.Arduino("COM4")
steps = 200
rotations = 2
times = 2
print("hi")

dirPin = board.get_pin("d:9:o")
stepPin = board.get_pin("d:6:o")

def rotate(steps, direction):
    dirPin.write(direction)
    for a in range(steps):
        stepPin.write(1)
        stepPin.write(0)

    
import keyboard  # using module keyboard
while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('a'):  # if key 'q' is pressed 
            rotate(1,0)
              # finishing the loop
        elif keyboard.is_pressed("d"):
            rotate(1,1)
    except:
        break  # if user pressed a key other than the given key the loop will break

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



    

    
