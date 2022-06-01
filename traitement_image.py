from scipy import ndimage
import imgutils
import cv2
import numpy as np
from PIL import Image

def silhouette(path):
    src = cv2.imread(path)

    # --- Trouve la couleur d'un pixel du fond ---
    image = Image.open(path)
    image = image.convert("RGB")
    coordonee = x, y = 10, 10
    pixel = image.getpixel(coordonee)

    # --- Rajoute une bordure ---
    bordersize = 5
    border = cv2.copyMakeBorder(src, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize,
                                borderType=cv2.BORDER_ISOLATED, value=pixel)
    Resize = imgutils.opencv_resize(border, 800 / border.shape[0])

    # --- Image en niveau de gris ---
    img = cv2.cvtColor(Resize, cv2.COLOR_BGR2GRAY)

    # --- Filtre ---
    img = ndimage.maximum_filter(img, size=5) # pour les reflets
    img = cv2.medianBlur(img, 5) # flouter l'image
    img = cv2.Canny(img, 200, 200)

    # --- Fermeture morphologique ---
    kernel = np.ones((5,5))
    img = cv2.dilate(img, kernel, iterations=3)
    img = cv2.erode(img, kernel, iterations=2)

    return Resize, img

def traitement_apres_recadrage_2 (img):
    # --- Enleve un contour de 5 px ---
    h = int(img.shape[1])
    w = int(img.shape[0])
    pixel = 5
    img = img[pixel:(w-pixel), pixel:(h-pixel)]

    # --- Resize ---
    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)

    # --- Image en niveau de gris ---
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- Enleve bruit ---
    kernel = np.ones((1, 1))
    img = cv2.dilate(img, kernel, iterations=2)
    img = cv2.erode(img, kernel, iterations=2)

    # --- Unsharp mask --- Permet de déflouter un peu
    gaussian_3 = cv2.GaussianBlur(img, (0, 0), 2.0)
    img = cv2.addWeighted(img, 2.0, gaussian_3, -1.0, 0)

    # imgutils.affiche(img)
    return img

