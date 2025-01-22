"""Configuration for U-Net model loading and prediction"""

### Load the model
MODEL_PATH = r"wound_segmentation_chkp"
NET_SIZE = (128, 128, 1)

### Configuration for predictions
IMG_SIZE = (128, 128)
BASE_THRESHOLD = 0.7
MIN_THRESHOLD = 0.1
THRESHOLD_STEP = 0.1

### Post-processing
ROI_BORDER = 5  # px
