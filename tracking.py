"""Tracking of the surface"""

import cv2
import numpy as np

from config.tracker import APPROX_FUNC, FLANN, FLANN_THRESHOLD, SIFT


def track(
    roi_cur: np.ndarray,
    roi_prev: np.ndarray,
    kpnts_prev: np.ndarray = None,
    desc_prev: np.ndarray = None,
    dst_pnts: np.ndarray = None,
) -> tuple[np.ndarray, int, int, np.ndarray, np.ndarray, np.ndarray]:
    """Track the wound and estimate its displacement

    Args:
        roi_cur (np.ndarray): current ROI
        roi_prev (np.ndarray): previous ROI to compare with
        kpnts_prev (np.ndarray, optional): key points in the previous frame
        desc_prev (np.ndarray, optional): descriptors in the previous frame
        dst_pnts (np.ndarray, optional): destination points in the previous frame

    Returns:
        tuple[np.ndarray, int, int, np.ndarray, np.ndarray, np.ndarray]:
        source points,
        X- and Y-axes displacement (px),
        key points,
        descriptors,
        and destination points of the current frame
    """
    ## if it is not the first run, use previously calculated values as values
    ## for the `roi_prev`, otherwise calculate them
    if kpnts_prev:
        src_pnts = dst_pnts
    else:
        kpnts_prev, desc_prev = SIFT.detectAndCompute(roi_prev, None)
        src_pnts = None

    # extract features from the current ROI
    kpnts_cur, desc_cur = SIFT.detectAndCompute(roi_cur, None)
    desc_prev = np.float32(desc_prev)
    desc_cur = np.float32(desc_cur)

    # match features, apply Lowe's ratio to filter bad matches
    matcher = FLANN.knnMatch(desc_prev, desc_cur, k=2)
    matches = []  # good matches
    for m, n in matcher:
        if m.distance < FLANN_THRESHOLD * n.distance:
            matches.append(m)

    # find features old and new coordinates
    if not src_pnts:
        src_pnts = np.float32([kpnts_prev[m.queryIdx].pt for m in matches]).reshape(
            -1, 1, 2
        )
    dst_pnts = np.float32([kpnts_cur[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # calculate the median displacement
    moved_X = APPROX_FUNC(dst_pnts[:, 0, 0] - src_pnts[:, 0, 0])
    moved_Y = APPROX_FUNC(dst_pnts[:, 0, 1] - src_pnts[:, 0, 1])

    return (
        src_pnts,
        moved_X,
        moved_Y,
        kpnts_cur,
        desc_cur,
        dst_pnts,
    )


def rotation(src_pnts: np.ndarray, dst_pnts: np.ndarray) -> float:
    """Estimate rotation

    Args:
        src_pnts (np.ndarray): source points
        dst_pnts (np.ndarray): destination points

    Returns:
        float: (deg) occurred rotation in one plane
    """
    M, _ = cv2.findHomography(src_pnts, dst_pnts, cv2.RANSAC, ransacReprojThreshold=3.0)
    return np.degrees(np.arctan2(M[1, 0], M[0, 0]))
