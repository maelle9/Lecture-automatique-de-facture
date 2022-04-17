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
    for line in result:
        print(line[1][0])


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

def affiche_total(image):
    df = df_pytesseract(image)
    #df = df_paddle(image)
    print(list(df['text']))
    total = '0'
    if(df.empty == False):
        df['text'] = df['text'].astype(str).str.lower()
        df.text = df.text.str.replace(',', '.')
        df.text = df.text.str.replace('[$,EUR,€,\',"]', '')
        df = df[(df['text'] != "") & (df['conf'] > "10")] #79
        df.text = df.text.str.lower()

        # Is somethings before number - S'il y a un caractère devant un chiffre alors on l'enleve car il s'agit probablement d'un "$" mal lu
        try : df["text"] = df.apply(lambda row:
                                    row["text"][1:] if (row["text"][0] != '.' and is_number(row["text"][0]) == False and is_number(row["text"][1:]) == True)
                                    else row["text"], axis=1)
        except: print('Is somethings before number not work')

        df['digit'] = [is_number(word) for word in df['text']]
        if not "total" in list(df['text']):
            df = elimination_des_mots_parasites(df)
            total = list_chiffre_a_droite(image,df)
        else:
            print("mot total trouvé")
            if (search_total(df) == '0'):
                df = elimination_des_mots_parasites(df)
                total = list_chiffre_a_droite(image,df)
            else:
                total = search_total(df)
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
        text.append(str(line[1][0]))
    d = {"top": top, "left": left, "height": height, "width": width, "conf": conf, "text": text}
    df = pd.DataFrame(d)
    return df

def find_text_on_the_same_line (top, text, df):
    df = df[(df['top'] > top-3) & (df['top'] < top+3) & (df['text'] != text)]
    return list(df['text'])

def search_total(df):
    try:
        total = '0'
        df_not_digit = df[(df['digit'] == False)]
        df_digit = df[(df['digit'] == True)]
        df_digit["list"] = df_digit.apply(lambda row: find_text_on_the_same_line(row["top"],row["text"], df_not_digit) ,axis=1)
        df_digit["total_word"] = df_digit.apply(lambda row: True if "total" in row["list"] else False ,axis=1)
        df_digit = df_digit[(df_digit['total_word'] == True)]
        total = select_le_plus_grand_chiffre(df_digit[(df_digit['conf'] > "55")])
        print(df_digit[['top', 'left', 'height', 'conf', 'text', 'list']])
    except Exception:
        print("error function - search_total")
    return total

def mot_parasites (list):
    presence = False
    liste_parasite = ['change','charge','check','discout','fee','gratuity','guests','item','order','other','received',
                      'sale','service','subtotal','sub','tax','taxable','tva','tip','ticket','table','%','#']
    for i in range (len(liste_parasite)):
        if (liste_parasite[i] in list):
            presence = True
            break
    return presence

def elimination_des_mots_parasites(df):
    try:
        print("elimination_des_mots_parasites")
        df_not_digit = df[(df['digit'] == False)]
        df_digit = df[(df['digit'] == True)]
        df_digit["list"] = df_digit.apply(lambda row: find_text_on_the_same_line(row["top"],row["text"], df_not_digit) ,axis=1)
        df_digit["total_word"] = df_digit.apply(lambda row: mot_parasites(row["list"]),axis=1)
        df_digit = df_digit[(df_digit['total_word'] == False)]
        print(df_digit)
    except Exception:
        print("error function - elimination_des_mots_parasites")
    return df_digit

def list_chiffre_a_droite(image,df):
    left = int(image.shape[1]/3)
    top = int(image.shape[0]/4)
    df = df[(df['text'] != "") & (df['left'] > left) & (df['top'] > top) & (df['digit'] == True)]
    total = select_le_plus_grand_chiffre(df[(df['conf'] > "75")])
    print(df[['top','left','height','conf','text']])
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
        df = df[(df['text'] < 40000) & (df['height'] >= moyenne_hauteur-1)]
        df = df.sort_values(by=['text'], ascending=False)
        print('select_le_plus_grand_chiffre')
        print(df)
        if (len(df) > 0) :
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
        if (a < b +4 and a > b -4 and a1 < b1 + 3 and a1 > b1 -3):
            if "." not in a2 and "." not in b2 or "." in a2 and "." not in b2 or "." not in a2 and "." in b2:
                DF = df[(df['top'] != a) & (df['height'] != a1) & (df['top'] != b) & (df['height'] != b1)]
                df_new_line = pd.DataFrame([[int((a1+b1)/2), float(str(b2)+str(a2))]], columns=['height', 'text'])
                DF = pd.concat([DF, df_new_line], ignore_index=True)
        b = a
        b1 = a1
        b2=a2
    return DF

# BALENCE DUE + PAYEMENT