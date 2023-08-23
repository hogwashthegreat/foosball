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

def numPoints(mask, pointsIn, pointsOut):
    numIn = 0
    numOut = 0
    for point in pointsIn:
        if mask[point[1]][point[0]] == 255:
            numIn += 1
    for point in pointsOut:
        if mask[point[1]][point[0]] == 255:
            numOut += 1

    return numOut, numIn


img = cv2.imread("masktests/colormatch14.JPG")
                           
values = []


h, w, c = img.shape
pointsIn, pointsOut = getPoints(w, h, 1020, 246, 18)
def fullMask(pointsIn, pointsOut):
    values = [(0,0,0), (0,255,255)]
    values = hsvMask(pointsIn, pointsOut, (0, 180), (0, 180), 179, values, 0, 0, 100000000, 180)
    print("s")
    values = hsvMask(pointsIn, pointsOut, (0, 256), (0, 256), 255, values, 1, 0, 100000000, 256)
    print("v")
    values = hsvMask(pointsIn, pointsOut, (0, 256), (0, 256), 255, values, 2, 0, 100000000, 256)

def hsvMask(pointsIn, pointsOut, vmin, vmax, step, values, hsvType, pixelsIn, pixelsOut, absMax):
    pixelsIn = 0
    pixelsOut = 10000000000
    print(f"step: {step}, vMin: {vmin}, vMax: {vmax}") 
    if step == 0:
        return values
    for a in range(vmin[0], vmin[1], step):
        for b in range(vmax[0], vmax[1], step):
            if a < b and a >= 0 and b >= 0: 
                print(a, b)
                if hsvType == 0:
                    h1 = a
                    h2 = b
                    s1 = values[0][1]
                    s2 = values[1][1]
                    v1 = values[0][2]
                    v2 = values[1][2]
                    
                elif hsvType == 1:
                    s1 = a
                    s2 = b
                    h1 = values[0][0]
                    h2 = values[1][0]
                    v1 = values[0][2]
                    v2 = values[1][2]
                else:
                    v1 = a
                    v2 = b
                    h1 = values[0][0]
                    h2 = values[1][0]
                    s1 = values[0][1]
                    s2 = values[1][1]
                lower = np.array([h1, s1, v1])
                upper = np.array([h2, s2, v2])
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, lower, upper)
                numOut, numIn = numPoints(mask, pointsIn, pointsOut)

                if numOut < pixelsOut and numIn > pixelsIn:
                    pixelsOut = numOut
                    pixelsIn = numIn
                    values = [(h1, s1, v1),(h2, s2, v2)] 
                    print(values)
    vMin = (values[0][hsvType]-step, values[0][hsvType]+step) 
    vMax = (values[1][hsvType]-step, values[1][hsvType]+step) 
    
    if vMin[0] < 0:
        vMin = (0, values[0][hsvType]+step+1)
        
    if vMin[1] > absMax:
        vMin = (values[0][hsvType]-step, absMax)
        
    if vMax[0] < 0:
        vMax = (0, values[1][hsvType]+step+1)
        
    if vMax[1] > absMax:
        vMax = (values[1][hsvType]-step, absMax)
    if step > 1:
        step = math.floor(step/2)
    else:
        step = 0
    return values, hsvMask(pointsIn, pointsOut, vMin, vMax, step, values, hsvType, pixelsIn, pixelsOut)
    '''
    if values[0][hsvType] > vmin[0]:
        if values[1][hsvType] > vmax[0]:
            return hsvMask(pointsIn, pointsOut, (values[0][hsvType]-(round(step/2)),values[0][hsvType]+1), (values[1][hsvType]-(round(step/2)),values[1][hsvType]+1), round(step/2), values, hsvType, pixelsIn, pixelsOut)
        else:
            return hsvMask(pointsIn, pointsOut, (values[0][hsvType]-(round(step/2)),values[0][hsvType]+1), (values[1][hsvType],values[1][hsvType]+(round(step/2))+1), round(step/2), values, hsvType, pixelsIn, pixelsOut)
    else:
        if values[1][hsvType] > vmax[0]:
            return hsvMask(pointsIn, pointsOut, (values[0][hsvType]-(round(step/2)),values[0][hsvType]+(round(step/2))+1), (values[1][hsvType]-round(step/2),values[1][hsvType]+round(step/2)+1), round(step/2), values, hsvType, pixelsIn, pixelsOut)
        else:
            return hsvMask(pointsIn, pointsOut, (values[0][hsvType],values[0][hsvType]+(round(step/2))+1), (values[1][hsvType],values[1][hsvType]+(round(step/2))+1), round(step/2), values,hsvType, pixelsIn, pixelsOut)
    '''
t1 = time.time()
val = fullMask(pointsIn, pointsOut)
print(val)
print(f"{time.time()-t1} seconds")