import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from components.ResumoComponent import ResumoComponent
from components.ResumoAnualComponent import ResumoAnualComponent
from components.ComparativoAnualComponent import ComparativoAnualComponent
from components.MediasMensaisComponent import MediasMensaisComponent
from components.MediasDiariasComponent import MediasDiariasComponent
from layout.HeaderComponent import HeaderComponent

HeaderComponent()

@st.cache_data

def load_data():
    df = pd.read_csv("data.csv", sep=';', quotechar='"', encoding='utf-8')

    # Corrigir vírgulas e converter colunas para numérico
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace(',', '.', regex=False)
            try:
                df[col] = df[col].astype(float)
            except:
                pass

    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')
    df['Ano'] = df['Data'].dt.year
    df['Mes'] = df['Data'].dt.month
    df['Dia'] = df['Data'].dt.day
    return df

df = load_data()
anos_disponiveis = sorted(df['Ano'].dropna().unique())

aba = st.tabs(["📋 Resumo Histórico de Extremos Climáticos", "📅 Resumo de Extremos por Ano", "📈 Comparação entre Anos", "📅 Médias Diárias por Mês (Ano único)", "📅 Médias Diárias por Mês"])

# ------------------------ ABA 0 ------------------------
with aba[0]:
    ResumoComponent(df)

# ------------------------ ABA 1 ------------------------
with aba[1]:
    ResumoAnualComponent(df)
    
# ------------------------ ABA 2 ------------------------
with aba[2]:
    ComparativoAnualComponent(df, anos_disponiveis)

# ------------------------ ABA 3 ------------------------
with aba[3]:
    MediasMensaisComponent(df, anos_disponiveis)

# ------------------------ ABA 4 ------------------------
with aba[4]:
    MediasDiariasComponent(df, anos_disponiveis)