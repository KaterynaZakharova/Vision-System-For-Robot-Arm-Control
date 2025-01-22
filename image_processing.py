"""Main image processing methods: finding shape, cropping ROI"""

import cv2
import numpy as np
from tensorflow import keras

from config.camera import FRAME_HEIGHT, FRAME_WIDTH
from config.model import (
    IMG_SIZE,
    BASE_THRESHOLD,
    MIN_THRESHOLD,
    THRESHOLD_STEP,
    ROI_BORDER,
)
from model.wound_segmentation import model


def segmentation(
    gray: np.ndarray,
    segment: keras.Model = model,
) -> np.ndarray:
    """Find a wound in the image and segment it

    Args:
        gray (np.ndarray): frame in grayscale
        segment (keras.Model, optional): segmentation model. Defaults to
        `model`.

    Returns:
        np.ndarray: segmentation mask.
    """
    image = cv2.resize(gray, IMG_SIZE)  # resize image to march model input
    image = image / 255  # normalize the image [0 ... 1]
    mask = np.array(segment(np.array([image])))[0]  # predict segmentation mask

    resized_mask = cv2.resize(
        mask, (FRAME_HEIGHT, FRAME_WIDTH)
    )  # return original dimensions
    threshold = BASE_THRESHOLD  # initial threshold

    # decrease the threshold until we find the mask or the threshold reaches 0.1
    while threshold > MIN_THRESHOLD:
        # pixel equals to 0 if it is lower than the threshold, 1 otherwise
        filtered_mask = np.where(resized_mask > threshold)

        if len(filtered_mask[0]) == 0:  # if no pixel has value
            threshold -= THRESHOLD_STEP  # decrease the threshold
        else:
            break  # otherwise return filtered_mask
    return filtered_mask


def crop_ROI(
    gray: np.ndarray,
    mask: np.ndarray,
    roi_prev: np.ndarray = None,
    gray_prev: np.ndarray = None,
    border: int = ROI_BORDER,
    initial_run_flag: bool = False,
):
    """Crop ROI based on the segmented mask

    Args:
        gray (np.ndarray): current frame in grayscale
        mask (np.ndarray): segmented wound mask
        roi_prev (np.ndarray, optional): previous ROI coordinates
        gray_prev (np.ndarray, optional): previous frame in grayscale
        border (int, optional): border around ROI (px). Defaults to
        `ROI_BORDER`.
        initial_run_flag (bool, optional): points if now is the first
        program run. Defaults to False.

    Returns:
        cropped current and previous frames in grayscale, new ROI
        coordinates
    """
    # find bounding box coordinates of the mask
    xmin, xmax, ymin, ymax = mask[0].min(), mask[0].max(), mask[1].min(), mask[1].max()

    # if it's an initial program run, set current values as previous ones
    if not roi_prev:
        initial_run_flag = True
        roi_prev = xmin, xmax, ymin, ymax

    xmin_previous, xmax_previous, ymin_previous, ymax_previous = roi_prev
    roi_prev = (
        xmin,
        xmax,
        ymin,
        ymax,
    )  # update previous coordinates with the new ROI

    # select min max values between current and previous masks
    min_x, max_x, min_y, max_y = (
        min(xmin_previous, xmin),
        max(xmax_previous, xmax),
        min(ymin_previous, ymin),
        max(ymax_previous, ymax),
    )

    # add border, but keep it inside of the image
    if border:
        min_x, max_x, min_y, max_y = (
            max(0, min_x - border),
            min(FRAME_WIDTH, max_x + border),
            max(0, min_y - border),
            min(FRAME_HEIGHT, max_y + border),
        )

    # crop ROI on a current frame
    cropped_gr = gray.copy()[
        min_x:max_x,
        min_y:max_y,
    ]

    # crop ROI on a previous frame
    if initial_run_flag:
        gray_prev = cropped_gr.copy()
    else:
        gray_prev = gray_prev.copy()[
            min_x:max_x,
            min_y:max_y,
        ]
    # apply Bilateral filter on both ROIs
    return (
        cv2.bilateralFilter(cropped_gr, 10, 75, 750),
        cv2.bilateralFilter(gray_prev, 10, 75, 750),
        roi_prev,
    )


def convert_to_world_values(x: int, y: int, scale_factor: float) -> tuple[float, float]:
    """Apply scale factor to the displacements to convert px to mm

    Args:
        x (int): X value in pixels
        y (int): Y value in pixels
        scale_factor (float): (px/mm) scaling. Should be dynamic,
        if Z changes occur

    Returns:
        tuple[float, float]: world coordinates for X and Y in mm
    """
    return x * scale_factor, y * scale_factor
