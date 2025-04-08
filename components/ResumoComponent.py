import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def ResumoComponent(df):
    st.subheader("📋 Resumo Histórico de Extremos Climáticos")

    # Garantir que os dados estejam válidos
    df_valid = df.dropna(subset=['Data', 'Hora (UTC)', 'Temp. Ins. (C)', 'Chuva (mm)', 'Radiacao (KJ/m²)'])

    # Criar coluna de datetime completo
    df_valid['Datetime'] = pd.to_datetime(df_valid['Data'].astype(str) + ' ' + df_valid['Hora (UTC)'], format='%Y-%m-%d %H:%M')
    df_valid = df_valid.sort_values('Datetime')  # Garantir ordenação
    df_valid.set_index('Datetime', inplace=True)

    # Temperatura mínima
    temp_min_idx = df_valid['Temp. Ins. (C)'].idxmin()
    temp_min = df_valid.loc[temp_min_idx]

    # Temperatura máxima
    temp_max_idx = df_valid['Temp. Ins. (C)'].idxmax()
    temp_max = df_valid.loc[temp_max_idx]

    # Precipitação máxima pontual
    chuva_max_idx = df_valid['Chuva (mm)'].idxmax()
    chuva_max = df_valid.loc[chuva_max_idx]

    # Radiação máxima
    rad_max_idx = df_valid['Radiacao (KJ/m²)'].idxmax()
    rad_max = df_valid.loc[rad_max_idx]

    # Chuva acumulada em 24h
    rolling_chuva_24h = df_valid['Chuva (mm)'].rolling('24H').sum()
    chuva_24h_idx = rolling_chuva_24h.idxmax()
    chuva_24h_val = rolling_chuva_24h.max()
    chuva_24h_fim = chuva_24h_idx
    chuva_24h_ini = chuva_24h_fim - pd.Timedelta(hours=24)

    # Chuva acumulada em 7 dias (168h)
    rolling_chuva_7d = df_valid['Chuva (mm)'].rolling('168H').sum()
    chuva_7d_idx = rolling_chuva_7d.idxmax()
    chuva_7d_val = rolling_chuva_7d.max()
    chuva_7d_fim = chuva_7d_idx
    chuva_7d_ini = chuva_7d_fim - pd.Timedelta(days=7)

    # Exibição
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🌡️ Temperatura Mínima", f"{temp_min['Temp. Ins. (C)']:.2f} °C", help=f"{temp_min['Data'].strftime('%d/%m/%Y')}")
        st.write("📅 Data/Hora: " + f"{temp_min['Data'].strftime('%d/%m/%Y')} {temp_min['Hora (UTC)']} UTC")

        st.metric("🌧️ Precipitação Máxima", f"{chuva_max['Chuva (mm)']:.2f} mm", help=f"{chuva_max['Data'].strftime('%d/%m/%Y')}")
        st.write("📅 Data/Hora: " + f"{chuva_max['Data'].strftime('%d/%m/%Y')} {chuva_max['Hora (UTC)']} UTC")

        st.metric("🌧️ Chuva Acumulada (24h)", f"{chuva_24h_val:.2f} mm")
        st.write("🕒 Período: " + f"{chuva_24h_ini.strftime('%d/%m/%Y %H:%M')} - {chuva_24h_fim.strftime('%d/%m/%Y %H:%M')} UTC")

    with col2:
        st.metric("🌡️ Temperatura Máxima", f"{temp_max['Temp. Ins. (C)']:.2f} °C", help=f"{temp_max['Data'].strftime('%d/%m/%Y')}")
        st.write("📅 Data/Hora: " + f"{temp_max['Data'].strftime('%d/%m/%Y')} {temp_max['Hora (UTC)']} UTC")

        st.metric("☀️ Radiação Máxima", f"{rad_max['Radiacao (KJ/m²)']:.2f} KJ/m²", help=f"{rad_max['Data'].strftime('%d/%m/%Y')}")
        st.write("📅 Data/Hora: " + f"{rad_max['Data'].strftime('%d/%m/%Y')} {rad_max['Hora (UTC)']} UTC")

        st.metric("🌧️ Chuva Acumulada (7 dias)", f"{chuva_7d_val:.2f} mm")
        st.write("🕒 Período: " + f"{chuva_7d_ini.strftime('%d/%m/%Y %H:%M')} - {chuva_7d_fim.strftime('%d/%m/%Y %H:%M')} UTC")
