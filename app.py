import streamlit as st
from national_tomate import get_list_tomate
import plotly.graph_objects as go
import plotly.express as px

df = get_list_tomate()
df = df.groupby(["flux", "annee", "nc8_code"], as_index=False).sum()

fig = px.line(df, x="annee", y="masse_kg")

st.plotly_chart(fig)

st.table(df)

st.write("Hello world")