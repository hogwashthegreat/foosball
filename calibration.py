import cv2
import numpy as np
import time
import math
def mouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"coords {x, y}, colors Blue- {img[y, x, 0]} , Green- {img[y, x, 1]}, Red- {img[y, x, 2]} ")




def getPoints(width, height, centerx, centery, radius):
    pointsIn = []
    pointsOut = []
    for x in range(width):
        for y in range(height):
            dx = (x - centerx)
            dy = (y - centery)
            distance_squared = (dx**2) + (dy**2)
            if distance_squared <= radius**2:
                pointsIn.append((x,y))
            else:
                pointsOut.append((x,y))

    return pointsIn, pointsOut

def numPoints(mask, pointsIn, pointsOut, totalPoints, weight):
    numIn = 0
    numOut = 0
    for point in pointsIn:
        if mask[point[1]][point[0]] == 255:
            numIn += 1
    for point in pointsOut:
        if mask[point[1]][point[0]] == 255:
            numOut += 1
    #print(f"numIn: {numIn}, numOut: {numOut}")
    score = (((numIn*weight)-numOut)/(totalPoints*weight))
    score = (1-score)
    return score

def looper(start, stop, step):
    n = start 
    while n <= stop:
        yield n
        if n + step > stop and n != stop:
            n = stop
            yield n
            break
        else:
            n += step
        

''' #old images
img1 = cv2.imread("masktests/colormatch14.JPG")
img2 = cv2.imread("masktests/colormatch13.JPG")
img3 = cv2.imread("masktests/colormatch12.JPG")

img1 = cv2.imread("masktests/Screenshot 2023-08-26 085231.jpg")
img2 = cv2.imread("masktests/Screenshot 2023-08-26 085340.jpg")
img3 = cv2.imread("masktests/Screenshot 2023-08-26 085413.jpg")
'''

r = 38
y = 36
x = 812
img1 = cv2.imread("masktests/today1.jpg")
img2 = cv2.imread("masktests/today2.jpg")
img3 = cv2.imread("masktests/today3.jpg")
img4 = cv2.imread("masktests/today4.jpg")
img5 = cv2.imread("masktests/today5.jpg")
#crop_img = img[y:y+r, x:x+r]
#cv2.imshow("crop", crop_img)
#cv2.setMouseCallback("crop", mouse_callback)
#cv2.waitKey(0)

imgs = [img1, img2, img3, img4, img5]
for x in range(len(imgs)):
    imgs[x] = ~imgs[x]
#old coords:
# coords = [(1020, 246), (299, 524), (657, 342)]
#coords = [(882, 478, 28), (393, 318, 19), (168, 153, 21)]
coords = [(823+19, 690+19, 19), (498+19, 209+19, 19), (1108+19, 211+19, 19), (175+19, 577+19, 19), (812+19, 36+19, 19)]

values = []
points = []
hsvs = []
for z in range(len(imgs)):
    img = imgs[z]
    h, w, c = img.shape 
    pointsIn, pointsOut = getPoints(w, h, coords[z][0], coords[z][1], coords[z][2])
    points.append((pointsIn, pointsOut)) 
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsvs.append(hsv)
                 #centerx centery radius  


#weights: 200, 200, 1 for regular, 200, 3, 3 inverted
def fullMask(points):
    values = [(0,0,0), (179,255,255)]
    
    values = hsvMask(points, (0, 179), (0, 179), 88, values, 0, 10000000000000, 179, hsvs)
    print("s")
    values = hsvMask(points, (0, 255), (0, 255), 126, values, 1, 10000000000000, 255, hsvs)
    print("v")
    values = hsvMask(points, (0, 255), (0, 255), 126, values, 2, 10000000000000, 255, hsvs)
    
    return values


