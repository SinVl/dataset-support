import cv2
from matplotlib import pyplot as plt

from src.image_provider import ImageProvider

if __name__ == "__main__":
    # cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    provider = ImageProvider()
    provider.send_request("crocodile")
    images = provider.get_images(6)
    for i, image in enumerate(images):
        plt.subplot(3, 3, i+1)
        plt.imshow(image)
    plt.show()
        # cv2.imshow('image', image)
        # while cv2.waitKey(0) != 32:
        #    pass
