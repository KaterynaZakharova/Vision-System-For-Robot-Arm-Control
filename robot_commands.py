"""Main robot commands: home, move"""

import time

from config.robot import (
    HOME_J6,
    HOME_J5,
    HOME_X,
    HOME_Y,
    HOME_Z,
    HOME_SPEED,
    MEAN_SPEED,
)
from helpers.communication import send_message_G1


def homing(
    j6: float = HOME_J6,
    j5: float = HOME_J5,
    x: float = HOME_X,
    y: float = HOME_Y,
    z: float = HOME_Z,
    speed: float = HOME_SPEED,
):
    """Homing the robot

    After the main process is done, homing to the initial position.

    Args:
        j6, j5, x, y, z (float, optional): home position
        speed (float, optional): selected speed (mm/min) for homing
    """
    print('HOMING...')
    send_message_G1(j6, j5, x, y, z, speed)
    time.sleep(3)  # wait for the robot to home
    print('HOMED')


def move_arm(
    new_J6: float,
    new_J5: float,
    new_x: float,
    new_y: float,
    new_z: float,
    J6: float,
    J5: float,
    X: float,
    Y: float,
    Z: float,
    speed=MEAN_SPEED,
) -> tuple[float, float, float, float, float]:
    """Move robot to designated coordinates

    Args:
        new_J6, new_J5 (float): degrees to add
        new_x, new_y, new_z (float): distance to add
        J6, J5 (float): current J6/J5 angle
        X, Y, Z (float): current XYZ position
        speed (float, optional): requested speed of the robot's movement.
        Defaults to `MEAN_SPEED`.

    Returns:
        tuple[float, float, float, float, float]: new angles and positions
    """
    J6 += new_J6
    J5 += new_J5
    X += new_x
    Y += new_y
    Z += new_z

    send_message_G1(J6, J5, X, Y, Z, speed)

    return J6, J5, X, Y, Z
