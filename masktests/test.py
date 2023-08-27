import numpy as np
import cv2
import time
image = cv2.imread("masktests/colormatch14.JPG")
print(image[0][0])
cv2.imshow("a", image)
cv2.waitKey(1000)
image = ~image
cv2.imshow("a", image)
cv2.waitKey(0)
print(image[0][0])
image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
#image = ~image
"""
for i in range(len(image)):
    for j in range(len(image[i])):
        image[i][j][0]
"""
#print(image[0][0])
#cv2.imshow("test",image)


lower = np.uint8([[[43,88,109]]])
upper = np.uint8([[[92,255,255]]])



lowerred = ~cv2.cvtColor(lower,cv2.COLOR_HSV2BGR)
upperred = ~cv2.cvtColor(upper,cv2.COLOR_HSV2BGR)

lowerred = cv2.cvtColor(lowerred,cv2.COLOR_BGR2HSV)
upperred = cv2.cvtColor(upperred,cv2.COLOR_BGR2HSV)

print(type(lower))
print(type(upper))

print("mask1")
print(lowerred[0][0][0],lower[0][0][1],lower[0][0][2])
print(f"179, {upper[0][0][1]}, {upper[0][0][2]}")

print("mask2")
print(f"0, {lower[0][0][1]}, {lower[0][0][2]}")
print(upperred[0][0][0],upper[0][0][1],upper[0][0][2])
#cv2.imshow("lower",lower)
#print(lower)
#print(~lower)
#print(~upper)

