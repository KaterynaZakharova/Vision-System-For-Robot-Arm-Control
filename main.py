"""Run the system"""

import time
import threading
import queue

from config.camera import BOTTOM_CAMERA_ID, TOP_CAMERA_ID
from config.robot import CONN, HOME_J6, HOME_J5, HOME_X, HOME_Y, HOME_Z
from robot_commands import homing, move_arm
from vision_system import capture_frames


def manipulate_robot_arm(
    top_cam_queue: queue.Queue,
    btm_cam_queue: queue.Queue,
    top_cam_event: threading.Event,
    btm_cam_event: threading.Event,
    J6: float,
    J5: float,
    X: float,
    Y: float,
    Z: float,
):
    """Robot arm manipulations.

    Args:
        top_cam_queue (queue.Queue): results from top camera thread
        btm_cam_queue (queue.Queue): results from bottom camera thread
        top_cam_event (threading.Event): top camera's flag
        btm_cam_event (threading.Event): bottom camera's flag
        J6 (int): current J6 position
        J5 (int): current J5 position
        X (int):  current X position
        Y (int):  current Y position
        Z (int):  current Z position
    """
    # endless loop, until the condition applies
    while True:
        # wait for both events to be set
        top_cam_event.wait()
        btm_cam_event.wait()

        # get frames from both queues
        new_J6, new_x, new_y = top_cam_queue.get()
        new_J5, _, new_z = btm_cam_queue.get()

        # if queues return all None's, stop all the processes
        if (new_J6 is None and new_x is None and new_y is None) and (
            new_J5 is None and new_z is None
        ):
            time.sleep(10)  # wait 'till robot finishes the last movement
            homing()
            CONN.close()  # close connector
            print("PRINTER STOPPED")
            break

        J6, J5, X, Y, Z = move_arm(new_J6, new_J5, new_x, new_y, new_z, J6, J5, X, Y, Z)

        # clear the events for the next iteration
        top_cam_event.clear()
        btm_cam_event.clear()


if __name__ == '__main__':
    # initialise queue per camera. Each queue has 3 elements:
    # 2D movement vector and rotation
    top_cam_queue = queue.Queue(3)
    btm_cam_queue = queue.Queue(3)

    # initialise event flags per camera
    top_cam_event = threading.Event()
    btm_cam_event = threading.Event()

    # initialise thread for the top camera
    top_cam = threading.Thread(
        target=capture_frames,
        args=(
            TOP_CAMERA_ID,
            top_cam_queue,
            top_cam_event,
        ),
    )

    # initialise thread for the bottom camera
    btm_cam = threading.Thread(
        target=capture_frames,
        args=(
            BOTTOM_CAMERA_ID,
            btm_cam_queue,
            btm_cam_event,
        ),
    )
    # initialise thread for the robot
    robot = threading.Thread(
        target=manipulate_robot_arm,
        args=(
            top_cam_queue,
            btm_cam_queue,
            top_cam_event,
            btm_cam_event,
            HOME_J6,
            HOME_J5,
            HOME_X,
            HOME_Y,
            HOME_Z,
        ),
    )

    ### Start threads
    top_cam.start()
    btm_cam.start()
    robot.start()

    ### Finish threads
    top_cam.join()
    btm_cam.join()
    robot.join()
