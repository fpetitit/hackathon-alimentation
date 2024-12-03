import pandas as pd 

def loading_product_data():
  return pd.read_csv("data/agreste_prod_tomate.csv", sep=";")

def get_prod_tomate():
     years = [str(i) for i in range(2010,2024)]
     col = ["pays", "Production de tomates frais et industrie en tonnes*10"] + years
     df = pd.read_excel("agreste/2024-11-22 22_31_46 SAA_2010-2023_definitives_donnees_regionales_AGRESTE.xlsx", sheet_name="LEG", skiprows=46, nrows=1, header=None, names=col, usecols="A,B,AE:AR")
     df_melted = pd.melt(df, id_vars=["pays", "Production de tomates frais et industrie en tonnes*10"], value_vars=years, var_name="annee", value_name="masse_100kg")
     df_melted["annee"] = df_melted["annee"].apply(lambda x: int(x))
     df_melted["masse_tonne"] = df_melted["masse_100kg"].apply(lambda x: int(x/10)) # en 100kg donc *100/1000 tonne
     df_final = df_melted[["annee", "masse_tonne"]]
     return df_final.to_csv("agreste_prod_tomate.csv", index=False, sep=";")

if __name__ == "__main__":
    get_prod_tomate()