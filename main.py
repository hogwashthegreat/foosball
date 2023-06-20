import sys
from typing import Optional  
import time
from vmbpy import *

from Handler import Handler

# All frames will either be recorded in this format, or transformed to it before being displayed
opencv_display_format = PixelFormat.Bgr8

def print_usage():
    print('Usage:')
    print('    python asynchronous_grab_opencv.py [camera_id]')
    print('    python asynchronous_grab_opencv.py [/h] [-h]')
    print()
    print('Parameters:')
    print('    camera_id   ID of the camera to use (using first camera if not specified)')
    print()


def abort(reason: str, return_code: int = 1, usage: bool = False):
    print(reason + '\n')

    if usage:
        print_usage()

    sys.exit(return_code)


def parse_args() -> Optional[str]:
    args = sys.argv[1:]
    argc = len(args)

    for arg in args:
        if arg in ('/h', '-h'):
            print_usage()
            sys.exit(0)

    if argc > 1:
        abort(reason="Invalid number of arguments. Abort.", return_code=2, usage=True)

    return None if argc == 0 else args[0]


def get_camera(camera_id: Optional[str]) -> Camera:
    with VmbSystem.get_instance() as vmb:
        if camera_id:
            try:
                return vmb.get_camera_by_id(camera_id)

            except VmbCameraError:
                abort('Failed to access Camera \'{}\'. Abort.'.format(camera_id))

        else:
            cams = vmb.get_all_cameras()
            if not cams:
                abort('No Cameras accessible. Abort.')

            return cams[0]


#setup camera with settings from camerasettings.xml and set pixel format to Bgr8
def setup_camera(cam: Camera):
    with cam:
        # Enable auto exposure time setting if camera supports it
        try:
            cam.load_settings("testcamerasettings.xml", PersistType.All)
            cam.set_pixel_format(PixelFormat.Bgr8)
        except (AttributeError, VmbFeatureError):
            pass


"""
class Handler:
    def __init__(self):
        self.shutdown_event = threading.Event()

    def __call__(self, cam: Camera, stream: Stream, frame: Frame):
        ENTER_KEY_CODE = 13

        key = cv2.waitKey(1)
        if key == ENTER_KEY_CODE:
            self.shutdown_event.set()
            return

        elif frame.get_status() == FrameStatus.Complete:
            print('{} acquired {}'.format(cam, frame), flush=True)
            display = frame

            msg = 'Stream from \'{}\'. Press <Enter> to stop stream.'
            cv2.imshow(msg.format(cam.get_name()), display.as_opencv_image())

        cam.queue_frame(frame)
"""


def main():
    cam_id = parse_args()

    with VmbSystem.get_instance():
        with get_camera(cam_id) as cam:
            # setup general camera settings and the pixel format in which frames are recorded
            setup_camera(cam)
            handler = Handler()

            try:
                # Start Streaming with a custom a buffer of 3 Frames (defaults to 5)
                time_ = time.time()
                cam.start_streaming(handler=handler, buffer_count=5
                                    )
                handler.shutdown_event.wait()

            finally:
                print(f"time: {time.time()-time_}")
                print(f"frames processed: {handler.getFrames()}")
                cam.stop_streaming()


if __name__ == '__main__':
    main()
