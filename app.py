import streamlit as st
from national_tomate import get_list_tomate_nat
from regional_tomate import get_list_tomate_dep
import plotly.graph_objects as go
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