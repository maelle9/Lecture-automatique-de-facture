import numpy as np
import cv2
import matplotlib.pyplot as plt
import self as self
from skimage.exposure import rescale_intensity

import imgutils

def silhouette(path):
    src = cv2.imread(path)
    bordersize = 10
    border = cv2.copyMakeBorder(src, top=bordersize, bottom=bordersize, left=0, right=bordersize,
                                borderType=cv2.BORDER_ISOLATED, value=[0, 0, 0])
    Resize = imgutils.opencv_resize(border, 800 / border.shape[0])
    Blur = cv2.GaussianBlur(Resize, (3, 3), 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    Struct = cv2.dilate(Blur, kernel)
    image = cv2.Canny(Struct, 100, 300, apertureSize=3)
    self.array_alpha = np.array([1.75])
    cv2.multiply(image, self.array_alpha, image)

    th, im_th = cv2.threshold(image, 0, 255,
                              cv2.THRESH_BINARY_INV +
                              cv2.THRESH_OTSU)
    # Copy the thresholded image.
    im_floodfill = im_th.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_th.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255);

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    cv2.waitKey(0)
    cv2.imwrite('data/output.jpg', im_floodfill_inv)
    return Resize, image


