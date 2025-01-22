"""Communication protocol with the robot arm (SEED S6H4D robot arm)"""

import struct

from config.robot import CONN


def format_message(value: float) -> list[int]:
    """Convert float to a hexadecimal string

    1.	Format float numbers into the IEEE 754 binary32 single-precision format.
    2.	Convert every byte to a lowercase hexadecimal string prefixed with “0x”.
    3.	Convert the hexadecimal representation to an integer with 16 bases

    Args:
        value (float): input float number

    Returns:
        list: list of hexadecimal
    """
    return [int(hex(i), 16) for i in struct.pack('f', value)]


def send_message_G1(
    j6: float,
    j5: float,
    x: float,
    y: float,
    z: float,
    speed: float,
):
    """Send G1 code instructions

    Args:
        j6, j5, x, y, z (float): new position
        speed (float): selected speed (mm/min)
    """
    # Pack instruction frame
    instruction = [0] * 48  # frame consists of 48 bytes
    instruction[0] = [238]  # frame head - G1 code equivalent
    instruction[1] = '1'.encode()
    instruction[2] = 1
    # every code takes 4 bytes
    instruction[3:7] = format_message(x)  # x
    instruction[7:11] = format_message(y)  # y
    instruction[11:15] = format_message(z)  # z
    instruction[15:19] = format_message(j5)  # J5
    instruction[23:27] = format_message(j6)  # J6
    instruction[43:47] = format_message(speed)  # speed
    instruction[47] = 239  # frame tail

    # convert instructions to bytes
    full_instr = bytes(instruction[0]) + instruction[1] + bytes(instruction[2:])
    CONN.write(full_instr)  # send instructions
