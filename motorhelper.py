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
    