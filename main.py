import imgutils
import cv2
import matplotlib.pyplot as plt
import extraction_silhouette
import contours_image
import part3
import pandas as pd

path = "data/sample.jpg" #34 #60 ---- 84

# marche :) -> sample, 1167, 1136, 1138, 1141, 1143, 1145
# marche pas -> 1134, 1135, 1137, 1139, 1140, 1144, 1146, 1147, 1148
# 1191 -> ticket très dur car présence de pourboire

# camille -> 1132, 1146, 1147, 1163
# pb de cadre : 1134


def main(path, display_image):

    ###### début 2.2

    base, image = extraction_silhouette.silhouette(path)

    #imgutils.plot_gray(image)
    #plt.show()

    ####### début 2.3

    img_contours, contours = contours_image.extraction_contour(image, base)
    if (display_image == True) : imgutils.affiche(img_contours)
    list = contours_image.ten_contours(contours)

    img_large_contours = cv2.drawContours(base.copy(), list, -1, (255, 0, 0), 3)

    if (display_image == True) : imgutils.affiche(img_large_contours)
    rect =imgutils.get_receipt_contour(list)

    if (contours_image.si_image_bien_cadre (image,contours) == True): # si cadre taille normal alors on recadre l'image

        rect =imgutils.get_receipt_contour(list)

        img_rect = cv2.drawContours(base.copy(), rect, -1, (0, 255, 0), 3)

        if (display_image == True) : imgutils.affiche(img_rect)

        #######2.4

        img_redresse = imgutils.wrap_perspective(base.copy(), imgutils.contour_to_rect(rect))

        img_scan = imgutils.bw_scanner(img_redresse)
        if (display_image == True) : imgutils.affiche(img_scan)

        total = part3.affiche_total(img_scan)
        if (display_image == True) : part3.affiche_rectangle('Facture', img_scan, (0, 255, 0), 2)

    else: # si cadre trop petit alors on ne recadre pas l'image
        img_scan = imgutils.bw_scanner(cv2.imread(path))
        total = part3.affiche_total(img_scan)
        if (display_image == True) : part3.affiche_rectangle('Facture', img_scan, (0, 255, 0), 2)

    return total

def table_comparaison():
    df = pd.read_csv("table_de_verification.csv", sep=';')
    for i in range (len(df)):
        num = df.loc[i,'numero']
        print(num)
        total = main("data/" + str(num) +"-receipt.jpg", False)
        df.loc[i, 'total_obtenu'] = total
    df["result"] = df.apply(lambda row: True if float(row["total"]) == float(row["total_obtenu"]) else False, axis = 1)
    print(df)
    print(df['result'].value_counts())

print("LE TOTAL EST : ", main(path, True))
#table_comparaison()
