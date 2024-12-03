

import pandas as pd

PAYS_COLUMNS_NAME = ["code", "pays", "codea", "codeb"]
PAYS_COLUMNS_TYPES = {
    "code":"string",
    "pays":"string",
}
DEP_COLUMNS_NAME = ["dep_code", "departement", "region_code", "region"]
DEP_COLUMNS_TYPES = {
    "dep_code":"string",
    "departement":"string",
    "region_code":"string",
    "region":"string"
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
CPF4_COLUMNS_NAME = ["code", "cpf4", "codea", "codeb"]
CPF4_COLUMNS_TYPES = {
    "code":"Int64",
    "cpf4":"string"
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

def read_data(*args, path, col_names=[], col_types={}, sep=";", header=None, encoding="utf-8"):
    if args : 
        return pd.read_csv(path, sep=sep, names=col_names, dtype=col_types, header=header, encoding=encoding, usecols=args[0])
    else:
        return pd.read_csv(path, sep=sep, names=col_names, dtype=col_types, header=header, encoding=encoding)
   
def get_data_libelle():
    df_pays = read_data(
        path="douane_data/libelle_pays.txt",
        col_names=PAYS_COLUMNS_NAME,
        col_types=PAYS_COLUMNS_TYPES,
        encoding="utf-8"
    )
    df_dep = read_data(
        path="douane_data/Departement_region.txt",
        col_names=DEP_COLUMNS_NAME,
        col_types=DEP_COLUMNS_TYPES
    )
    df_a129 = read_data(
        path="douane_data/libelle_a129.txt", 
        col_names=A129_COLUMNS_NAME, 
        col_types=A129_COLUMNS_TYPES
    )
    df_cpf6 = read_data(
        path="douane_data/libelle_cpf6.txt", 
        col_names=CPF6_COLUMNS_NAME, 
        col_types=CPF6_COLUMNS_TYPES,
        encoding="latin-1"
        )
    df_cpf4 = read_data(
        path="douane_data/libelle_cpf4.txt", 
        col_names=CPF4_COLUMNS_NAME, 
        col_types=CPF4_COLUMNS_TYPES,
        encoding="latin-1"
    )
    return df_pays, df_dep, df_a129, df_cpf6, df_cpf4
    