def hsvMask(points, vmin, vmax, step, values, hsvType, topScore, absMax, hsvs):
    totalPoints = 0
    for point in points:
        totalPoints += len(point[0]) 
    totalPoints /= len(point)   
    print(f"\nstep: {step}, vMin: {vmin}, vMax: {vmax}\n") 
    if step == 0:
        return values
    for a in looper(vmin[0], vmin[1], step):
        for b in looper(vmax[0], vmax[1], step):
            if b-a >= step and a >= 0 and b >= 0: 
                    print(a, b)
                    if hsvType == 0:
                        h1 = a
                        h2 = b
                        s1 = 0
                        s2 = 255
                        v1 = 0
                        v2 = 255
                        weight = 217
                        
                    elif hsvType == 1:
                        s1 = a
                        s2 = b
                        h1 = values[0][0]
                        h2 = values[1][0]
                        v1 = 0
                        v2 = 255
                        weight = 10
                    else:
                        v1 = a
                        v2 = b
                        h1 = values[0][0]
                        h2 = values[1][0]
                        s1 = values[0][1]
                        s2 = values[1][1]
                        weight = 100
                    lower = np.array([h1, s1, v1])
                    upper = np.array([h2, s2, v2])
                    score = 0
                    for i in range(len(hsvs)):
                        hsv = hsvs[i]
                        pointsIn = points[i][0]
                        pointsOut = points[i][1]
                        mask = cv2.inRange(hsv, lower, upper)
                        score += numPoints(mask, pointsIn, pointsOut, totalPoints, weight)
                    score = score/len(hsvs)
                    
                        
                    
                    
                    if score < topScore:
                        print(f'score: {score}')
                        topScore = score
                        values = [(h1, s1, v1),(h2, s2, v2)] 
                        hsv = hsvs[0]
                        mask = cv2.inRange(hsv, lower, upper)
                        cv2.imshow("mask", mask)
                        cv2.waitKey(1000)
                        cv2.destroyWindow("mask")
                        print(values)
                        
    step = math.floor(step/2)
    
    vMin = (values[0][hsvType]-step, values[0][hsvType]+step) 
    vMax = (values[1][hsvType]-step, values[1][hsvType]+step) 
    
    if vMin[0] < 0:
        vMin = (0, values[0][hsvType]+step)
        
    if vMin[1] > absMax:
        vMin = (values[0][hsvType]-step, absMax)
        
    if vMax[0] < 0:
        vMax = (0, values[1][hsvType]+step)
        
    if vMax[1] > absMax:
        vMax = (values[1][hsvType]-step, absMax)    

    return hsvMask(points, vMin, vMax, step, values, hsvType, topScore, absMax, hsvs)

t1 = time.time()
val = fullMask(points)
print(val)
print(f"{time.time()-t1} seconds")
lower = np.array(val[0])
upper = np.array(val[1])
for i in range(len(hsvs)):
    hsv = hsvs[i]
    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow(str(i)+"mask", mask)
    cv2.imshow(str(i)+"img", imgs[i])

def uninvert(lower, upper):
    lower = np.uint8([[lower]])
    upper = np.uint8([[upper]])

    lowerred = ~cv2.cvtColor(lower,cv2.COLOR_HSV2BGR)
    upperred = ~cv2.cvtColor(upper,cv2.COLOR_HSV2BGR)

    lowerred = cv2.cvtColor(lowerred,cv2.COLOR_BGR2HSV)
    upperred = cv2.cvtColor(upperred,cv2.COLOR_BGR2HSV)


    lower = lower[0][0]
    upper = upper[0][0]
    lowerred = lowerred[0][0]
    upperred = upperred[0][0]


    lower1 = np.array([lowerred[0], lower[1], lower[2]])
    if upperred[0] < lowerred[0]:
        upper1 = np.array([179, upper[1], upper[2]])
        lower2 = np.array([0, lower[1], lower[2]])
    else:
        upper1 = np.array([upperred[0], upper[1], upper[2]])
        lower2 = np.array([lowerred[0], lower[1], lower[2]])

    upper2 = np.array([upperred[0],upper[1],upper[2]])

    print("mask1")
    print(lower1)
    print(upper1)

    print("mask2")
    print(lower2)
    print(upper2)
    return lower1, upper1, lower2, upper2

cv2.waitKey(0)