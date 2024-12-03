

import pandas as pd
from commerce_ext_tomate import get_data_libelle, read_data

CODE_TOMATE_CPF4=113
KEEPING_COLUMNS_NAME = ["flux", "trim_annee", "departement", "region", "cpf4_code", "a129_code", "pays", "valeur_euro", "masse_kg",]

PAYS_COLUMNS_NAME = ["code", "pays", "codea", "codeb"]
PAYS_COLUMNS_TYPES = {
    "code":"string",
    "pays":"string",
}

DATA_COLUMNS_NAME = ["flux", "trimestre", "annee", "dep_code", "region_code",  "a129_code", "cpf4_code", "pays_code", "valeur_euro", "masse_kg",]
DATA_COLUMNS_TYPES = {
    "flux" : "string", 
    "trimestre" : "Int64",
    "annee" : "Int64",
    "dep_code" : "string",
    "region_code" : "string",
    "a129_code" : "string",
    "cpf4_code" : "Int64",
    "pays_code" : "string",
    "valeur_euro" : "Int64",
    "masse_kg" : "Int64"
}

def get_data_per_year(year, flux):
    df_pays, df_dep, df_a129, _, df_cpf4 = get_data_libelle()
    df = read_data(
        [0,1,2,3,4,5,6,7,8,9],
        path=f"data/Region_20{year}_{flux}.txt",
        col_names=DATA_COLUMNS_NAME,
        col_types=DATA_COLUMNS_TYPES
    )

    print("filtering on tomatoe code...")
    df_on_code = df[df["cpf4_code"]==CODE_TOMATE_CPF4]

    print("merging df...")
    merged_df = df_on_code.merge(
            df_pays, how="left", left_on="pays_code", right_on="code",  suffixes=("x", "_pays")
        ).merge(
            df_dep, how="left", on="dep_code",  suffixes=("xxxx", "_nc8")
        ).merge(
            df_cpf4, how="left", left_on="cpf4_code", right_on="code",  suffixes=("xx", "_cpf4")
        ).merge(
            df_a129, how="left", left_on="a129_code", right_on="code",  suffixes=("xxx", "_a129")
        )
    
    merged_df["trim_annee"] = merged_df.apply(lambda x:'%s_%s' % (x['annee'],x['trimestre']),axis=1)
    trunc_merged_df = merged_df[KEEPING_COLUMNS_NAME]
    return trunc_merged_df

def get_list_tomate_dep(flux):
    df_final = pd.DataFrame()
    year_list = []
    for year in range(21,23):
        year_list.append(f"20{year}")
        df = get_data_per_year(year, flux)
        df_final = pd.concat([df_final, df])
    return df_final


if __name__ == "__main__":
    df=get_list_tomate_dep("Import")
    print(df)
