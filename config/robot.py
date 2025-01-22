"""Basic robot's configuration"""

import serial

### Initialise connector from the host computer to the robot
# Windows
CONN = serial.Serial(
    'COM3',
    baudrate=115200,
    timeout=None,
    bytesize=8,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_NONE,
)

### Home position
HOME_J6 = 0  # (deg) initial position of Joint 6 - wrist (aw)
HOME_J5 = 0  # (deg) initial position of Joint 5 - elbow (b0)
HOME_X = 203  # (mm) initial position of X
HOME_Y = 163  # (mm) initial position of Y
HOME_Z = 30  # (mm) initial position of Z
HOME_SPEED = 1000  # (mm/min) slower speed for homing

### Main action
MEAN_SPEED = 2500  # (mm/min) not fast and not slow
