

import pandas as pd
from commerce_ext_tomate import get_data_libelle, read_data

CODE_TOMATE=7020000
KEEPING_COLUMNS_NAME = ["flux", "annee", "nc8_code", "pays", "valeur_euro", "masse_kg",]

NC8_COLUMNS_NAME = ["code", "nc8", "usup", "pusup", "debut", "fin"]
NC8_COLUMNS_TYPES = {
    "code":"Int64",
    "nc8":"string",
    "usup":"string",
    "pusup":"string",
    "debut":"Int64",
    "fin":"Int64"
}

DATA_COLUMNS_NAME = ["flux", "mois", "annee", "cpf6_code", "a129_code", "nc8_code", "pays_code", "valeur_euro", "masse_kg","usup",]
DATA_COLUMNS_TYPES = {
    "flux" : "string", 
    "mois" : "Int64",
    "annee" : "Int64",
    "cpf6_code" : "string",
    "a129_code" : "string",
    "nc8_code" : "Int64",
    "pays_code" : "string",
    "valeur_euro" : "Int64",
    "masse_kg" : "Int64",
    "usup" : "Int64"
}
   
def get_data_per_year(year, flux):
    df_pays, _, df_a129, df_cpf6, _ = get_data_libelle()
    df_nc8 = read_data(
        path=f"data/Libelle_NC8_20{year}.txt", 
        col_names=NC8_COLUMNS_NAME,
        col_types=NC8_COLUMNS_TYPES,
        header=0,
        encoding="latin-1"
    )
    df = read_data(
        path=f"data/National_20{year}_{flux}.txt",
        col_names=DATA_COLUMNS_NAME,
        col_types=DATA_COLUMNS_TYPES
    )

    print("filtering on tomatoe code...")
    df_on_code = df[df["nc8_code"]==CODE_TOMATE]

    print("merging df...")
    merged_df = df_on_code.merge(
            df_pays, how="left", left_on="pays_code", right_on="code",  suffixes=("x", "_pays")
        ).merge(
            df_cpf6, how="left", left_on="cpf6_code", right_on="code",  suffixes=("xx", "_cpf6")
        ).merge(
            df_a129, how="left", left_on="a129_code", right_on="code",  suffixes=("xxx", "_a129")
        ).merge(
            df_nc8, how="left", left_on="nc8_code", right_on="code",  suffixes=("xxxx", "_nc8")
        )
    
    trunc_merged_df = merged_df[KEEPING_COLUMNS_NAME]
    return trunc_merged_df

def get_list_tomate_nat(flux):
    df_final = pd.DataFrame()
    year_list = []
    for year in range(18,24):
        year_list.append(f"20{year}")
        df = get_data_per_year(year, flux)
        df_final = pd.concat([df_final, df])
    return df_final

if __name__ == "__main__":
    df_nat_e = get_list_tomate_nat("Export")
    df_nat_i = get_list_tomate_nat("Import")
    df_nat = pd.concat([df_nat_e, df_nat_i])
    df_nat.to_csv("data/export_import_national_2018_2023.csv", sep=";", index=False)

