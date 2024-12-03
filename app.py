import streamlit as st
from national_tomate import get_list_tomate_nat
from regional_tomate import get_list_tomate_dep
from conso_tomate import get_conso_tomatoes
import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd
from commerce_ext_tomate import read_data
from production_tomate import loading_product_data


st.set_page_config( 
	layout="wide"
)

st.title("Analyse de la production et de la consommation de la tomate en France")
#st.header("Production et consommation de tomates")

# NATIONAL 
pays=["France", "Espagne", "Maroc", "Italie", "Pays-Bas"]

st.header("Importation et exportation nationale")

st.write("Importation totale des tomates en France")

df_ei = pd.read_csv(
    "data/export_import_national_2018_2023.csv", 
    sep=";",
    header=0
)
df_wo_ip=df_ei.loc[~df_ei["pays"].isin(["France", "Espagne", "Maroc", "Italie", "Pays-Bas", "Belgique"])].groupby(["flux", "annee", "nc8_code"], as_index=False).sum()
df_wo_ip["pays"]="Autre origine"

df_w_ip = df_ei.loc[df_ei["pays"].isin(["France", "Espagne", "Maroc", "Italie", "Pays-Bas", "Belgique"])]
df_w_ip["pays"].loc[df_w_ip["pays"]=="Pays-Bas"] = "Hollande"

df_nat = pd.concat([df_wo_ip, df_w_ip])
df_nat["pays"] = df_nat["pays"].apply(lambda x: x.upper())

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

    col1, col2 = st.columns([2,2])
    with col1 : 
        st.subheader("Consommation de tomates en France")
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
    
    with col2 : 
        st.subheader("Consommation de tomates en France par an")
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


    #lissa
    df_grouped.columns = ["annee", "pays", "masse_kg"]
    df_grouped["flux"] = "Consommation"
    df_f = (df_nat.loc[df_nat["flux"]=="I"].groupby(["flux", "annee", "nc8_code", "pays"], as_index=False).sum())[["annee", "pays", "masse_kg", "flux"]]
    df_mix = pd.concat([df_grouped, df_f])

    list_pays = set(df_mix["pays"])
    for pays in list_pays :
        st.subheader(f"Importation et consommation en France des tomates en provenance de {pays.lower()} ")
        col1, col2 = st.columns([2,2])
        with col1:
            fig_line = px.line(df_mix.loc[df_mix["pays"] == pays], x="annee", y="masse_kg", color="flux")
            st.plotly_chart(fig_line, use_container_width=True)
        with col2:
            fig_bar = px.bar(df_mix.loc[df_mix["pays"] == pays], x="annee", y="masse_kg", color="flux", barmode="group")
            st.plotly_chart(fig_bar, use_container_width=True)


plot_quantities_by_year_and_country(df_conso)

# Consommation vs production 

product = loading_product_data()
conso = df_conso[df_conso.pays == 'FRANCE'].groupby('annee')['quantite'].sum().reset_index()


col1, col2 = st.columns([2,2])
with col1:
    trace_bio = go.Scatter(
        x=conso['annee'],
        y=conso['quantite']/ 10000,
        mode='lines+markers',
        name="Consommation de tomates francaise en France",
        line=dict(color='blue'), 
    )

    trace_export = go.Scatter(
            x=product['annee'],
            y=product['masse_tonne'],
            mode='lines+markers',
            name="Production de tomates en France",
            line=dict(color='green'),
        )

    fig = go.Figure(data=[trace_bio, trace_export])

    fig.update_layout(
        title="Quantité de tomates consommée et produite en France par an",
        xaxis=dict(
            title="Année",
            tickmode='linear',  
            tick0=2018,         
            dtick=1             
        ),
        yaxis_title="Quantité",
        title_font_size=14
    )

    st.plotly_chart(fig)

with col2:
    df_export = df_nat[df_nat['flux'] == 'E']
    df_export = df_export.groupby(["annee"], as_index=False)['masse_kg'].sum()
    df_export['masse_tonnes'] = df_export['masse_kg'] / 1000


    df_export_product = product.merge(df_export, left_on='annee', right_on='annee')
    df_export_product['product_expo'] = df_export_product['masse_tonne'] - df_export_product['masse_tonnes']


    trace_conso = go.Scatter(
            x=conso['annee'],
            y=conso['quantite']/10000,
            mode='lines+markers',
            name="Consommation de tomates francaise en France",
            line=dict(color='blue'), 
        )

    trace_export_product = go.Scatter(
            x=df_export_product['annee'],
            y=df_export_product['product_expo'],
            mode='lines+markers',
            name="Production de tomates francaise pour la France métropolitaine",
            line=dict(color='green'),
        )

    fig = go.Figure(data=[trace_conso, trace_export_product])

    fig.update_layout(
        title="Quantité de tomates consommée vs production de tomates francaise pour la France métropolitaine",
        xaxis=dict(
            title="Année",
            tickmode='linear',  
            tick0=2018,         
            dtick=1             
        ),
        yaxis_title="Quantité",
        title_font_size=14
    )

    st.plotly_chart(fig)

### consommation au global 

conso_glob = pd.read_csv('data/fruit_veg_kantar_05_22.csv')
conso_glob_grouped = conso_glob.groupby(['annee'], as_index=False)['quantite'].sum()

fig = px.line(
            conso_glob_grouped,
            x='annee',
            y='quantite',
            markers=True,
            labels={'annee': 'Année', 'quantite': 'Quantité'}
        )

fig.update_layout(
            title = "Consommation de tomates en France de 2005 à 2023",
            xaxis_title="Année",
            yaxis_title="Quantité",
            title_font_size=18
        )

st.plotly_chart(fig)

st.markdown("""
### Sources :
- [DataDouane](https://lekiosque.finances.gouv.fr/site_fr/telechargement/telechargement_SGBD.asp)
- Kantar
- Rapport : Agreste - élaboration FranceAgriMer
""")
