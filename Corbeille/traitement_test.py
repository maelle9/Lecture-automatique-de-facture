from matplotlib import pyplot as plt
from scipy import ndimage
from skimage.filters import threshold_local
import imgutils
import cv2
from scipy.ndimage.filters import median_filter
import numpy as np
from skimage.exposure import rescale_intensity
from PIL import Image


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

# ---- Luminosité ----
# contrast = 1.2
# brightness = 0
# img = cv2.addWeighted(img, contrast, img, 0, brightness)

# p_low, p_high = np.percentile(img, (1, 95))
# img = rescale_intensity(img, in_range=(p_low, p_high))

# ---- threshold ----
# img = cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
# img = cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)



"""
# Test rotation text
osd_rotated_image = pytesseract.image_to_osd(image)
angle_rotated_image = re.search('(?<=Rotate: )\d+', osd_rotated_image).group(0)
print(angle_rotated_image)
"""