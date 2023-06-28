from vmbpy import *
import threading
import cv2
import opencvstuff

class Handler:
    def __init__(self):
        self.shutdown_event = threading.Event()
        self.processed_frames = 0

    def __call__(self, cam: Camera, stream: Stream, frame: Frame):
        ENTER_KEY_CODE = 13

        #key = cv2.waitKey(1)
        #if key == ENTER_KEY_CODE: #
        #   self.shutdown_event.set()
        #   return

        if frame.get_status() == FrameStatus.Complete:
            #print('{} acquired {}'.format(cam, frame), flush=True)
            display = frame.as_opencv_image()
            #display = display[:500, :500]
            center = opencvstuff.getBallCenter(display)
            msg = 'Stream from \'{}\'. Press <Enter> to stop stream.'
            #cv2.imshow(msg.format(cam.get_name()), display)
            self.processed_frames += 1
            if self.processed_frames >= 1000:
                self.shutdown_event.set()
                return
            

        cam.queue_frame(frame)
        
    def getFrames(self):
        return self.processed_frames
