import numpy as np
import cv2
import matplotlib.pyplot as plt
import self as self
from skimage.exposure import rescale_intensity

import imgutils

def silhouette(src):
    #src = cv2.imread(path)
    bordersize = 10
    border = cv2.copyMakeBorder(src, top=bordersize, bottom=bordersize, left=0, right=bordersize,
                                borderType=cv2.BORDER_ISOLATED, value=[0, 0, 0])
    Resize = imgutils.opencv_resize(border, 800 / border.shape[0])
    Blur = cv2.GaussianBlur(Resize, (3, 3), 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    Struct = cv2.dilate(Blur, kernel)
    image = cv2.Canny(Struct, 100, 100, apertureSize=3)
    return Resize, image


