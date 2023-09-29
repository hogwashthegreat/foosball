from vmbpy import *
import threading
import cv2
import helper
import numpy as np
from calibration import fullMask
import motorhelper

class FakeHandler:
    def __init__(self):
        self.shutdown_event = threading.Event()
        self.processed_frames = 0 #test var to check how many frames are being processed to calculate fps
        self.centers = np.zeros((3,2)) #array of tuples with array index 0 being most recent and tuple is (x,y)
        self.waitKey = 1
        self.calibrate = 0 #positive is calibrating and 0 is not
        self.coords = []
        self.frames = []
        self.needFrame = False
        self.lower1 = None
        self.upper1 = None
        self.lower2 = None

        self.stickPos = [0,0,0,0]
            
    def __call__(self, cam: Camera, stream: Stream, frame: Frame):
        #waitkey for opencv stream
        ENTER_KEY_CODE = 13

        key = cv2.waitKey(self.waitKey)
        if key == ENTER_KEY_CODE: #
           self.shutdown_event.set()
           return
        
        #frame processing
        if frame.get_status() == FrameStatus.Complete:
            display = frame.as_opencv_image() #convert vimba to opencv format
            self.stickPos, mask = motorhelper.getStickPos(display)
            cv2.imshow("frame", display)
            cv2.imshow("mask", mask)


        cam.queue_frame(frame) #get next frame from buffer
        
    def getFrames(self): #return number of processed frames (for fps)
        return self.processed_frames
    
    def getWaitKey(self):
        return self.waitKey