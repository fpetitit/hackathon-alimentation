import re
import pandas as pd
import zipfile

PATH_KANTAR = "data/kantar_data_simplified.csv.zip"
YEAR_START = 2013
YEAR_END = 2023
AGE_GROUPS = [
            '65 ANS ET PLUS', 'DE 35 A 49 ANS', 'DE 50 A 64 ANS',
            'MOINS DE 35 ANS', 'ADO 16-19 ANS MAX', 'ADO 20-24 ANS MAX',
            'ENF 0-5 ANS MAX', 'ENF 11-15 ANS MAX', 'ENF 6-10 ANS MAX'
        ]
        
SEARCH_TERM_TOMATOES = r'^[Tt]omate.*$'

COUNTRY = ['BELGIQUE', 'ESPAGNE', 'HOLLANDE', 'ITALIE', 'MAROC', 'ORIGINE']
LABEL_COLUMN_NAME = 'label'

def extract_country(LABEL_COLUMN_NAME):
    for country in COUNTRY:
        if country in LABEL_COLUMN_NAME:
            return country
    return 'FRANCE'

def loading_kantar_data() :
  with zipfile.ZipFile(PATH_KANTAR, "r") as f:
      with f.open(f.namelist()[0]) as zd:
          df = pd.read_csv(zd, encoding='latin-1', low_memory=False)
          return df

def cleaning_kantar_data(df, YEAR_START = 2013 , YEAR_END = 2023, age_groups=AGE_GROUPS):
  df = df.rename(columns={'Libellé_Court': 'label', 'Q_ach' : 'quantite'})
  df = df[(df.annee >= YEAR_START) & (df.annee <= YEAR_END)]
  df = df[df['geog'].isin(AGE_GROUPS)]
  return df

def find_term(df,search_term = SEARCH_TERM_TOMATOES ):
  resultats = df[df[LABEL_COLUMN_NAME].str.contains(search_term, flags=re.IGNORECASE, na=False)]
  return resultats

def clean_label(df, remplace_underscore=True, supprime_non_bio=True, remplace_espaces=True, supprime_espace_fin=True):
    if remplace_underscore:
        df.loc[:, LABEL_COLUMN_NAME] = df[LABEL_COLUMN_NAME].str.replace('_', ' ', regex=False)

    if supprime_non_bio:
        df.loc[:, LABEL_COLUMN_NAME] = df[LABEL_COLUMN_NAME].str.replace('NON BIO', '', regex=False)

    if remplace_espaces:
        df.loc[:, LABEL_COLUMN_NAME] = df[LABEL_COLUMN_NAME].str.replace(r'\s{2,}', ' ', regex=True)

    if supprime_espace_fin:
        df.loc[:, LABEL_COLUMN_NAME] = df[LABEL_COLUMN_NAME].str.rstrip()

    return df

#def split_bio(df, colonne='label'):
#    df['BIO'] = df[colonne].apply(lambda x: 'BIO' if 'BIO' in str(x).upper() else 'NON BIO')
#    return df

def get_conso_tomatoes(): 
    df  = loading_kantar_data()
    #df = cleaning_kantar_data(df)
    #df = find_term(df)
    #df = clean_label(df)
    #df['pays'] = df[LABEL_COLUMN_NAME].apply(extract_country)
    #df['pays'] = df['pays'].replace('ORIGINE', 'AUTRE ORIGINE')
    return df 
   

if __name__ == "__main__":
    get_conso_tomatoes()