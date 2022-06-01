import pandas as pd
import ocr
from traitement_text import clean_df, liste_total, elimination_des_mots_parasites, format_chiffre, mot_total


def displayTextDf(df_pytes, df_padd):
    print('---- df_pytes ----')
    print(list(df_pytes['text']))
    print('---- df_padd ----')
    print(list(df_padd['text']))


# ----------------------------------------------------------------------------------------------------------------------
#               Combine les 2 ocr pour une meilleurz efficacité
# ----------------------------------------------------------------------------------------------------------------------

def affiche_total(image):
    df_pytes = ocr.df_pytesseract(image)
    df_padd = ocr.df_paddle(image)
    total = '0'
    displayTextDf(df_pytes, df_padd)
    synonyme_total_trouver = False

    # --- Si les 2 ocr trouvent des écritures ---
    if df_padd.empty == False and df_pytes.empty == False:
        df_pytes = clean_df(df_pytes)
        df_padd = clean_df(df_padd)
        # displayTextDf(df_pytes, df_padd)
    if df_padd.empty == False and df_pytes.empty == False:
        for i in range(len(liste_total)):
            if liste_total[i] in list(df_padd['text']):
                total = search_total(df_padd)
                synonyme_total_trouver = True
                break
        if not synonyme_total_trouver:
            for i in range(len(liste_total)):
                if liste_total[i] in list(df_pytes['text']):
                    total = search_total(df_pytes)
                    break
        if total == '0':
            df_padd = elimination_des_mots_parasites(df_padd)
            total = list_chiffre_a_droite(image, df_padd)
        if total == '0':
            df_pytes = elimination_des_mots_parasites(df_pytes)
            total = list_chiffre_a_droite(image, df_pytes)
    else:
        displayTextDf(df_pytes, df_padd)
        if not df_padd.empty:
            df_padd = clean_df(df_padd)
            if not df_padd.empty:
                for i in range(len(liste_total)):
                    if liste_total[i] in list(df_padd['text']):
                        total = search_total(df_padd)
                        break
                if total == '0':
                    df_padd = elimination_des_mots_parasites(df_padd)
                    total = list_chiffre_a_droite(image, df_padd)
        if df_pytes.empty == False and total == '0':
            df_pytes = clean_df(df_pytes)
            if not df_pytes.empty:
                for i in range(len(liste_total)):
                    if liste_total[i] in list(df_pytes['text']):
                        total = search_total(df_pytes)
                        break
                if total == '0':
                    df_pytes = elimination_des_mots_parasites(df_pytes)
                    total = list_chiffre_a_droite(image, df_pytes)
    return total


# ----------------------------------------------------------------------------------------------------------------------
#               Cherche le mot "total"
# ----------------------------------------------------------------------------------------------------------------------

def search_total(df):
    try:
        total = '0'
        df_not_digit = df[(df['digit'] == False)]
        df_digit = elimination_des_mots_parasites(df)

        df_digit["total_word"] = df_digit.apply(lambda row: mot_total(row["list"]), axis=1)
        df_digit = df_digit[(df_digit['total_word'] == True)]

        df_not_digit["total_word"] = df_not_digit.apply(lambda row: True if row["text"] in liste_total else False,
                                                        axis=1)
        df_not_digit = df_not_digit[(df_not_digit['total_word'] == True)]

        left = min(list(df_not_digit['left']))
        df_digit = df_digit[(df_digit['left'] >= left)]
        total = select_le_plus_grand_chiffre(df_digit)

        # print(df_digit[['top', 'left', 'height', 'conf', 'text', 'list']])
    except Exception:
        print("error function - search_total")
    return total


# ----------------------------------------------------------------------------------------------------------------------
#               Cherche les chiffres ce trouvant en bas à droite de l'image
# ----------------------------------------------------------------------------------------------------------------------

def list_chiffre_a_droite(image, df):
    left = int(image.shape[1] / 2)
    top = int(image.shape[0] / 3)
    df = df[(df['text'] != "") & (df['left'] > left) & (df['top'] > top) & (df['digit'] == True)]
    df = format_chiffre(df)
    # print(df[['top', 'left', 'height', 'conf', 'text', 'list']])
    total = select_le_plus_grand_chiffre(df[(df['conf'] > "80")])
    return total


# ----------------------------------------------------------------------------------------------------------------------
#               Selection final
# ----------------------------------------------------------------------------------------------------------------------

def select_le_plus_grand_chiffre(df):
    total = '0'
    if len(df) == 1:
        df = df[df['text'].notnull()].copy()
        df['text'] = df['text'].astype(float)
        df = df[(df['text'] < 40000)]
        total = list(df['text'])[0]
    elif len(df) > 1:
        df = df[df['text'].notnull()].copy()
        df['text'] = df['text'].astype(float)
        # moyenne_hauteur = df.height.mean()
        df = df[(df['text'] < 40000)]  # (df['height'] >= moyenne_hauteur-1)
        df = df.sort_values(by=['text'], ascending=False)
        if len(df) > 0: total = list(df['text'])[0]
    else:
        print("Liste vide - Pas de total trouvé")
    return total
