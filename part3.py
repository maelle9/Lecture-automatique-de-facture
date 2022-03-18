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


def is_number(num):
    try :
        float(num)
        return True
    except ValueError:
        return False

def if_somethings_before_number(num):
    try :
        float(num[1:])
        return True
    except ValueError:
        return False

def affiche_total(image):
    print(read_text(image))
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    df = pd.DataFrame(data)
    df['text'] = df['text'].str.lower()
    df.text = df.text.str.replace(',', '.')
    df.text = df.text.str.replace('[$,EUR,€,\',"]', '')
    df = df[(df['text'] != "") & (df['conf'] > "10")]
    df['digit'] = [is_number(word) for word in df['text']]
    if not "total" in list(df['text']):
        total = list_chiffre_a_droite(image,df)
    else:
        if (search_total(df) == '0'):
            print("methode chiffre à droite")
            total = list_chiffre_a_droite(image,df)
        else:
            total = search_total(df)
    return total


def search_total(df):
    try:
        index_list = list(df.index[df['text'] == "total"])
        top_word_total = df['top'][index_list[-1]]
        df = df[(df['text'] != "total") & (df['digit'] == True)]
        df = df[df['text'].notnull()].copy()
        df['text'] = df['text'].astype(float)
        df = df[(df['top'] < top_word_total+3) & (df['top'] > top_word_total-3)]
        print(df)
        total = select_le_plus_grand_chiffre(df)
    except Exception:
        print("error function - search_total 2")
    return total


def list_chiffre_a_droite(image,df):
    left = int(image.shape[1]/2)
    top = int(image.shape[0]/3)
    df = df[(df['text'] != "") & (df['left'] > left) & (df['top'] > top) & (df['digit'] == True)]
    total = select_le_plus_grand_chiffre(df)
    print(df)
    return total

def select_le_plus_grand_chiffre(df):
    total = '0'
    if (len(df) == 1):
        total = list(df['text'])[0]
    elif (len(df) > 1):
        df = df[df['text'].notnull()].copy()
        df['text'] = df['text'].astype(float)
        #moyenne_hauteur = df.height.mean()
        df = df[(df['text'] < 10000000)] # & (df['height'] >= moyenne_hauteur)
        df = df.sort_values(by=['text'], ascending=False)
        total = list(df['text'])[0]
    else:
        print("Liste vide - Pas de total trouvé")
    return total


# =============================== Brouillon =======================================
"""
def read_table_verification():
    df = pd.read_csv("table_de_verification.csv", sep=";")
    print(df)

def search_total(data):
    total = "0"
    try:
        index_word_total = data['text'].index("total")
        df = pd.DataFrame(data)
        df.text = df.text.str.replace('[$,EUR,€,\',"]', '')
        print("F")
        for i in range (len(df['text'])):
            precision = -2
            for j in range (abs(precision)*2+1): # precision
                print("A")
                if (is_number(df['text'][i])==False):
                    print("B")
                    if (if_letter_before_number(df['text'][i]) != False):
                        df.loc[i, 'text']= if_letter_before_number(df['text'][i])
                        print("C")
                if (df['top'][i] == df['top'][index_word_total + precision] and df['text'][i] != "total" and df['text'][i] != "" and is_number(df['text'][i])==True):
                    print("D")
                    total = df['text'][i]
                precision +=1
                print("E")
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

def a(num):
    try :
        float(num)
        return True
    except ValueError:
        return False

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
"""