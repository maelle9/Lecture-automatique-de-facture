import imgutils
import cv2
import matplotlib.pyplot as plt
import extraction_silhouette
import contours_image
import part3

###### début 2.2

path_sample = "data/1143-receipt.jpg" #34 #60 ---- 84

# marche :) -> sample, 1167, 1136, 1138, 1141, 1145, 1143
# marche pas -> 1135, 1137, 1140
# marche pas car pb trait -> 1134, 1139, 1144

base, image = extraction_silhouette.silhouette(path_sample)

#imgutils.plot_gray(image)
#plt.show()

#######début 2.3

img_contours, contours = contours_image.extraction_contour(image, base)

imgutils.affiche(img_contours)

list = contours_image.ten_contours(contours)


img_large_contours = cv2.drawContours(base.copy(), list, -1, (255, 0, 0), 3)

imgutils.affiche(img_large_contours)
rect =imgutils.get_receipt_contour(list)

if (contours_image.si_image_bien_cadre (image,contours) == True):
    rect =imgutils.get_receipt_contour(list)

    img_rect = cv2.drawContours(base.copy(), rect, -1, (0, 255, 0), 3)

    imgutils.affiche(img_rect)


    #######2.4

    img_redresse = imgutils.wrap_perspective(base.copy(), imgutils.contour_to_rect(rect))

    img_scan = imgutils.bw_scanner(img_redresse)
    imgutils.affiche(img_scan)


    part3.affiche_total(img_scan)
    part3.affiche_rectangle('Facture', img_scan, (0, 255, 0), 2)

else:
    img_scan = imgutils.bw_scanner(cv2.imread(path_sample))
    part3.affiche_total(img_scan)
    part3.affiche_rectangle('Facture', img_scan, (0, 255, 0), 2)
