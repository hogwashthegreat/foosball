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
cv2.setTrackbarPos('HMax', 'image', 179)
cv2.setTrackbarPos('SMax', 'image', 255)
cv2.setTrackbarPos('VMax', 'image', 255)

# Initialize to check if HSV min/max value changes
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0


wait_time = 33

while(1):
    # get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin','image')
    sMin = cv2.getTrackbarPos('SMin','image')
    vMin = cv2.getTrackbarPos('VMin','image')

    hMax = cv2.getTrackbarPos('HMax','image')
    sMax = cv2.getTrackbarPos('SMax','image')
    vMax = cv2.getTrackbarPos('VMax','image')

    # Set minimum and max HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Create HSV Image and threshold into a range.
    outputs = []
    for i in images:
        hsv = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)
        outputs.append(cv2.inRange(hsv, lower, upper))

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
        cv2.imshow(imagenames[x],resized[x])

    # Wait longer to prevent freeze for videos.
    if cv2.waitKey(wait_time) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()