import numpy as np
import cv2
import matplotlib.pyplot as plt
import imgutils

def silhouette(path):
    src = cv2.imread(path)
    bordersize = 10
    border = cv2.copyMakeBorder(src, top=bordersize, bottom=bordersize, left=0, right=bordersize,
                                borderType=cv2.BORDER_ISOLATED, value=[0, 255, 0])
    Resize = imgutils.opencv_resize(border, 800 / border.shape[0])
    Color = cv2.cvtColor(Resize, cv2.COLOR_BGR2GRAY)
    Blur = cv2.GaussianBlur(Color, (3, 3), 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    Struct = cv2.dilate(Blur, kernel)
    image = cv2.Canny(Struct, 100, 100, apertureSize=3)
    return Resize, image




