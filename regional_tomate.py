

import pandas as pd

CODE_TOMATE=7020000
KEEPING_COLUMNS_NAME = ["flux", "trimestre", "annee", "departement", "region", "cpf4_code", "cpf4", "pays", "valeur_euro", "masse_kg",]
GROUPBY_COLUMNS_NAME = ["flux", "trimestre", "annee", "departement", "region", "cpf4_code", "cpf4", "pays"]
PAYS_COLUMNS_NAME = ["code", "pays", "codea", "codeb"]
PAYS_COLUMNS_TYPES = {
    "code":"string",
    "pays":"string",
}
DEP_COLUMNS_NAME = ["dep_code", "departement", "region_code", "region"]
DEP_COLUMNS_TYPES = {
    "dep_code":"string",
    "departement":"string",
    "region_code":"Int64",
    "region":"string"
}
CPF4_COLUMNS_NAME = ["code", "cpf4", "codea", "codeb"]
CPF4_COLUMNS_TYPES = {
    "code":"Int64",
    "cpf4":"string"
}
A129_COLUMNS_NAME = ["code", "a129", "codea", "codeb"]
A129_COLUMNS_TYPES = {
    "code":"string",
    "a129":"string"
}
DATA_COLUMNS_NAME = ["flux", "trimestre", "annee", "dep_code", "region_code", "cpf4_code", "a129_code", "pays_code", "valeur_euro", "masse_kg",]
DATA_COLUMNS_TYPES = {
    "flux" : "string", 
    "trimestre" : "Int64",
    "annee" : "Int64",
    "dep_code" : "string",
    "region_code" : "Int64",
    "cpf4_code" : "Int64",
    "a129_code" : "string",
    "pays_code" : "string",
    "valeur_euro" : "Int64",
    "masse_kg" : "Int64"
}

def read_data(path, col_names, col_types, sep=";", header=None, encoding="utf-8"):
    return pd.read_csv(path, sep=sep, names=col_names, dtype=col_types, header=header, encoding=encoding)
   
def get_data_per_year(year):
    df_a129 = read_data(
        "data/libelle_a129.txt", 
        col_names=A129_COLUMNS_NAME, 
        col_types=A129_COLUMNS_TYPES
    )
    df_cpf4 = read_data(
        "data/libelle_cpf4.txt", 
        col_names=CPF4_COLUMNS_NAME, 
        col_types=CPF4_COLUMNS_TYPES,
        encoding="latin-1"
    )
    df_pays = read_data(
        "data/libelle_pays.txt",
        col_names=PAYS_COLUMNS_NAME,
        col_types=PAYS_COLUMNS_TYPES,
        encoding="utf-8"
    )
    df_dep = read_data(
        "data/Departement_region.txt",
        col_names=DEP_COLUMNS_NAME,
        col_types=DEP_COLUMNS_TYPES
    )
    df = read_data(
        f"data/Regional_20{year}_Import.txt",
        col_names=DATA_COLUMNS_NAME,
        col_types=DATA_COLUMNS_TYPES
    )

    # print("filtering on tomatoe code...")
    # df_on_code = df[df["cpf4_code"]==CODE_TOMATE]

    print("merging df...")
    merged_df = df.merge(
            df_pays, how="left", left_on="pays_code", right_on="code",  suffixes=("x", "_pays")
        ).merge(
            df_dep, how="left", on="dep_code",  suffixes=("xxxx", "_nc8")
        ).merge(
            df_cpf4, how="left", left_on="cpf4_code", right_on="code",  suffixes=("xx", "_cpf4")
        ).merge(
            df_a129, how="left", left_on="a129_code", right_on="code",  suffixes=("xxx", "_a129")
        )
    
    trunc_merged_df = merged_df[KEEPING_COLUMNS_NAME]
    return trunc_merged_df.groupby(GROUPBY_COLUMNS_NAME, as_index=False).sum()

def get_list_tomate_dep():
    df_final = pd.DataFrame()
    year_list = []
    for year in range(21,22):
        year_list.append(f"20{year}")
        df = get_data_per_year(year)
        df_final = pd.concat([df_final, df])
    print(df_final.columns)
    print(df_final)
    return df_final


if __name__ == "__main__":
    df=get_list_tomate_dep()
    print(df)
