from vmbpy import *
import threading
import cv2
import helper
import numpy as np

class Handler:
    def __init__(self):
        self.shutdown_event = threading.Event()
        self.processed_frames = 0 #test var to check how many frames are being processed to calculate fps
        self.centers = np.zeros((3,2)) #array of tuples with array index 0 being most recent and tuple is (x,y)

    def __call__(self, cam: Camera, stream: Stream, frame: Frame):
        #waitkey for opencv stream
        ENTER_KEY_CODE = 13

        key = cv2.waitKey(1)
        if key == ENTER_KEY_CODE: #
           self.shutdown_event.set()
           return
        
        #frame processing
        if frame.get_status() == FrameStatus.Complete:
            display = frame.as_opencv_image() #convert vimba to opencv format
            
            #Get new ball center and update array
            center, mask = helper.getBallCenter(display)
            self.centers[2] = self.centers[1]
            self.centers[1] = self.centers[0]
            self.centers[0] = center
                        
            
            scale_percent = 50 # percent of original size
            width = int(display.shape[1] * scale_percent / 100)
            height = int(display.shape[0] * scale_percent / 100)
            dim = (width, height)
            display = cv2.resize(display, dim, interpolation = cv2.INTER_AREA) #resize original image
            mask  = cv2.resize(mask, dim, interpolation = cv2.INTER_AREA) #resize mask
            cv2.imshow("Camera", display) 
            cv2.imshow("Mask", mask)
            self.processed_frames += 1 #Frame has been processed
            if self.processed_frames >= 10000: #if 10k frames are processed end the program (for testing)
                self.shutdown_event.set()
                return
            

        cam.queue_frame(frame) #get next frame from buffer
        
    def getFrames(self): #return number of processed frames (for fps)
        return self.processed_frames