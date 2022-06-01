import pandas as pd

# ----------------------------------------------------------------------------------------------------------------------
#               Liste de mots
# ----------------------------------------------------------------------------------------------------------------------

liste_total = ['total', 'totale', 'tot', 'tota', 'otal', 'totl', 'due', 'amt', 'amount', 'amoun', 'amont', 'balance']

liste_parasite = ['account', 'caisse', 'change', 'charge', 'check', 'code', 'date', 'discout', 'fee', 'gratuity',
                  'gratuit', 'guests', 'id', 'item', 'monnaie', 'no', 'num', 'number', 'numero', 'order', 'other',
                  'received', 'receipt', 'ref', 'reference', 'rendu', 'sale', 'sales', 'service', 'sous', 'sos',
                  'soustotal', 'subtotal', 'sub-total', 'sb', 'sub', 'tax', 'taxe', 'taxable', 'terminal', 'tva',
                  'tip', 'ticket', 'table', 'vat', '%', '#']


# ----------------------------------------------------------------------------------------------------------------------
#               Nettoyage
# ----------------------------------------------------------------------------------------------------------------------

def clean_df(df):
    df = df[["top", "left", "height", "width", "conf", "text"]]
    df['text'] = df['text'].astype(str).str.lower()
    df.text = df.text.str.replace(',', '.')
    df.text = df.text.str.replace('[$,¥,€,\',",«,»]', '')
    # df.text = df.text.str.replace('[;,:,=,-]', ' ')
    df["text"] = df.apply(lambda row: "%" if '%' in row["text"] else row["text"], axis=1)
    df["text"] = df.apply(lambda row: "#" if '#' in row["text"] else row["text"], axis=1)
    df = df[(df['text'] != "") & (df['text'] != " ") & (df['conf'] > "10")]

    print(list(df['text']))
    if not df.empty:
        DF = pd.DataFrame()
        for index, row in df.iterrows():
            liste_text = row['text'].split()
            for i in range(len(liste_text)):
                row_add = pd.Series([row['top'], row['left'], row['height'], row['width'], row['conf'], liste_text[i]],
                                    index=df.columns)
                DF = DF.append(row_add, ignore_index=True)
        df = DF.copy()
    # Is somethings before number - S'il y a un caractère devant un chiffre alors on l'enleve car il s'agit probablement d'un "$" mal lu
    try:
        df["text"] = df.apply(lambda row: row["text"][1:] if (
                row["text"][0] != '.' and is_number(row["text"][0]) == False and is_number(row["text"][1:]) == True)
        else row["text"], axis=1)
    except:
        print('Is somethings before number not work')

    # Is somethings after number - S'il y a un caractère après un chiffre alors on l'enleve car il s'agit probablement d'un "E" mal lu
    try:
        df["text"] = df.apply(lambda row: row["text"][:-1] if (
                row["text"][-1] != '.' and is_number(row["text"][-1]) == False and is_number(
            row["text"][:-1]) == True)
        else row["text"], axis=1)
    except:
        print('Is somethings after number not work')

    if not df.empty:
        df['digit'] = [is_number(word) for word in df['text']]
        df["diff"] = [count_difference_between_word(word, 'total') for word in df['text']]
        df["text"] = df.apply(lambda row: 'total' if (row["diff"] <= 1) else row["text"], axis=1)
    return df


# ----------------------------------------------------------------------------------------------------------------------
#               Mots parasites
# ----------------------------------------------------------------------------------------------------------------------

def mot_parasites(list):
    presence = False
    for i in range(len(liste_parasite)):
        if liste_parasite[i] in list:
            presence = True
            break
    return presence


def elimination_des_mots_parasites(df):
    try:
        df_not_digit = df[(df['digit'] == False)]
        df_digit = df[(df['digit'] == True)]
        df_digit["list"] = df_digit.apply(lambda row: find_text_on_the_same_line(row["top"], row["text"], df_not_digit),
                                          axis=1)
        df_digit["parasites_word"] = df_digit.apply(lambda row: mot_parasites(row["list"]), axis=1)
        df_digit = df_digit[(df_digit['parasites_word'] == False)]
    except Exception:
        df_digit = df.copy()
        print("error function - elimination_des_mots_parasites")
    return df_digit


# ----------------------------------------------------------------------------------------------------------------------
#               Format chiffre
# ----------------------------------------------------------------------------------------------------------------------

def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def format_chiffre_(chiffre):  # xx.xx
    try:
        if chiffre[-3] == '.' and len(chiffre) >= 4:
            return True
        else:
            return False
    except Exception:
        return False


def format_chiffre(df):
    try:
        df["format"] = df.apply(lambda row: format_chiffre_(row["text"]), axis=1)
        df = df[(df['format'] == True)]
    except Exception:
        print('error - format chiffre')
    return df


# ----------------------------------------------------------------------------------------------------------------------
#               Autres fonctions
# ----------------------------------------------------------------------------------------------------------------------

def count_difference_between_word(a, b):
    zipped = zip(a, b)
    difference = sum(1 for e in zipped if e[0] != e[1])
    difference = difference + abs(
        len(a) - len(b))  # si les 2 chaînes sont de longueur différente -> ajoute la différence de longueur
    return difference


def find_text_on_the_same_line(top, text, df):
    df = df[(df['top'] >= top - 10) & (df['top'] <= top + 10) & (df['text'] != text)]
    return list(df['text'])


def mot_total(list):
    presence = False
    for i in range(len(liste_total)):
        if liste_total[i] in list:
            presence = True
            break
    return presence


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
        if b + 6 > a > b - 6 and b1 + 1 > a1 > b1 - 1:
            if "." not in a2 and "." not in b2 or "." in a2 and "." not in b2 or "." not in a2 and "." in b2:
                DF = df[(df['top'] != a) & (df['height'] != a1) & (df['top'] != b) & (df['height'] != b1)]
                df_new_line = pd.DataFrame([[int((a1 + b1) / 2), float(str(b2) + str(a2))]], columns=['height', 'text'])
                DF = pd.concat([DF, df_new_line], ignore_index=True)
        b = a
        b1 = a1
        b2 = a2
    return DF
