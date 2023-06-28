import cv2
import time
import numpy as np
from collections import deque
from imutils.video import VideoStream
import argparse
import imutils


def getBallCenter(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 96, 172])
    upper_red = np.array([4, 124, 255])
    
    mask = cv2.inRange(hsv, lower_red, upper_red)


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
        if radius > 1:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    
    #cv2.imshow("vimba",frame)
    return center

#get x,y velocity of ball based on average of the 2 steps
def getVelo(centers):
    x = (centers[0][0]-centers[2][0])//2
    y = (centers[0][1]-centers[2][1])//2
    return (x,y)

def getNextPos(centers):
    velo = getVelo(centers)
    x = centers[0][0] + velo[0]
    y = centers[0][1] + velo[1]
    return (int(x),int(y))