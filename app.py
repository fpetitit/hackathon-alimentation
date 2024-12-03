import streamlit as st
from national_tomate import get_list_tomate_nat
from regional_tomate import get_list_tomate_dep
from conso_tomate import get_conso_tomatoes
import plotly.express as px 

import pandas as pd
from commerce_ext_tomate import read_data

st.header("Production et consommation de tomates")

# NATIONAL 
st.header("Importation et exportation nationale")

st.write("Importation totale des tomates en France")

df_nat = pd.read_csv(
    "data/export_import_national_2018_2023.csv", 
    sep=";",
    header=0
)

df_tot = df_nat.groupby(["flux", "annee", "nc8_code"], as_index=False).sum()
fig = px.line(df_tot, x="annee", y="masse_kg", color="flux")

st.plotly_chart(fig)


# CONSOMMATION 

st.header("Consommation de tomates étrangères en France")

def plot_quantities_by_country(df, label_col='label', quantity_col='quantite', title="Quantités par pays d'origine de 2013 à 2023"):
    df_grouped = df.groupby('pays', as_index=False)[quantity_col].sum()
    fig = px.bar(
        df_grouped,
        x='pays',
        y=quantity_col,
        title=title,
        labels={'pays': 'Pays', quantity_col: 'Quantité'},
        text=quantity_col,
        color='pays'
    )

    fig.update_layout(xaxis_title="Pays", yaxis_title="Quantité")
    st.plotly_chart(fig)

df_conso = get_conso_tomatoes()
plot_quantities_by_country(df_conso)

st.header("Consommation de tomates étrangères en France par an")

def plot_quantities_by_year_and_country(df, year_col='annee', country_col='pays', quantity_col='quantite', title="Quantités par année et par pays"):
    df_grouped = df.groupby([year_col, country_col], as_index=False)[quantity_col].sum()

    fig = px.line(
        df_grouped,
        x=year_col,
        y=quantity_col,
        color=country_col,
        markers=True,
        title=title,
        labels={year_col: 'Année', quantity_col: 'Quantité', country_col: 'Pays'}
    )

    fig.update_layout(
        xaxis_title="Année",
        yaxis_title="Quantité",
        legend_title="Pays",
        title_font_size=18
    )

    st.plotly_chart(fig)


plot_quantities_by_year_and_country(df_conso)