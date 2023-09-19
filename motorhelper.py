import pyfirmata
import numpy as np
import cv2
import imutils


def setup():
    try:
        board = pyfirmata.Arduino("COM4")
    except:
        board = pyfirmata.Arduino("COM5")
    sticks = []
    sticks.append([[board.get_pin("d:8:o"), board.get_pin("d:8:0")], [board.get_pin("d:8:o"), board.get_pin("d:8:0")]])
    sticks.append([[board.get_pin("d:8:o"), board.get_pin("d:8:0")], [board.get_pin("d:8:o"), board.get_pin("d:8:0")]])
    lateralMotor = [board.get_pin("d:9:o"), board.get_pin("d:6:0")] #dir:9, step:6
    rotateMotor = [board.get_pin("d:10:o"), board.get_pin("d:5:o")] #dir"10, step:5
    stick = [lateralMotor, rotateMotor]
    sticks.append(stick)
    sticks.append([[board.get_pin("d:8:o"), board.get_pin("d:8:0")], [board.get_pin("d:8:o"), board.get_pin("d:8:0")]])
    return board, sticks

def rotate(steps, direction, motor, board):
    dirPin = motor[0]
    stepPin = motor[1]
    dirPin.write(direction)
    for a in range(steps):
        stepPin.write(1)
        stepPin.write(0)

def moveTo(start, end, stick, board):
    pixelToPulse = 100/43
    distance = abs(end-start) * pixelToPulse
    direction = 0
    if (end-start) > 0:
        direction = 1

    motor = stick[0]
    rotate(distance, direction, motor, board)
    return end
    
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
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.waitKey(0)
    #get players y
    # 
    #
    #990 1111
    #for i in range(len(sticks)):
    #    moveTo(playerY[i], 0, sticks[i])
    return players

getStickPos(cv2.imread("masktests\\today5.jpg"))