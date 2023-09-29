import cv2
import numpy as np
import imutils
import motorhelper
#stick x locations of camera pixels
stickX = {0:410, 1:740, 2:1070, 3:1230, 4:-1}
tableY = 760 #table height
#magic squre for player max/min
table = [[[45, 309], [260, 521], [472, 736]], 
         [[45, 177], [183, 315], [323, 453], [462, 592], [605, 735]], 
         [[50, 445], [330, 740]], 
         [[240, 530]]]

def getBallCenter(frame, lower1, lower2, upper1, upper2):
    radius = 0
    #convert color format to hsv for masking
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #lower range of red mask
    lower_red = lower1
    upper_red = upper1
    #upper range of red mask
    lower_red2 = lower2
    upper_red2 = upper2

    lower_red = np.array([134,62,127])
    upper_red = np.array([179,178,204])

    lower_red2 = np.array([0,62,127])
    upper_red2 = np.array([1,178,204])


    #get low and high mask then combine with bitwise OR
    mask = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask, mask2)

    #find contours using color mask
    kernel = np.ones((4,4),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

	# only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
        """
        if radius > 6:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pass
        """

    return center, radius, mask

#get x,y velocity of ball based on average of the first and 3rd positions
def getVelo(centers):
    x = (centers[0][0]-centers[2][0])/2
    y = (centers[0][1]-centers[2][1])/2
    return (x,y)


#find which stick is going to be hit based on stickX
def whichStick(centers):
    velo = getVelo(centers)
    nextX = centers[0][0]
    if velo[0] != 0:
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
    else:
            return 4, velo
#find yPos of predicted contact with stick
def yHit(centers):
    stick, velo = whichStick(centers) #retrieve next stick to get hit and ball velocity
    if stick != 4 or velo[0] != 0:
        x = stickX[stick] #get the x location of the collision
        frames = (x-centers[0][0])/velo[0] #how many frames until collision
        yPos = frames*velo[1]+centers[0][1] #total y position
        #bounce logic using flipped table
        numTables = yPos//tableY
        remainder = yPos % tableY
        if numTables % 2:
            yPos = tableY-remainder
        else:
            yPos = remainder
        return int(yPos), stick #return predicted yposition of collision and stick collided with
    else:
        return -1, -1
#find player to hit with based on predicted yPos
def whichPlayer(centers, board, sticks, stickPos):
    yPos, stickNum = yHit(centers)
    if yPos == -1 or stickNum == -1:
        return 0, stickPos[0]
    stick = sticks[stickNum]
    stickPos = stickPos[stickNum]
    if stickNum == 0: #3-man
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
        
        
    elif stickNum == 1: #5-man
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
        
                                                                                    
        
    elif stickNum == 2: #2-man, 18 and 304 magic numbers, position of each player at motor 0
        if yPos < table[2][0][0]:
            #player 1 at motor min
            return stickNum, motorhelper.moveTo(stickPos, 0, stick, board)

        elif yPos < table[2][1][0]:
            #player 1
            return stickNum, motorhelper.moveTo(stickPos, yPos-18, stick, board)
        elif yPos < table[2][0][1]:
            #overlap stuff
            if abs(yPos-(stickPos+18)) > abs(yPos-(stickPos+304)):
                return stickNum, motorhelper.moveTo(stickPos, yPos-304, stick, board)
            else:
                return stickNum, motorhelper.moveTo(stickPos, yPos-18, stick, board)
        elif yPos < table[2][1][1]:
            #player 2
            return stickNum, motorhelper.moveTo(stickPos, yPos-304, stick, board)

        else:
            #player 2 at motor max
            return stickNum, motorhelper.moveTo(stickPos, table[2][1][1]-304, stick, board)

        
        
    elif stickNum == 3: #goalie
        if yPos > table[3][0][0] and yPos < table[3][0][0]:
            #in-range
            pass
        else:
            #out of range
            pass
        
        
    elif stickNum == 4: #if past our goalie stick
        pass

    return stickNum, stickPos