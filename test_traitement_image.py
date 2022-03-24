import numpy as np
import cv2
import self
import imgutils
from matplotlib import pyplot as plt


def test_morpho(img):
    # Read image
    #img = cv2.imread(path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    self.array_alpha = np.array([1.7])
    cv2.multiply(gray, self.array_alpha, gray)

    th, im_th = cv2.threshold(gray, 0, 255,
                                    cv2.THRESH_BINARY_INV +
                                    cv2.THRESH_OTSU)
    #Copy the thresholded image.
    im_floodfill = im_th.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0,0), 255);

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    cv2.waitKey(0)
    cv2.imwrite('data/output.jpg', im_floodfill_inv)