import pandas as pd
import pytesseract
from pytesseract import Output
import cv2  # pip install opencv-python
from paddleocr import PaddleOCR

import imgutils

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# ----------------------------------------------------------------------------------------------------------------------
#               Lit le contenu de l'image
# ----------------------------------------------------------------------------------------------------------------------

def read_text_pytesseract(img):
    text = pytesseract.image_to_string(img)  # ,lang = 'eng'
    return text


def read_text_paddle(img):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(img, cls=True)
    for line in result:
        print(line[1][0])


# ----------------------------------------------------------------------------------------------------------------------
#               Affiche des rectangles autour du texte sur l'image
# ----------------------------------------------------------------------------------------------------------------------

def affiche_rectangle_pytesseract(image, color, thickness):
    data = pytesseract.image_to_data(image, output_type=Output.DICT, lang='eng', config='--psm 11')
    affiche_rectangle(data, image, color, thickness)


def affiche_rectangle_paddle(image, color, thickness):
    data = df_paddle(image)
    affiche_rectangle(data, image, color, thickness)


def affiche_rectangle(data, image, color, thickness):
    for i in range(len(data['left'])):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
        # cropped = image[y:y + h, x:x + w]
        # plt.imshow(cropped)
        # plt.show()
    imgutils.affiche(image)


# ----------------------------------------------------------------------------------------------------------------------
#               Convertit le texte des images en dataFrame
# ----------------------------------------------------------------------------------------------------------------------

def df_pytesseract(image):
    data = pytesseract.image_to_data(image, output_type=Output.DICT, lang='eng', config='--psm 11')
    df = pd.DataFrame(data)
    return df


def df_paddle(image):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(image, cls=True)
    top, left, height, width, conf, text = [], [], [], [], [], []
    for line in result:
        top.append(int(line[0][0][1]))
        left.append(int(line[0][0][0]))
        height.append(int(line[0][2][1]) - int(line[0][0][1]))
        width.append(int(line[0][2][0]) - int(line[0][0][0]))
        conf.append(str(line[1][1] * 100))
        text.append(str(line[1][0]))
    d = {"top": top, "left": left, "height": height, "width": width, "conf": conf, "text": text}
    df = pd.DataFrame(d)
    return df
