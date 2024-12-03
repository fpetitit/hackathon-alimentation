import streamlit as st
from national_tomate import get_list_tomate_nat
from regional_tomate import get_list_tomate_dep
from conso_tomate import get_conso_tomatoes
import plotly.express as px 


# NATIONAL

st.header("National")

df = get_list_tomate_nat()
fig_par_pays = px.line(df, x="annee", y="masse_kg", color="pays")

df = df.groupby(["flux", "annee", "nc8_code"], as_index=False).sum()
fig = px.line(df, x="annee", y="masse_kg")

st.plotly_chart(fig_par_pays)
st.plotly_chart(fig)


# REGIONAL
st.header("Regional")

df = get_list_tomate_dep()
fig_par_pays = px.line(df, x="annee", y="masse_kg", color=["pays", "departement"])


st.plotly_chart(fig_par_pays)

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