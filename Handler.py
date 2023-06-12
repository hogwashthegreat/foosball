from vmbpy import *
import threading
import cv2


class Handler:
    def __init__(self):
        self.shutdown_event = threading.Event()

    def __call__(self, cam: Camera, stream: Stream, frame: Frame):
        ENTER_KEY_CODE = 13

        key = cv2.waitKey(1)
        if key == ENTER_KEY_CODE: #
            self.shutdown_event.set()
            return

        elif frame.get_status() == FrameStatus.Complete:
            print('{} acquired {}'.format(cam, frame), flush=True)
            display = frame

            msg = 'Stream from \'{}\'. Press <Enter> to stop stream.'
            cv2.imshow(msg.format(cam.get_name()), display.as_opencv_image())

        cam.queue_frame(frame)