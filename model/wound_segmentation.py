"""Load U-Net model for wound segmentation"""

import numpy as np

np.object = object
np.bool = bool
np.int = int

from config.model import MODEL_PATH, NET_SIZE
from tensorflow import keras
from tensorflow.keras import layers


def build_unet_model(input_shape: tuple[int, int, int]) -> keras.Model:
    """Initialize model

    U-Net model architecture.

    Args:
        input_shape (tuple[int, int, int]): input image size (height,
        width, channels)

    Returns:
        keras.Model: wound segmentation model
    """
    inputs = keras.Input(shape=input_shape)

    # Encoder
    conv1 = layers.Conv2D(
        64, 3, activation='relu', kernel_initializer='he_normal', padding='same'
    )(inputs)
    conv1 = layers.Conv2D(
        64, 3, activation='relu', kernel_initializer='he_normal', padding='same'
    )(conv1)
    pool1 = layers.MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = layers.Conv2D(
        128, 3, activation='relu', kernel_initializer='he_normal', padding='same'
    )(pool1)
    conv2 = layers.Conv2D(
        128, 3, activation='relu', kernel_initializer='he_normal', padding='same'
    )(conv2)
    pool2 = layers.MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = layers.Conv2D(
        256, 3, activation='relu', kernel_initializer='he_normal', padding='same'
    )(pool2)
    conv3 = layers.Conv2D(
        256, 3, activation='relu', kernel_initializer='he_normal', padding='same'
    )(conv3)
    pool3 = layers.MaxPooling2D(pool_size=(2, 2))(conv3)

    # Bottleneck
    conv4 = layers.Conv2D(
        512, 3, activation='relu', kernel_initializer='he_normal', padding='same'
    )(pool3)
    conv4 = layers.Conv2D(
        512, 3, activation='relu', kernel_initializer='he_normal', padding='same'
    )(conv4)

    # Decoder
    up1 = layers.UpSampling2D((2, 2))(conv4)
    concat1 = layers.Concatenate(axis=-1)([conv3, up1])
    conv5 = layers.Conv2D(
        256, 3, activation='relu', kernel_initializer='he_normal', padding='same'
    )(concat1)
    conv5 = layers.Conv2D(
        256, 3, activation='relu', kernel_initializer='he_normal', padding='same'
    )(conv5)
    up2 = layers.UpSampling2D((2, 2))(conv5)

    concat2 = layers.Concatenate(axis=-1)([conv2, up2])
    conv6 = layers.Conv2D(
        128, 3, activation='relu', kernel_initializer='he_normal', padding='same'
    )(concat2)
    conv6 = layers.Conv2D(
        128, 3, activation='relu', kernel_initializer='he_normal', padding='same'
    )(conv6)
    up3 = layers.UpSampling2D((2, 2))(conv6)

    concat3 = layers.Concatenate(axis=-1)([conv1, up3])
    conv7 = layers.Conv2D(
        128, 3, activation='relu', kernel_initializer='he_normal', padding='same'
    )(concat3)
    conv7 = layers.Conv2D(
        128, 3, activation='relu', kernel_initializer='he_normal', padding='same'
    )(conv7)

    outputs = layers.Conv2D(1, 1, activation='sigmoid')(conv7)
    return keras.Model(inputs=inputs, outputs=outputs)


### Loading the wound segmentation model
model = build_unet_model(NET_SIZE)  # trained model size
model.load_weights(MODEL_PATH)
