import pandas as pd
import pytesseract
from matplotlib import pyplot as plt
from pytesseract import Output
import cv2 # pip install opencv-python
from paddleocr import PaddleOCR

import traitement

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

liste_total = ['total', 'totale', 'tot', 'tota', 'otal', 'totl', 'due', 'amt', 'amount', 'amoun','amont', 'balance']

liste_parasite = ['account','caisse','change', 'charge', 'check','code','date', 'discout', 'fee', 'gratuity', 'gratuit', 'guests',
                  'id', 'item','monnaie','no', 'num', 'number', 'numero','order','other', 'received','receipt', 'ref', 'reference',
                  'rendu','sale', 'sales', 'service','sous','sos','soustotal', 'subtotal', 'sub-total','sb', 'sub', 'tax', 'taxe','taxable', 'terminal',
                  'tva', 'tip', 'ticket','table', 'vat', '%', '#']

def read_text_pytesseract (img):
    text = pytesseract.image_to_string(img)  # ,lang = 'eng'
    return text

def read_text_paddle(img):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(img, cls=True)
    for line in result:
        print(line[1][0])


def affiche_rectangle (image, color, thickness):
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    nbRectangle = len(data['level'])
    for i in range(nbRectangle):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
        """
        print(x, y, w, h)
        #https://mindee.github.io/doctr/getting_started/installing.html OCR
        cropped = image[y:y + h, x:x + w]
        plt.imshow(cropped)
        plt.show()"""

    plt.imshow(image)
    plt.show()


def is_number(num):
    try :
        float(num)
        return True
    except ValueError:
        return False

def count_difference_between_word(a,b):
    zipped = zip(a, b)
    difference = sum(1 for e in zipped if e[0] != e[1])
    difference = difference + abs(len(a) - len(b)) # si les 2 chaînes sont de longueur différente -> ajoute la différence de longueur
    return difference

def clean_df (df):
    df = df[["top","left","height","width","conf","text"]]
    df['text'] = df['text'].astype(str).str.lower()
    df.text = df.text.str.replace(',', '.')
    df.text = df.text.str.replace('[$,¥,€,\',",«,»]', '')
    #df.text = df.text.str.replace('[;,:,=,-]', ' ')
    df["text"] = df.apply(lambda row: "%" if '%' in row["text"] else row["text"], axis=1)
    df["text"] = df.apply(lambda row: "#" if '#' in row["text"] else row["text"], axis=1)
    df = df[(df['text'] != "") & (df['text'] != " ") & (df['conf'] > "10")]

    print(list(df['text']))
    if(df.empty == False):
        DF = pd.DataFrame()
        for index, row in df.iterrows():
            liste_text = row['text'].split()
            for i in range (len(liste_text)):
                row_add = pd.Series([row['top'],row['left'],row['height'],row['width'],row['conf'],liste_text[i]], index=df.columns)
                DF = DF.append(row_add, ignore_index=True)
        df = DF.copy()
    # Is somethings before number - S'il y a un caractère devant un chiffre alors on l'enleve car il s'agit probablement d'un "$" mal lu
    try:
        df["text"] = df.apply(lambda row:row["text"][1:] if (row["text"][0] != '.' and is_number(row["text"][0]) == False and is_number(row["text"][1:]) == True)
                                                        else row["text"], axis=1)
    except:
        print('Is somethings before number not work')

    # Is somethings after number - S'il y a un caractère après un chiffre alors on l'enleve car il s'agit probablement d'un "E" mal lu
    try:
        df["text"] = df.apply(lambda row:row["text"][:-1] if (row["text"][-1] != '.' and is_number(row["text"][-1]) == False and is_number(row["text"][:-1]) == True)
                                                        else row["text"], axis=1)
    except:
        print('Is somethings after number not work')

    if(df.empty == False):
        df['digit'] = [is_number(word) for word in df['text']]
        df["diff"] = [count_difference_between_word(word, 'total') for word in df['text']]
        df["text"] = df.apply(lambda row: 'total' if (row["diff"] <= 1) else row["text"], axis=1)
    return df

def displayTextDf(df_pytes, df_padd):
    print('---- df_pytes ----')
    print(list(df_pytes['text']))
    print('---- df_padd ----')
    print(list(df_padd['text']))

def affiche_total(image):
    image = traitement.traitement_apres_recadrage_2(image)
    df_pytes = df_pytesseract(image)
    df_padd = df_paddle(image)
    total = '0'
    displayTextDf(df_pytes, df_padd)
    synonyme_total_trouver = False
    if(df_padd.empty == False and df_pytes.empty == False):
        df_pytes = clean_df(df_pytes)
        df_padd = clean_df(df_padd)
        displayTextDf(df_pytes, df_padd)
    if (df_padd.empty == False and df_pytes.empty == False):
        for i in range (len(liste_total)):
            if liste_total[i] in list(df_padd['text']):
                total = search_total(df_padd)
                synonyme_total_trouver = True
                break
        if (synonyme_total_trouver == False):
            for i in range(len(liste_total)):
                if liste_total[i] in list(df_pytes['text']):
                    total = search_total(df_pytes)
                    break
        if (total == '0'):
            df_padd = elimination_des_mots_parasites(df_padd)
            total = list_chiffre_a_droite(image,df_padd)
        if (total == '0'):
            df_pytes = elimination_des_mots_parasites(df_pytes)
            total = list_chiffre_a_droite(image,df_pytes)
    else:
        displayTextDf(df_pytes, df_padd)
        if(df_padd.empty == False):
            df_padd = clean_df(df_padd)
            if (df_padd.empty == False):
                for i in range(len(liste_total)):
                    if liste_total[i] in list(df_padd['text']):
                        total = search_total(df_padd)
                        break
                if (total == '0'):
                    df_padd = elimination_des_mots_parasites(df_padd)
                    total = list_chiffre_a_droite(image, df_padd)
        if(df_pytes.empty == False and total == '0'):
            df_pytes = clean_df(df_pytes)
            if(df_pytes.empty == False):
                for i in range(len(liste_total)):
                    if liste_total[i] in list(df_pytes['text']):
                        total = search_total(df_pytes)
                        break
                if (total == '0'):
                    df_pytes = elimination_des_mots_parasites(df_pytes)
                    total = list_chiffre_a_droite(image, df_pytes)
    return total

