import pandas as pd
from PIL import Image
import pytesseract
from matplotlib import pyplot as plt
from pytesseract import Output
import cv2 # pip install opencv-python
from paddleocr import PaddleOCR

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def read_text_pytesseract (img):
    text = pytesseract.image_to_string(img)  # , lang = 'eng'
    return text

def read_text_paddle(img):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(img, cls=True)
    #for line in result:
        #print(line[1][0])


def affiche_rectangle (image, color, thickness):
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    nbRectangle = len(data['level'])
    for i in range(nbRectangle):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
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
    print(read_text_pytesseract(image))
    #df = df_pytesseract(image)
    df = df_paddle(image)
    total = '0'
    if(df.empty == False):
        df['text'] = df['text'].str.lower()
        print("ici:",df['text'])
        df.text = df.text.str.replace(',', '.')
        df.text = df.text.str.replace('[$,EUR,€,\',"]', '')
        df = df[(df['text'] != "") & (df['conf'] > "50")]
        df['digit'] = [is_number(word) for word in df['text']]

        if not "total" in list(df['text']):
            total = list_chiffre_a_droite(image,df)
        else:
            if (search_total(df) == '0'):
                print("methode chiffre à droite")
                total = list_chiffre_a_droite(image,df)
            else:
                total = search_total(df)
    else:
        df2 = df_pytesseract(image)
        if (df2.empty == False):
            df2['text'] = df2['text'].str.lower()
            print("ici:",df['text'])
            df2.text = df2.text.str.replace(',', '.')
            df2.text = df2.text.str.replace('[$,EUR,€,\',"]', '')
            df2 = df2[(df2['text'] != "") & (df2['conf'] > "50")]
            df2['digit'] = [is_number(word) for word in df2['text']]

            if not "total" in list(df2['text']):
                total = list_chiffre_a_droite(image, df2)
            else:
                if (search_total(df2) == '0'):
                    print("methode chiffre à droite")
                    total = list_chiffre_a_droite(image, df2)
                else:
                    total = search_total(df2)
    return total

def df_pytesseract(image):
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
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
        conf.append(str(line[1][1]*100))
        text.append(line[1][0])
    d = {"top": top, "left": left, "height": height, "width": width, "conf": conf, "text": text}
    df = pd.DataFrame(d)
    return df


def search_total(df):
    try:
        total = '0'
        index_list = list(df.index[df['text'] == "total"])
        top_word_total = df['top'][index_list[-1]]
        df = df[(df['text'] != "total") & (df['digit'] == True)]
        df = df[df['text'].notnull()].copy()
        df['text'] = df['text'].astype(float)
        df = df[(df['top'] < top_word_total+3) & (df['top'] > top_word_total-3)]
        total = select_le_plus_grand_chiffre(df)
        #print(df[['top', 'left', 'height', 'conf', 'text']])
    except Exception:
        print("error function - search_total 2")
    return total

def elimination_des_mots_parasites(df): # A FINIR
    try:
        total = '0'
        index_list = list(df.index[df['text'] == "ticket"])
        top_word_total = df['top'][index_list[-1]]
        df = df[(df['text'] != "total") & (df['digit'] == True)]
        df = df[df['text'].notnull()].copy()
        df['text'] = df['text'].astype(float)
        df = df[(df['top'] < top_word_total+3) & (df['top'] > top_word_total-3)]
        total = select_le_plus_grand_chiffre(df)
        #print(df[['top', 'left', 'height', 'conf', 'text']])
    except Exception:
        print("error function - elimination_des_mots_parasites")
    return total


def list_chiffre_a_droite(image,df):
    left = int(image.shape[1]/2)
    top = int(image.shape[0]/3)
    df = df[(df['text'] != "") & (df['left'] > left) & (df['top'] > top) & (df['digit'] == True)]
    total = select_le_plus_grand_chiffre(df)
    #print(df[['top','left','height','conf','text']])
    return total

def select_le_plus_grand_chiffre(df):
    df = verifie_si_chiffre_pas_en_2_parties(df)
    total = '0'
    if (len(df) == 1):
        total = list(df['text'])[0]
    elif (len(df) > 1):
        df = df[df['text'].notnull()].copy()
        df['text'] = df['text'].astype(float)
        moyenne_hauteur = df.height.mean()
        df = df[(df['text'] < 10000000) & (df['height'] >= moyenne_hauteur)]
        df = df.sort_values(by=['text'], ascending=False)
        total = list(df['text'])[0]
    else:
        print("Liste vide - Pas de total trouvé")
    return total

def verifie_si_chiffre_pas_en_2_parties(df):
    df = df.sort_values(by=['top'], ascending=False)
    b = 0
    b1 = 0
    b2 = 0
    DF = df.copy()
    for index, row in df.iterrows():
        a = row['top']
        a1 = row['height']
        a2 = row['text']
        if (a < b +4 and a > b -4 and a1 < b1 + 2 and a1 > b1 -2):
            if "." not in a2 and "." not in b2 or "." in a2 and "." not in b2 or "." not in a2 and "." in b2:
                DF = df[(df['top'] != a) & (df['height'] != a1) & (df['top'] != b) & (df['height'] != b1)]
                df_new_line = pd.DataFrame([[int((a1+b1)/2), float(str(b2)+str(a2))]], columns=['height', 'text'])
                DF = pd.concat([DF, df_new_line], ignore_index=True)
        b = a
        b1 = a1
        b2=a2
    return DF

# BALENCE DUE + PAYEMENT