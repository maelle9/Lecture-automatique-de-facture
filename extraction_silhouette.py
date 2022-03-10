import numpy as np
import cv2
import matplotlib.pyplot as plt
import imgutils

def silhouette(path):
    src = cv2.imread(path)
    Color = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    Resize = imgutils.opencv_resize(Color, 450 / Color.shape[0])
    Blur = cv2.GaussianBlur(Resize, (3, 3), 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    Struct = cv2.dilate(Blur, kernel, iterations=2)
    image = cv2.Canny(Struct, 100, 100, apertureSize=3)
    return image




