import pandas as pd

from PIL import Image
import pytesseract
from pytesseract import Output
import cv2 # pip install opencv-python
import re

def read_text (path):
    img = Image.open(path)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(img)  # , lang = 'eng'
    return text

def create_data_image(path):
    img = Image.open(path)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    return pytesseract.image_to_data(img, output_type=Output.DICT)

def affiche_rectangle (window_name, path, color, thickness):
    data = create_data_image(path)
    image = cv2.imread(path)
    nbRectangle = len(data['level'])
    for i in range(nbRectangle):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)

def read_table_verification():
    df = pd.read_csv("table_de_verification.csv", sep=";")
    print(df)


def search_total(path):
    data = create_data_image(path)
    data['text'] = [word.lower() for word in data['text']]
    if not "total" in data['text']:
        print("NE SAIT PAS")
    else:
        index_word_total = data['text'].index("total")
        for i in range (len(data['text'])):
            precision = -2
            for j in range (abs(precision)*2+1): # precision
                if (data['top'][i] == data['top'][index_word_total + precision] and data['text'][i] != "total" and data['text'][i] != ""):
                    print("SOLUTION", data['text'][i])
                precision +=1

def list_texte_a_droite(path):
    image = cv2.imread(path)
    left = int(image.shape[1]/2)
    top = int(image.shape[0]/3)
    data = create_data_image(path)
    df = pd.DataFrame(data)
    df = df[(df['text'] != "") & (df['left'] > left) & (df['top'] > top)]
    print(df)
    return df

def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result: return True
    else: return False

def list_chiffre_a_droite(path):
    df = list_texte_a_droite(path)
    df.text = df.text.str.replace('[$,EUR,€]', '')
    df['digit'] = [is_number(word) for word in df['text']]
    return df[(df['text'] != "") & (df['digit'] == True)]


def main_3 ():
    path = "data/1133-receipt.jpg"

    df = list_chiffre_a_droite(path)

    df['text'] = df['text'].astype(float)
    df = df.sort_values(by=['text'], ascending=False)
    print(df.text.head(1))

    affiche_rectangle ('Facture', path, (0, 255, 0), 2)

