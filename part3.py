import pandas as pd
from PIL import Image
import pytesseract
from matplotlib import pyplot as plt
from pytesseract import Output
import cv2 # pip install opencv-python
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def read_text (img):
    text = pytesseract.image_to_string(img)  # , lang = 'eng'
    return text

def affiche_rectangle (image, color, thickness):
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    nbRectangle = len(data['level'])
    for i in range(nbRectangle):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
    #cv2.imshow(window_name, image)
    #cv2.waitKey(0)
    plt.imshow(image)
    plt.show()

def read_table_verification():
    df = pd.read_csv("table_de_verification.csv", sep=";")
    print(df)

def search_total(data):
    total = "0"
    try:
        index_word_total = data['text'].index("total")
        df = pd.DataFrame(data)
        df.text = df.text.str.replace('[$,EUR,€,\',"]', '')
        for i in range (len(df['text'])):
            precision = -2
            for j in range (abs(precision)*2+1): # precision
                if (is_number(df['text'][i])==False):
                    if (if_letter_before_number(df['text'][i]) != False):
                        df.loc[i, 'text']= if_letter_before_number(df['text'][i])
                if (df['top'][i] == df['top'][index_word_total + precision] and df['text'][i] != "total" and df['text'][i] != "" and is_number(df['text'][i])==True):
                    total = df['text'][i]
                precision +=1
    except Exception:
        print("error function - search_total")
    return total

def list_texte_a_droite(image):
    left = int(image.shape[1]/2)
    top = int(image.shape[0]/3)
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    df = pd.DataFrame(data)
    df = df[(df['text'] != "") & (df['left'] > left) & (df['top'] > top)]
    return df

def if_letter_before_number(num):
    pattern = re.compile(r'^.[0-9]\d*\.[0-9]\d*|.[0-9]\d*')
    result = pattern.match(num)
    if result:
        return num[1:]
    else: return False

def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result: return True
    else: return False

def list_chiffre_a_droite(image):
    total = "0" #Pas trouvé
    try:
        df = list_texte_a_droite(image)
        df.text = df.text.str.replace(',', '.')
        df.text = df.text.str.replace('[$,EUR,€,\',"], ', '')
        df['digit'] = [is_number(word) for word in df['text']]
        df = df[(df['text'] != "") & (df['digit'] == True) & (df['conf'] >"60")]
        if (df.empty):
            print("Total non trouvé")
        else:
            try:
                df['text'] = df['text'].astype(float)
                df = df.sort_values(by=['text'], ascending=False)
                total = df.text.iloc[0]
            except Exception:
                print("could not convert string to float")
    except Exception:
        print("error function - list_chiffre_a_droite")
    return total


def affiche_total (image):
    print(read_text (image))
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    data['text'] = [word.lower() for word in data['text']]
    print(list(data['text']))
    if not "total" in data['text']:
        total = list_chiffre_a_droite(image)
    else:
        if (search_total(data) == 'Total non trouvé'):
            print("Total non trouvé -> utilisation méthode 2")
            total = list_chiffre_a_droite(image)
        else:
            total = search_total(data)
            #print("LE TOTAL DE CETTE FACTURE EST :", search_total(data))
    return total



