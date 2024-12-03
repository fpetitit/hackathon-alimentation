import pandas as pd 

def loading_product_data():
  d = {'annee': [2018,2019, 2020, 2021, 2022],
       'quantite': [684509, 667421, 615095, 701123, 677814]}
  product = pd.DataFrame(data=d)
  return product