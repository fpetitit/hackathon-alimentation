import pandas as pd

CODE_TOMATE=7020000
KEEPING_COLUMNS_NAME = ["flux", "annee", "nc8_code", "pays", "valeur_euro", "masse_kg",]
PAYS_COLUMNS_NAME = ["code", "pays", "codea", "codeb"]
PAYS_COLUMNS_TYPES = {
    "code":"string",
    "pays":"string",
}
NC8_COLUMNS_NAME = ["code", "nc8", "usup", "pusup", "debut", "fin"]
NC8_COLUMNS_TYPES = {
    "code":"Int64",
    "nc8":"string",
    "usup":"string",
    "pusup":"string",
    "debut":"Int64",
    "fin":"Int64"
}
CPF6_COLUMNS_NAME = ["code", "cpf6", "codea", "codeb"]
CPF6_COLUMNS_TYPES = {
    "code":"string",
    "cpf6":"string"
}
A129_COLUMNS_NAME = ["code", "a129", "codea", "codeb"]
A129_COLUMNS_TYPES = {
    "code":"string",
    "a129":"string"
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

def read_data(path, col_names, col_types, sep=";", header=None, encoding="utf-8"):
    return pd.read_csv(path, sep=sep, names=col_names, dtype=col_types, header=header, encoding=encoding)
   
def get_data_per_year(year):
    df_a129 = read_data(
        "data/libelle_a129.txt", 
        col_names=A129_COLUMNS_NAME, 
        col_types=A129_COLUMNS_TYPES
        )
    df_cpf6 = read_data(
        "data/libelle_cpf6.txt", 
        col_names=CPF6_COLUMNS_NAME, 
        col_types=CPF6_COLUMNS_TYPES,
        encoding="latin-1"
        )
    df_nc8 = read_data(
        f"data/Libelle_NC8_20{year}.txt", 
        col_names=NC8_COLUMNS_NAME,
        col_types=NC8_COLUMNS_TYPES,
        header=0,
        encoding="latin-1"
    )
    df_pays = read_data(
        "data/libelle_pays.txt",
        col_names=PAYS_COLUMNS_NAME,
        col_types=PAYS_COLUMNS_TYPES
    )
    df = read_data(
        f"data/National_20{year}_Import.txt",
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
    return trunc_merged_df.groupby(["flux", "annee", "nc8_code", "pays"], as_index=False).sum()

def get_list_tomate_nat():
    df_final = pd.DataFrame()
    year_list = []
    for year in range(18,24):
        year_list.append(f"20{year}")
        df = get_data_per_year(year)
        df_final = pd.concat([df_final, df])
    print(df_final.columns)
    print(df_final)
    return df_final


if __name__ == "__main__":
    get_list_tomate_nat()

