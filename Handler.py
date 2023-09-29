from vmbpy import *
import threading
import cv2
import helper
import numpy as np
from calibration import fullMask
import motorhelper

class Handler:
    def __init__(self):
        self.shutdown_event = threading.Event()
        self.processed_frames = 0 #test var to check how many frames are being processed to calculate fps
        self.centers = np.zeros((3,2)) #array of tuples with array index 0 being most recent and tuple is (x,y)
        self.waitKey = 1
        self.calibrate = 4 #positive is calibrating and 0 is not
        self.coords = []
        self.frames = []
        self.needFrame = False
        self.lower1 = None
        self.upper1 = None
        self.lower2 = None
        self.upper2 = None
        self.board, self.sticks = motorhelper.setup()
        self.stickPos = []
    def mouse_callback(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.needFrame = True
            self.stickPos.append(y)
            self.calibrate -= 1
            if self.calibrate == 0:
                cv2.destroyWindow("calibrate")
            print(f"coords {x, y}")
            
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
            if self.needFrame:
                    self.frames.append(display.copy())
                    self.needFrame = False
                    
            if self.calibrate == 0 and self.needFrame == False:
                self.calibrate -= 1
                print(len(self.frames))
                print(self.coords)
                #self.lower1, self.upper1, self.lower2, self.upper2 = fullMask(self.coords, self.frames)
                
            if self.calibrate > 0:
                cv2.imshow("calibrate", display)
                cv2.setMouseCallback("calibrate", self.mouse_callback)
            
            else:    
                #Get new ball center and update array
                
                center, radius, mask = helper.getBallCenter(display, self.lower1, self.lower2, self.upper1, self.upper2)
                """
                if (abs(center[0] - self.centers[0][0]) > 200) or (abs(center[1] - self.centers[0][1]) > 200):
                    print("distance too big")
                    velo = helper.getVelo(self.centers)
                    #center = (self.centers[0][0] + velo[0],self.centers[0][1] + velo[1])
                    center = self.centers[0]
                elif radius < 6:
                    print("radius too small")
                    velo = helper.getVelo(self.centers)
                    #center = (self.centers[0][0] + velo[0],self.centers[0][1] + velo[1])
                """
                if center != None:
                    self.centers[2] = self.centers[1]
                    self.centers[1] = self.centers[0]
                    self.centers[0] = center
                num, yPos = helper.whichPlayer(self.centers, self.board, self.sticks, self.stickPos)
                self.stickPos[num] = yPos
                try:
                    cv2.circle(display, (int(self.centers[0][0]), int(self.centers[0][1])), int(radius),
                        (0, 255, 255), 2)
                    cv2.circle(display, (int(self.centers[0][0]), int(self.centers[0][1])), 5, (0, 0, 255), -1)
                except:
                    pass
                
                            
                
                scale_percent = 50 # percent of original size
                width = int(display.shape[1] * scale_percent / 100)
                height = int(display.shape[0] * scale_percent / 100)
                dim = (width, height)
                display = cv2.resize(display, dim, interpolation = cv2.INTER_AREA) #resize original image
                mask  = cv2.resize(mask, dim, interpolation = cv2.INTER_AREA) #resize mask

                self.processed_frames += 1 #Frame has been processed
                #print(self.centers)
                if self.processed_frames >= 10000: #if 10k frames are processed end the program (for testing)
                    self.shutdown_event.set()
                    return


        cam.queue_frame(frame) #get next frame from buffer
        
    def getFrames(self): #return number of processed frames (for fps)
        return self.processed_frames
    
    def getWaitKey(self):
        return self.waitKey