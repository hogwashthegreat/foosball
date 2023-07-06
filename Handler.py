from vmbpy import *
import threading
import cv2
import helper
import numpy as np

class Handler:
    def __init__(self):
        self.shutdown_event = threading.Event()
        self.processed_frames = 0
        self.centers = np.zeros((3,2))
    def __call__(self, cam: Camera, stream: Stream, frame: Frame):
        ENTER_KEY_CODE = 13

        key = cv2.waitKey(1)
        if key == ENTER_KEY_CODE: #
           self.shutdown_event.set()
           return

        if frame.get_status() == FrameStatus.Complete:
            #print('{} acquired {}'.format(cam, frame), flush=True)
            display = frame.as_opencv_image()
            #display = display[:500, :500]
            
            #Get new ball center and update array
            center = helper.getBallCenter(display)
            self.centers[2] = self.centers[1]
            self.centers[1] = self.centers[0]
            self.centers[0] = center
            #print(self.centers)
            
            #get predicted next position and draw it (if centers found)
            try:
                nextPos = helper.getNextPos(self.centers)
                cv2.circle(display, nextPos, 4 ,(0,255,0), -1)
                print(self.centers,nextPos)
                #print(nextPos)
            except:
                pass

            #Only gets and displays first 1000 frames
            msg = 'Stream from \'{}\'. Press <Enter> to stop stream.'            
            cv2.imshow(msg.format(cam.get_name()), display)
            self.processed_frames += 1
            if self.processed_frames >= 10000:
                self.shutdown_event.set()
                return
            

        cam.queue_frame(frame)
        
    def getFrames(self):
        return self.processed_frames
