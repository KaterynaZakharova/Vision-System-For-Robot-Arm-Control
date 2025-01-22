"""Configuration for tracking algorithms"""

import cv2
import numpy as np

### Choose feature extraction and matching algorithms
SIFT = cv2.SIFT_create(nfeatures=100)  # feature extractor (SIFT here)
# parameters for matcher
index_params = dict(algorithm=1, trees=4)
search_params = dict(checks=10)
FLANN = cv2.FlannBasedMatcher(
    index_params, search_params
)  # feature matcher (FLANN in our case OR try BF matcher instead (line below))
# feature_matcher_BF = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)

# filter for good matches
FLANN_THRESHOLD = 0.8

# function to use to get one number from a list of displacements
APPROX_FUNC = np.median
