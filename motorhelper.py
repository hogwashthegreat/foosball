import pyfirmata

def setup():
    try:
        board = pyfirmata.Arduino("COM4")
    except:
        board = pyfirmata.Arduino("COM5")
    lateralMotor = [board.get_pin("d:9:o"), board.get_pin("d:6:0")] #dir:9, step:6
    rotateMotor = [board.get_pin("d:10:o"), board.get_pin("d:5:o")] #dir"10, step:5
    stick = [lateralMotor, rotateMotor]

    return board, stick

def move(steps, direction, motor):
    dirPin = motor[0][0]
    stepPin = motor[0][1]
    dirPin.write(direction)
    for a in range(steps):
        stepPin.write(1)
        stepPin.write(0)

