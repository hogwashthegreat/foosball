#run StandardFirmata if broken to reset firmware
import pyfirmata
import time
import numpy as np
import cv2
import imutils
import motorhelper

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

rotate(100,1,0)

def getStickPos(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,0,0])
    upper_red = np.array([179,255,50])
    mask = cv2.inRange(hsv, lower_red, upper_red) #black player mask

    kernel = np.ones((4,4),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts) #find circles

	# only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
        players = [2000,2000,2000,2000]
        playerX = [[325,475],[675,800],[990,1111],[1150,1300]]
        for c in cnts:
        #c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            if (radius > 30): #if big enough to be a player
                if (x > playerX[0][0]) and (x < playerX[0][1]): #2 man, x range
                    if y < players[0]:
                        players[0] = y
                elif (x > playerX[1][0]) and (x < playerX[1][1]): #2 man, x range
                    if y < players[1]:
                        players[1] = y
                elif (x > playerX[2][0]) and (x < playerX[2][1]): #2 man, x range
                    if y < players[2]:
                        players[2] = y
                elif (x > playerX[3][0]) and (x < playerX[3][1]): #2 man, x range
                    if y < players[3]:
                        players[3] = y

    print(players)
    for i in range(len(players)):
        cv2.circle(frame, (int((playerX[i][1]+playerX[i][0])/2), int(players[i])), int(20), (0, 255, 255), 2)
    #cv2.imshow("frame", frame)
    #cv2.imshow("mask", mask)
    #cv2.waitKey(0)
    #get players y
    # 
    #
    #990 1111
    #for i in range(len(sticks)):
    #    moveTo(playerY[i], 0, sticks[i])
    return players


import keyboard  # using module keyboardljljljlj
while True:  # making a loop
    pos = getStickPos()
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




    

    
