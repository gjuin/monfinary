import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Connexion sécurisée au Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Lecture des données
df_valo = conn.read(worksheet="data_valo")
df_mapping = conn.read(worksheet="mapping")

# Nettoyage rapide (ex: convertir les % en float)
df_mapping['Pourcentage'] = df_mapping['Pourcentage'].str.replace('%', '').astype(float) / 100

# La jointure "magique" comme en SQL ou R
df_final = pd.merge(df_valo, df_mapping, on="Produit")
df_final["Valeur_Reelle"] = df_final["Derniere_Valo"] * df_final["Pourcentage"]

# Affichage du graphique d'allocation
st.plotly_chart(px.pie(df_final, values='Valeur_Reelle', names='Sous-Catégorie'))