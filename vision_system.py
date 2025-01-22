"""Processing of the every camera's frame together in sync"""

import queue
import threading
import traceback

import cv2

from config.camera import FRAME_HEIGHT, FRAME_WIDTH, SCALE
from image_processing import convert_to_world_values, crop_ROI, segmentation
from tracking import rotation, track


def capture_frames(
    camera_id: int,
    movements: queue.Queue,
    event: threading.Event,
):
    """Capture and process frame from the camera in a separate thread

    Args:
        camera_id (int): current camera (top/side/bottom)
        movements (queue.Queue): placeholder for displacement values
        event (threading.Event): flagger to other threads
    """
    # initialise variables
    roi_prev = None
    kpnts, desc, dest_pnts = None, None, None
    # read every 30th frame
    frame_to_skip = 30
    current_frame_index = -1

    # open camera
    camera = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    # read first frame and convert it to grayscale
    _, roi_prev = camera.read()
    gray_prev = cv2.cvtColor(roi_prev, cv2.COLOR_BGR2GRAY)

    while True:
        retrieve, frame = camera.read()

        # if camera is closed, stop reading frames and send commands to the
        # robot to home
        if not retrieve:
            print("STOPPING...")
            movements.put((None, None, None))  # send None types instead of real values
            event.set()  # set flag that the current thread finished iteration
            camera.release()  # stop camera processing
            print('STOPPED')
            break

        # skip frames, do not process skipped
        current_frame_index += 1
        if current_frame_index % frame_to_skip != 0:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to gray

        # process frame
        try:
            mask = segmentation(gray)

            roi_cur, gray_prev, roi_prev = crop_ROI(gray, mask, roi_prev, gray_prev)

            src_pnts, x, y, kpnts, desc, dest_pnts = track(
                roi_cur,
                roi_prev,
                kpnts,
                desc,
                dest_pnts,
            )
            joint_rotation = rotation(src_pnts, dest_pnts)
            x, y = convert_to_world_values(x, y, SCALE)

            # put the frame in the queue with the movements values
            movements.put((joint_rotation, x, y))

            # set the event to signal that a frame has been processed
            event.set()

            # reassign current frame as a previous one
            gray_prev = gray
        except Exception as e:
            # if there any runtime error in the code, log the error
            print(f"ERROR : {e}  {traceback.format_exc()}")
