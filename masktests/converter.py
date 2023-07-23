import cv2
import sys
import numpy as np

def nothing(x):
    pass

# Load in image
imagenames = ['masktests/colormatch10.jpg']
images = []
for x in range(len(imagenames)):
    images.append(cv2.imread(imagenames[x]))
# Create a window
cv2.namedWindow('image')
cv2.resizeWindow('image', 500, 250)
# create trackbars for color change
cv2.createTrackbar('HMin','image',0,179,nothing) # Hue is from 0-179 for Opencv
cv2.createTrackbar('SMin','image',0,255,nothing)
cv2.createTrackbar('VMin','image',0,255,nothing)
cv2.createTrackbar('HMax','image',0,179,nothing)
cv2.createTrackbar('SMax','image',0,255,nothing)
cv2.createTrackbar('VMax','image',0,255,nothing)

# Set default value for MAX HSV trackbars.
cv2.setTrackbarPos('HMax', 'image', 7)
cv2.setTrackbarPos('SMax', 'image', 105)
cv2.setTrackbarPos('VMax', 'image', 255)

cv2.setTrackbarPos('SMin', 'image', 54)
cv2.setTrackbarPos('VMin', 'image', 246)

cv2.namedWindow('image1')
cv2.resizeWindow('image1', 500, 250)
# create trackbars for color change
cv2.createTrackbar('HMin1','image1',0,179,nothing) # Hue is from 0-179 for Opencv
cv2.createTrackbar('SMin1','image1',0,255,nothing)
cv2.createTrackbar('VMin1','image1',0,255,nothing)
cv2.createTrackbar('HMax1','image1',0,179,nothing)
cv2.createTrackbar('SMax1','image1',0,255,nothing)
cv2.createTrackbar('VMax1','image1',0,255,nothing)

# Set default value for MAX HSV trackbars.
cv2.setTrackbarPos('HMax1', 'image1', 179)
cv2.setTrackbarPos('SMax1', 'image1', 255)
cv2.setTrackbarPos('VMax1', 'image1', 255)

cv2.setTrackbarPos('HMin1', 'image1', 172)
cv2.setTrackbarPos('SMin1', 'image1', 79)


# Initialize to check if HSV min/max value changes
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

hMin1 = sMin1 = vMin1 = hMax1 = sMax1 = vMax1 = 0
phMin1 = psMin1 = pvMin1 = phMax1 = psMax1 = pvMax1 = 0
wait_time = 33

while(1):
    # get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin','image')
    sMin = cv2.getTrackbarPos('SMin','image')
    vMin = cv2.getTrackbarPos('VMin','image')

    hMax = cv2.getTrackbarPos('HMax','image')
    sMax = cv2.getTrackbarPos('SMax','image')
    vMax = cv2.getTrackbarPos('VMax','image')

    hMin1 = cv2.getTrackbarPos('HMin1','image1')
    sMin1 = cv2.getTrackbarPos('SMin1','image1')
    vMin1 = cv2.getTrackbarPos('VMin1','image1')

    hMax1 = cv2.getTrackbarPos('HMax1','image1')
    sMax1 = cv2.getTrackbarPos('SMax1','image1')
    vMax1 = cv2.getTrackbarPos('VMax1','image1')

    # Set minimum and max HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])
    
    lower1 = np.array([hMin1, sMin1, vMin1])
    upper1 = np.array([hMax1, sMax1, vMax1])
    
    
    # Create HSV Image and threshold into a range.
    outputs = []
    for i in images:
        hsv = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask = cv2.bitwise_or(mask, mask1)
        outputs.append(mask)

    #output = cv2.bitwise_and(image,image, mask= mask)

    # Print if there is a change in HSV value
    if( (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
        print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax
        
    if( (phMin1 != hMin1) | (psMin1 != sMin1) | (pvMin1 != vMin1) | (phMax1 != hMax1) | (psMax1 != sMax1) | (pvMax1 != vMax1) ):
        print("(hMin1 = %d , sMin1 = %d, vMin1 = %d), (hMax1 = %d , sMax1 = %d, vMax1 = %d)" % (hMin1 , sMin1 , vMin1, hMax1, sMax1 , vMax1))
        phMin1 = hMin1
        psMin1 = sMin1
        pvMin1 = vMin1
        phMax1 = hMax1
        psMax1 = sMax1
        pvMax1 = vMax1

    # Display output image
    scale_percent = 50 # percent of original size
    width = int(outputs[0].shape[1] * scale_percent / 100)
    height = int(outputs[0].shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    resized = []
    for o in outputs:
        resized.append(cv2.resize(o, dim, interpolation = cv2.INTER_AREA))
    for x in range(len(resized)):
        cv2.imshow(imagenames[x]+" mask",resized[x])
        cv2.imshow(imagenames[x],cv2.resize(images[x], dim, interpolation = cv2.INTER_AREA))

    # Wait longer to prevent freeze for videos.
    if cv2.waitKey(wait_time) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()