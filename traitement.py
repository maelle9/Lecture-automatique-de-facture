import imgutils
import cv2
import numpy as np

def silhouette(path):
    src = cv2.imread(path)
    bordersize = 10
    border = cv2.copyMakeBorder(src, top=bordersize, bottom=bordersize, left=0, right=bordersize,
                                borderType=cv2.BORDER_ISOLATED, value=[0, 0, 0])
    Resize = imgutils.opencv_resize(border, 800 / border.shape[0])
    img = cv2.medianBlur(Resize, 5)
    retval, Blur = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    Struct = cv2.dilate(Blur, kernel)
    image = cv2.Canny(Struct, 100, 100, apertureSize=3)
    return Resize, image


def test_morpho(img):
    th, im_th = cv2.threshold(img, 0, 255,
                              cv2.THRESH_BINARY_INV +
                              cv2.THRESH_OTSU)
    im_floodfill = im_th.copy()
    h, w = im_th.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    cv2.waitKey(0)
    cv2.imwrite('data/output.jpg', im_floodfill_inv)


def pretraitement(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(gray)
    return equ