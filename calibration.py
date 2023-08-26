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
    n =  start 
    while n <= stop:
        yield n
        if n + step > stop and n != stop:
            n = stop
            yield n
            break
        else:
            n += step
        


img1 = cv2.imread("masktests/colormatch14.JPG")
img2 = cv2.imread("masktests/colormatch13.JPG")
img3 = cv2.imread("masktests/colormatch12.JPG")

imgs = [img1, img2, img3]
for x in range(len(imgs)):
    imgs[x] = ~imgs[x]
coords = [(1020, 246), (299, 524), (657, 342)]

r = 36
y = 524
x = 299
#crop_img = img2[y:y+r, x:x+r]
#cv2.imshow("crop", crop_img)
#cv2.waitKey(0)
values = []
points = []
hsvs = []
for z in range(len(imgs)):
    img = imgs[z]
    h, w, c = img.shape 
    pointsIn, pointsOut = getPoints(w, h, coords[z][0], coords[z][1], 18)
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
                        weight = 200
                        
                    elif hsvType == 1:
                        s1 = a
                        s2 = b
                        h1 = values[0][0]
                        h2 = values[1][0]
                        v1 = 0
                        v2 = 255
                        weight = 3
                    else:
                        v1 = a
                        v2 = b
                        h1 = values[0][0]
                        h2 = values[1][0]
                        s1 = values[0][1]
                        s2 = values[1][1]
                        weight = 3
                    lower = np.array([h1, s1, v1])
                    upper = np.array([h2, s2, v2])
                    totalNumIn = 0
                    totalNumOut = 0
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
    cv2.imshow(str(i)+"img", img)
cv2.waitKey(0)