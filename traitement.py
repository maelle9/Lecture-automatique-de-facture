from scipy import ndimage
from skimage.filters import threshold_local
import imgutils
import cv2
from scipy.ndimage.filters import median_filter
import numpy as np
from skimage.exposure import rescale_intensity
from PIL import Image

def silhouette(path):
    src = cv2.imread(path)

    image = Image.open(path)
    image = image.convert("RGB")
    coordonee = x, y = 10, 10
    pixel = image.getpixel(coordonee)
    print(pixel)

    bordersize = 5
    border = cv2.copyMakeBorder(src, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize,
                                borderType=cv2.BORDER_ISOLATED, value=pixel)
    Resize = imgutils.opencv_resize(border, 800 / border.shape[0])

    img = cv2.cvtColor(Resize, cv2.COLOR_BGR2GRAY)

    img = ndimage.maximum_filter(img, size=5) # pour les reflets
    #img = cv2.GaussianBlur(img, (5,5),1)
    img = cv2.medianBlur(img, 5)
    img = cv2.Canny(img, 200, 200)
    kernel = np.ones((5,5))
    img = cv2.dilate(img, kernel, iterations=3)
    img = cv2.erode(img, kernel, iterations=1)

    return Resize, img

def traitement_apres_recadrage_2 (img):
    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #ret, img = cv2.threshold(img, 120, 255, cv2.THRESH_TOZERO)

    #T = threshold_local(img, 21, offset=5, method="gaussian")
    #img = (img > T).astype("uint8") * 255


    kernel = np.ones((1,1))
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    #cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    #cv2.adaptiveThreshold(cv2.bilateralFilter(img, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    #cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Pour déflouter un peu -> unsharp mask
    #gaussian_3 = cv2.GaussianBlur(img, (0, 0), 2.0)
    #img = cv2.addWeighted(img, 2.0, gaussian_3, -1.0, 0)

    #contrast = 1.2
    #brightness = 0
    #img = cv2.addWeighted(img, contrast, img, 0, brightness)

    #p_low, p_high = np.percentile(img, (1, 95))
    #img = rescale_intensity(img, in_range=(p_low, p_high))

    #imgutils.affiche(img)
    return img


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