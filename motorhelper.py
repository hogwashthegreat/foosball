import pyfirmata

def setup():
    try:
        board = pyfirmata.Arduino("COM4")
    except:
        board = pyfirmata.Arduino("COM5")

    dirPin = [board.get_pin("d:9:o"), board.get_pin("d:10:o")] #dirpin 9,10
    stepPin = [board.get_pin("d:6:o"), board.get_pin("d:5:o")] #steppin 6,5
    return board, dirPin, stepPin

def rotate(steps, direction, motor, dirPin, stepPin):
    dirPin[motor].write(direction)
    for a in range(steps):
        stepPin[motor].write(1)
        stepPin[motor].write(0)

