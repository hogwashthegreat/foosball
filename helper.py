import cv2
import time
import numpy as np
from collections import deque
from imutils.video import VideoStream
import argparse
import imutils

stickX = {0:410, 1:740, 2:1070, 3:1230, 4:-1}
tableY = 760
#magic squre for player max/min
table = [[[45, 309], [260, 521], [472, 736]], 
         [[45, 177], [183, 315], [323, 453], [462, 592], [605, 735]], 
         [[50, 445], [330, 740]], 
         [[240, 530]]]

def getBallCenter(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #lower_red = np.array([0, 96, 172])
    #upper_red = np.array([4, 124, 255])

    lower_red = np.array([0, 54, 246])
    upper_red = np.array([7, 105, 255])
    
    lower_red2 = np.array([172, 78, 0])
    upper_red2 = np.array([179, 255, 255])
    

    
    mask = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    
    mask = cv2.bitwise_or(mask, mask2)


    kernel = np.ones((4,4),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

	# only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
        if radius > 6:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pass

    
    #cv2.imshow("vimba",frame)
    return center, mask

#get x,y velocity of ball based on average of the 2 steps
def getVelo(centers):
    x = (centers[0][0]-centers[2][0])/2
    y = (centers[0][1]-centers[2][1])/2
    return (x,y)
'''
def getNextPos(centers):
    velo = getVelo(centers)
    x = centers[0][0] + velo[0]
    y = centers[0][1] + velo[1]
    return (int(x),int(y)), velo
'''

#goalie: 1230, 2-man: 1070, 5-man: 740, 3-man: 410
def whichStick(centers):
    velo = getVelo(centers)
    nextX = centers[0][0]
    if velo[0] > 0:
        if nextX < stickX[0]:
            return 0, velo
        elif nextX < stickX[1]:
            return 1, velo
        elif nextX < stickX[2]:
            return 2, velo
        elif nextX < stickX[3]:
            return 3, velo
        else: #When ball is past goalie
            return 4, velo
        
#find yPos of predicted contact with stick
def yHit(centers):
    stick, velo = whichStick(centers)
    x = stickX[stick]
    frames = (x-centers[0][0])/velo[0]
    yPos = frames*velo[1]+centers[0][1]
    numTables = yPos//tableY
    remainder = yPos % tableY
    if numTables % 2:
        yPos = tableY-remainder
    else:
        yPos = remainder
    return int(yPos), stick

#find player to hit with based on predicted yPos
def whichPlayer(centers):
    yPos, stick = yHit(centers)
    
    if stick == 0: #3-man
        if yPos < table[0][0][0]:
            #player 1 at motor min
            pass
        if yPos < table[0][1][0]:
            #player 1
            pass
        elif yPos < table[0][0][1]:
            #overlap stuff
            pass
        elif yPos < table[0][2][0]:
            #player 2
            pass
        elif yPos < table[0][1][1]:
            #overlap stuff
            pass
        elif yPos < table[0][2][1]:
            #player 3
            pass
        else:
            #player 3 at motor max
            pass
        
        
    elif stick == 1: #5-man
        if yPos < 180:
            #player 1
            pass
        elif yPos < 319:
            #player 2
            pass
        elif yPos < 458:
            #player 3
            pass
        elif yPos < 598:
            #player 4
            pass
        else:
            #player 5
            pass
        
                                                                                    
        
    elif stick == 2: #2-man
        if yPos < table[2][0][0]:
            #player 1 at motor min
            pass
        elif yPos < table[2][1][0]:
            #player 1
            pass
        elif yPos < table[2][0][1]:
            #overlap stuff
            pass
        elif yPos < table[2][1][1]:
            #player 2
            pass
        else:
            #player 2 at motor max
            pass
        
        
    elif stick == 3: #goalie
        if yPos > table[3][0][0] and yPos < table[3][0][0]:
            #in-range
            pass
        else:
            #out of range
            pass
        
        
    elif stick == 4: #shit stick
        pass
    