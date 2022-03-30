""""
import imgutils
import pandas as pd
import cv2
import matplotlib.pyplot as plt


###### début 2.2

path = "data/sample.jpg"

src = cv2.imread(path)
Color = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
Resize = imgutils.opencv_resize(Color, 450 / Color.shape[0])
Blur = cv2.GaussianBlur(Resize,(3,3),0)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
Struct = cv2.dilate(Blur,kernel,iterations = 2)
image = cv2.Canny(Struct,100,100,apertureSize=3)
imgutils.plot_gray(image)
plt.show()


#######début 2.3

def list_area(list):
    area = []
    for i in range(len(list)):
        area_contours = cv2.contourArea(list[i])
        area.append(area_contours)
    return area

contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img_contours = cv2.drawContours(Resize.copy(), contours, -1, (0,255,0), 3)
imgutils.plot_rgb(img_contours)
plt.show()

area_list = list_area(contours)

index = []
for i in range (len(contours)):
    index.append(i)


df = pd.DataFrame({'index':index ,'area': area_list})

df_sorted = df.sort_values(by=['area'], ascending=False)


list_index = df_sorted['index'].head(10)

list_contours = []
for i in list_index:
    list_contours.append(contours[i])


img_large_contours = cv2.drawContours(Resize.copy(), list_contours, -1, (0, 255, 0), 3)
imgutils.plot_rgb(img_large_contours)
plt.show()

rect = imgutils.get_receipt_contour(list_contours)
img_rect = cv2.drawContours(Resize.copy(), rect, -1, (0, 255, 0), 3)
imgutils.plot_rgb(img_rect)
plt.show()

#######2.4

#######################code pour afficher coordonnées points sur image
font = cv2.FONT_HERSHEY_COMPLEX
n = rect.ravel()
i = 0

for j in n:
    if (i % 2 == 0):
        x = n[i]
        y = n[i + 1]

        string = str(x) + " " + str(y)

        if (i == 0):

            cv2.putText(base, "Arrow tip", (x, y),font, 0.5, (255, 0, 0))
        else:

            cv2.putText(base, string, (x, y), font, 0.5, (0, 255, 0))
    i = i + 1

cv2.imshow('image2', base)

if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()


### rajouter une bordure

bordersize = 5
border = cv2.copyMakeBorder(src, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize,
                                borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])
"""
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

