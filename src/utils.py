import numpy as np
import cv2


def image_from_buffer(buffer: np.ndarray, invert=False):
    image = cv2.imdecode(np.frombuffer(buffer, np.uint8), -1)
    if invert:
        image = image[:, :, ::-1]
    return image
