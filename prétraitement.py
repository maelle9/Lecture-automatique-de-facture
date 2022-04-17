
import numpy as np
import cv2

def pretraitement(path):
    # read a image using imread
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # creating a Histograms Equalization
    # of a image using cv2.equalizeHist()
    equ = cv2.equalizeHist(gray)

    # stacking images side-by-side
    #res = np.hstack((img, equ))
    return equ