import motorhelper
import keyboard
#board, sticks = motorhelper.setup()


import hid

#for device in hid.enumerate():
 #   print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")

gamepad = hid.device()
gamepad.open(0x045e, 0x0b13)
gamepad.set_nonblocking(True)
while True:
    report = gamepad.read(64)
    if report:
        print(report)

while True:        
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed("w"):  # if key 'q' is pressed 
            motorhelper.rotate(1, 1, sticks[2][0], board)
              # finishing the loop
        elif keyboard.is_pressed("s"):
            motorhelper.rotate(1, 0, sticks[2][0], board)
        elif keyboard.is_pressed("a"):  # if key 'q' is pressed 
            motorhelper.rotate(1, 1, sticks[2][1], board)
              # finishing the loop
        elif keyboard.is_pressed("d"):
            motorhelper.rotate(1, 0, sticks[2][1], board)
    except:
        break  # if user pressed a key other than the given key the loop will break
  