def df_pytesseract(image):
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    df = pd.DataFrame(data)
    """
    # Test rotation text
    osd_rotated_image = pytesseract.image_to_osd(image)
    angle_rotated_image = re.search('(?<=Rotate: )\d+', osd_rotated_image).group(0)
    print(angle_rotated_image)
    """
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
        text.append(str(line[1][0]))
    d = {"top": top, "left": left, "height": height, "width": width, "conf": conf, "text": text}
    df = pd.DataFrame(d)
    return df

def find_text_on_the_same_line (top, text, df):
    df = df[(df['top'] >= top-10) & (df['top'] <= top+10) & (df['text'] != text)]
    return list(df['text'])


def mot_total (list):
    presence = False
    for i in range (len(liste_total)):
        if (liste_total[i] in list):
            presence = True
            break
    return presence

def search_total(df):
    try:
        total = '0'
        df_not_digit = df[(df['digit'] == False)]
        df_digit = elimination_des_mots_parasites(df)

        df_digit["total_word"] = df_digit.apply(lambda row: mot_total(row["list"]),axis=1)
        df_digit = df_digit[(df_digit['total_word'] == True)]

        df_not_digit["total_word"] = df_not_digit.apply(lambda row: True if row["text"] in liste_total else False,axis=1)
        df_not_digit = df_not_digit[(df_not_digit['total_word'] == True)]

        left = min(list(df_not_digit['left']))

        print(df_digit[['top', 'left', 'height', 'conf', 'text', 'list']])
        print(df_not_digit[['top', 'left', 'height', 'conf', 'text']])

        df_digit = df_digit[(df_digit['left'] >= left)]
        total = select_le_plus_grand_chiffre(df_digit)
        print(df_digit[['top', 'left', 'height', 'conf', 'text', 'list']])
    except Exception:
        print("error function - search_total")
    return total

def mot_parasites (list):
    presence = False
    for i in range (len(liste_parasite)):
        if (liste_parasite[i] in list):
            presence = True
            break
    return presence

def elimination_des_mots_parasites(df):
    try:
        df_not_digit = df[(df['digit'] == False)]
        df_digit = df[(df['digit'] == True)]
        df_digit["list"] = df_digit.apply(lambda row: find_text_on_the_same_line(row["top"],row["text"], df_not_digit) ,axis=1)
        df_digit["parasites_word"] = df_digit.apply(lambda row: mot_parasites(row["list"]),axis=1)
        df_digit = df_digit[(df_digit['parasites_word'] == False)]
    except Exception:
        df_digit = df.copy()
        print("error function - elimination_des_mots_parasites")
    return df_digit

def list_chiffre_a_droite(image,df):
    left = int(image.shape[1]/2)
    top = int(image.shape[0]/3)
    print(df[['top', 'left', 'height', 'conf', 'text', 'list']])
    df = df[(df['text'] != "") & (df['left'] > left) & (df['top'] > top) & (df['digit'] == True)]
    print(df[['top', 'left', 'height', 'conf', 'text', 'list']])

    #df = verifie_si_chiffre_pas_en_2_parties(df)
    df = format_chiffre(df)
    print("format")
    print(df[['top', 'left', 'height', 'conf', 'text', 'list']])
    total = select_le_plus_grand_chiffre(df[(df['conf'] > "80")])
    return total


def format_chiffre_(chiffre):  # xx.xx
    try:
        if (chiffre[-3] == '.' and len(chiffre) >=4): return True
        else: return False
    except Exception:
        return False

def format_chiffre(df):
    try:
        df["format"] = df.apply(lambda row: format_chiffre_(row["text"]) ,axis=1)
        df = df[(df['format'] == True)]
    except Exception: print('error - format chiffre')
    return df


def select_le_plus_grand_chiffre(df):
    total = '0'
    if (len(df) == 1):
        df = df[df['text'].notnull()].copy()
        df['text'] = df['text'].astype(float)
        df = df[(df['text'] < 40000)]
        total = list(df['text'])[0]
    elif (len(df) > 1):
        df = df[df['text'].notnull()].copy()
        df['text'] = df['text'].astype(float)
        print(df[['top', 'left', 'height', 'conf', 'text', 'list']])
        #moyenne_hauteur = df.height.mean()
        df = df[(df['text'] < 40000)] #(df['height'] >= moyenne_hauteur-1)
        df = df.sort_values(by=['text'], ascending=False)
        if (len(df) > 0) : total = list(df['text'])[0]
    else: print("Liste vide - Pas de total trouvé")
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
        if (a < b +6 and a > b -6 and a1 < b1 + 1 and a1 > b1 -1):
            if "." not in a2 and "." not in b2 or "." in a2 and "." not in b2 or "." not in a2 and "." in b2:
                DF = df[(df['top'] != a) & (df['height'] != a1) & (df['top'] != b) & (df['height'] != b1)]
                df_new_line = pd.DataFrame([[int((a1+b1)/2), float(str(b2)+str(a2))]], columns=['height', 'text'])
                DF = pd.concat([DF, df_new_line], ignore_index=True)
        b = a
        b1 = a1
        b2 = a2
    return DF

# BALENCE DUE + PAYEMENT

