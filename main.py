import sys
from typing import Optional  
import time
from vmbpy import *
from Handler import Handler

# All frames will either be recorded in this format, or transformed to it before being displayed
opencv_display_format = PixelFormat.Bgr8


#abort and exit if error
def abort(reason: str, return_code: int = 1, usage: bool = False):
    print(reason + '\n')
    sys.exit(return_code)

#parse arguments
def parse_args() -> Optional[str]:
    args = sys.argv[1:]
    argc = len(args)

    for arg in args:
        if arg in ('/h', '-h'):
            sys.exit(0)

    if argc > 1:
        abort(reason="Invalid number of arguments. Abort.", return_code=2, usage=True)

    return None if argc == 0 else args[0]

#find camera on startup
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
        try:
            cam.load_settings("camerasettings.xml", PersistType.All)
            cam.set_pixel_format(PixelFormat.Bgr8)
        except (AttributeError, VmbFeatureError):
            pass



def main():
    cam_id = parse_args()

    with VmbSystem.get_instance():
        with get_camera(cam_id) as cam:
            # setup general camera settings and the pixel format in which frames are recorded
            setup_camera(cam)
            #get handler class to start streaming
            handler = Handler()
            waitKey = handler.getWaitKey()
            if waitKey:
                buffer = 5
            else:
                buffer = 1000
                 
            try:
                # Start Streaming with a buffer of 5 frames (5 is default)
                time_ = time.time()
                cam.start_streaming(handler=handler, buffer_count=buffer)
                handler.shutdown_event.wait()

            finally: #after program is ended, print total frames processed and time taken (for fps if needed)
                print(f"time: {time.time()-time_}")
                print(f"frames processed: {handler.getFrames()}")
                cam.stop_streaming()


if __name__ == '__main__':
    main()
