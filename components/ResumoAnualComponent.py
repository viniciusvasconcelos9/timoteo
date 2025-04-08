import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def ResumoAnualComponent(df):
    st.subheader("📅 Resumo de Extremos por Ano")

    # Garantir dados válidos
    df_valid = df.dropna(subset=['Data', 'Hora (UTC)', 'Temp. Ins. (C)', 'Chuva (mm)', 'Radiacao (KJ/m²)'])

    # Criar coluna de datetime completo
    df_valid['Datetime'] = pd.to_datetime(df_valid['Data'].astype(str) + ' ' + df_valid['Hora (UTC)'], format='%Y-%m-%d %H:%M')
    df_valid['Ano'] = df_valid['Datetime'].dt.year
    df_valid = df_valid.sort_values('Datetime')

    # Seleção de ano
    anos_disponiveis = sorted(df_valid['Ano'].unique(), reverse=True)
    ano_selecionado = st.selectbox("Selecione o ano", anos_disponiveis)

    # Filtrar pelo ano selecionado
    df_ano = df_valid[df_valid['Ano'] == ano_selecionado].copy()
    df_ano.set_index('Datetime', inplace=True)

    if not df_ano.empty:
        # Temperatura mínima
        temp_min_idx = df_ano['Temp. Ins. (C)'].idxmin()
        temp_min = df_ano.loc[temp_min_idx]

        # Temperatura máxima
        temp_max_idx = df_ano['Temp. Ins. (C)'].idxmax()
        temp_max = df_ano.loc[temp_max_idx]

        # Precipitação máxima
        chuva_max_idx = df_ano['Chuva (mm)'].idxmax()
        chuva_max = df_ano.loc[chuva_max_idx]

        # Radiação máxima
        rad_max_idx = df_ano['Radiacao (KJ/m²)'].idxmax()
        rad_max = df_ano.loc[rad_max_idx]

        # Chuva acumulada em 24h
        rolling_24h = df_ano['Chuva (mm)'].rolling('24H').sum()
        chuva_24h_idx = rolling_24h.idxmax()
        chuva_24h_val = rolling_24h.max()
        chuva_24h_ini = chuva_24h_idx - pd.Timedelta(hours=24)

        # Chuva acumulada em 7 dias
        rolling_7d = df_ano['Chuva (mm)'].rolling('168H').sum()
        chuva_7d_idx = rolling_7d.idxmax()
        chuva_7d_val = rolling_7d.max()
        chuva_7d_ini = chuva_7d_idx - pd.Timedelta(days=7)

        # Exibição
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🌡️ Temperatura Mínima", f"{temp_min['Temp. Ins. (C)']:.2f} °C", help=temp_min.name.strftime('%d/%m/%Y'))
            st.write("📅 Data/Hora: " + temp_min.name.strftime('%d/%m/%Y %H:%M') + " UTC")

            st.metric("🌧️ Precipitação Máxima", f"{chuva_max['Chuva (mm)']:.2f} mm", help=chuva_max.name.strftime('%d/%m/%Y'))
            st.write("📅 Data/Hora: " + chuva_max.name.strftime('%d/%m/%Y %H:%M') + " UTC")

            st.metric("🌧️ Chuva Acumulada (24h)", f"{chuva_24h_val:.2f} mm")
            st.write("🕒 Período: " + f"{chuva_24h_ini.strftime('%d/%m/%Y %H:%M')} - {chuva_24h_idx.strftime('%d/%m/%Y %H:%M')} UTC")

        with col2:
            st.metric("🌡️ Temperatura Máxima", f"{temp_max['Temp. Ins. (C)']:.2f} °C", help=temp_max.name.strftime('%d/%m/%Y'))
            st.write("📅 Data/Hora: " + temp_max.name.strftime('%d/%m/%Y %H:%M') + " UTC")

            st.metric("☀️ Radiação Máxima", f"{rad_max['Radiacao (KJ/m²)']:.2f} KJ/m²", help=rad_max.name.strftime('%d/%m/%Y'))
            st.write("📅 Data/Hora: " + rad_max.name.strftime('%d/%m/%Y %H:%M') + " UTC")

            st.metric("🌧️ Chuva Acumulada (7 dias)", f"{chuva_7d_val:.2f} mm")
            st.write("🕒 Período: " + f"{chuva_7d_ini.strftime('%d/%m/%Y %H:%M')} - {chuva_7d_idx.strftime('%d/%m/%Y %H:%M')} UTC")
    else:
        st.warning("Nenhum dado disponível para o ano selecionado.")
