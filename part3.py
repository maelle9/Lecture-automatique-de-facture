import pandas as pd

from PIL import Image
import pytesseract
from pytesseract import Output
import cv2 # pip install opencv-python
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def read_text (path):
    img = Image.open(path)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(img)  # , lang = 'eng'
    return text

def affiche_rectangle (window_name, image, color, thickness):
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    nbRectangle = len(data['level'])
    for i in range(nbRectangle):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)

def read_table_verification():
    df = pd.read_csv("table_de_verification.csv", sep=";")
    print(df)

def search_total(image):
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
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

def list_texte_a_droite(image):
    left = int(image.shape[1]/2)
    top = int(image.shape[0]/3)
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    df = pd.DataFrame(data)
    df = df[(df['text'] != "") & (df['left'] > left) & (df['top'] > top)]
    return df

def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result: return True
    else: return False

def list_chiffre_a_droite(image):
    df = list_texte_a_droite(image)
    df.text = df.text.str.replace(',', '.')
    df.text = df.text.str.replace('[$,EUR,€]', '')
    df['digit'] = [is_number(word) for word in df['text']]
    return df[(df['text'] != "") & (df['digit'] == True) & (df['conf'] >"60")]


def affiche_total (image):
    df = list_chiffre_a_droite(image)
    df['text'] = df['text'].astype(float)
    df = df.sort_values(by=['text'], ascending=False)
    print("LE TOTAL DE CETTE FACURE EST :", df.text.iloc[0])

    #search_total(image)

