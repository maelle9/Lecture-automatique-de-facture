import cv2
import pandas as pd


def extraction_contour(silhouette,source):
    contours, hierarchy = cv2.findContours(silhouette, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = cv2.drawContours(source.copy(), contours, -1, (0, 255, 0), 3)
    return img_contours, contours

def list_area(list):
    area = []
    for i in range(len(list)):
        area_contours = cv2.contourArea(list[i])
        area.append(area_contours)
    return area

def ten_contours(contours):
    area_list = list_area(contours)
    index = []
    for i in range(len(contours)):
        index.append(i)
    df = pd.DataFrame({'index': index, 'area': area_list})
    df_sorted = df.sort_values(by=['area'], ascending=False)
    list_index = df_sorted['index'].head(10)
    list_contours = []
    for i in list_index:
        list_contours.append(contours[i])
    return list_contours