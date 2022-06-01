import time
import imgutils
import cv2
import contours_image
import pandas as pd
import traitement_image
import ocr
from find_total_amount import affiche_total


def main(path, display_image):
    # silhouette
    base, image = traitement_image.silhouette(path)
    if display_image: imgutils.affiche(image)

    # extraction_contour
    img_contours, contours = contours_image.extraction_contour(image, base)
    if display_image: imgutils.affiche(img_contours)

    # ten_contours
    list = contours_image.ten_contours(contours)
    img_large_contours = cv2.drawContours(base.copy(), list, -1, (255, 0, 0), 3)
    if display_image: imgutils.affiche(img_large_contours)

    # get_receipt_contour
    rect = imgutils.get_receipt_contour(list)
    img_rect = cv2.drawContours(base.copy(), rect, -1, (0, 255, 0), 3)
    if display_image: imgutils.affiche(img_rect)

    # ==================== Recadrage d'image ===========================
    # si cadre détecté > 3.5 * taille de l'image

    if contours_image.si_image_bien_cadre(image, contours):

        # wrap_perspective
        img_redresse = imgutils.wrap_perspective(base.copy(), imgutils.contour_to_rect(rect))
        if display_image: imgutils.affiche(img_redresse)

        image_final = traitement_image.traitement_apres_recadrage_2(img_redresse)
        # affiche_total
        total = affiche_total(image_final)
        if display_image: ocr.affiche_rectangle_paddle(image_final, (0, 255, 0), 2)

    # ==================== Pas de recadrage d'image ===========================
    # si cadre détecté < 3.5 * taille de l'image

    else:
        image_final = traitement_image.traitement_apres_recadrage_2(base)
        # --- lecture image ------
        total = affiche_total(image_final)
        if display_image: ocr.affiche_rectangle_paddle(image_final, (0, 255, 0), 2)

    return total

# ----------------------------------------------------------------------------------------------------------------------
#               Test le programme sur un dataset
# ----------------------------------------------------------------------------------------------------------------------

def table_comparaison():
    df = pd.read_csv("table/table_de_verification_dataset.csv", sep=';')
    for i in range(len(df)):
        num = df.loc[i, 'numero']
        print(num)
        try:
            total = main("dataset/" + str(num) + "-receipt.jpg", False)
            # total = main("data_2/" + str(num) +".jpg", False) #2
        except:
            total = '0'
        df.loc[i, 'total_obtenu'] = total
    df["result"] = df.apply(lambda row: True if float(row["total"]) == float(row["total_obtenu"]) else False, axis=1)
    count = df['result'].value_counts()
    vrai = len(df[df['result'] == True])
    print('pourcentage', (int(vrai) / len(df)) * 100)
    print(df)
    print(count)

# ----------------------------------------------------------------------------------------------------------------------
#               Chronomètre + Lancement fonction
# ----------------------------------------------------------------------------------------------------------------------

start = time.time()

#print("LE TOTAL EST : ", main("data/sample.jpg", True))
table_comparaison()

end = time.time()
executionTime = end - start
print('Temps d\'exécution : ', executionTime, ' s')
