import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

st.set_page_config(page_title="Análise Climática", layout="wide")
st.title("📊 Análise Climática Comparativa")
st.write("Dados - 2006-2024")
st write("Fonte: Instituto Nacional de Meteorologia, INMET - Estação A511")
st write("Localização: -19,573889	 -42,622500")
st.write("Tem algumas inconsistências por falta de dados do ano")

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

# ------------------------ ABA 1 ------------------------
with aba[0]:
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


with aba[1]:
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

# ------------------------ ABA 1 ------------------------
with aba[2]:
    st.subheader("📆 Comparação entre Anos")

    anos_selecionados = st.multiselect("Selecione os anos para comparar", anos_disponiveis, default=anos_disponiveis[:2])
    df_filtrado = df[df['Ano'].isin(anos_selecionados)]

    df_grouped = df_filtrado.groupby(['Ano', 'Mes']).agg({
        "Temp. Ins. (C)": "mean",
        "Umi. Ins. (%)": "mean",
        "Radiacao (KJ/m²)": "mean",
        "Chuva (mm)": "sum"
    }).reset_index()

    df_grouped.columns = ['Ano', 'Mês', 'Temperatura', 'Umidade', 'Radiação', 'Chuva']

    def gerar_mapa_cores(anos):
        cmap = cm.get_cmap('tab10', len(anos)) if len(anos) <= 10 else cm.get_cmap('hsv', len(anos))
        return {ano: cmap(i) for i, ano in enumerate(anos)}

    def plot_line_chart(df, y, ylabel, title, color_map):
        fig, ax = plt.subplots(figsize=(7, 4))
        for ano in sorted(color_map.keys()):
            dados_ano = df[df['Ano'] == ano]
            ax.plot(dados_ano['Mês'], dados_ano[y], marker='o', label=str(ano), color=color_map[ano])
        ax.set_xlabel("Mês")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True)
        ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), title="Ano")
        plt.tight_layout()
        return fig

    color_map = gerar_mapa_cores(anos_selecionados)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌡️ Temperatura Média")
        st.pyplot(plot_line_chart(df_grouped, 'Temperatura', '°C', 'Temperatura Média por Mês', color_map))
    with col2:
        st.subheader("☀️ Radiação Média")
        st.pyplot(plot_line_chart(df_grouped, 'Radiação', 'KJ/m²', 'Radiação Média por Mês', color_map))

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("💧 Umidade Média")
        st.pyplot(plot_line_chart(df_grouped, 'Umidade', '%', 'Umidade Média por Mês', color_map))
    with col4:
        st.subheader("🌧️ Precipitação Total")
        st.pyplot(plot_line_chart(df_grouped, 'Chuva', 'mm', 'Precipitação Total por Mês', color_map))

# ------------------------ ABA 1 ------------------------
with aba[3]:
    st.subheader("📆 Análise de um Ano com Variação Mensal")

    ano_selecionado = st.selectbox("Selecione um ano", anos_disponiveis)
    df_ano = df[df['Ano'] == ano_selecionado]

    df_mensal = df_ano.groupby('Mes').agg({
        "Temp. Ins. (C)": ['mean', 'min', 'max'],
        "Umi. Ins. (%)": ['mean', 'min', 'max'],
        "Radiacao (KJ/m²)": ['mean', 'min', 'max'],
        "Chuva (mm)": ['sum', 'min', 'max']  # Precipitação como total, mas mostra min/max para coerência
    }).reset_index()

    df_mensal.columns = ['Mês',
                         'Temp_Media', 'Temp_Min', 'Temp_Max',
                         'Umi_Media', 'Umi_Min', 'Umi_Max',
                         'Rad_Media', 'Rad_Min', 'Rad_Max',
                         'Chuva_Total', 'Chuva_Min', 'Chuva_Max']

    def plot_barras_com_erro(df, media_col, min_col, max_col, ylabel, title, color):
        fig, ax = plt.subplots(figsize=(7, 4))
        x = df['Mês']
        y = df[media_col]

        # Corrigir para evitar valores negativos nas barras de erro
        yerr_lower = (y - df[min_col]).clip(lower=0)
        yerr_upper = (df[max_col] - y).clip(lower=0)
        yerr = [yerr_lower, yerr_upper]

        ax.bar(x, y, yerr=yerr, capsize=5, color=color, alpha=0.7)
        ax.set_xlabel("Mês")
        ax.set_ylabel(ylabel)
        ax.set_title(title + f" - {ano_selecionado}")
        ax.grid(True, axis='y')
        ax.set_xticks(range(1, 13))
        plt.tight_layout()
        return fig


    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌡️ Temperatura Média (com min/max)")
        st.pyplot(plot_barras_com_erro(df_mensal, 'Temp_Media', 'Temp_Min', 'Temp_Max', '°C', 'Temperatura Média Mensal', 'salmon'))

    with col2:
        st.subheader("☀️ Radiação Média (com min/max)")
        st.pyplot(plot_barras_com_erro(df_mensal, 'Rad_Media', 'Rad_Min', 'Rad_Max', 'KJ/m²', 'Radiação Mensal Média', 'gold'))

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("💧 Umidade Média (com min/max)")
        st.pyplot(plot_barras_com_erro(df_mensal, 'Umi_Media', 'Umi_Min', 'Umi_Max', '%', 'Umidade Média Mensal', 'skyblue'))

    with col4:
        st.subheader("🌧️ Precipitação Total (com min/max)")
        st.pyplot(plot_barras_com_erro(df_mensal, 'Chuva_Total', 'Chuva_Min', 'Chuva_Max', 'mm', 'Precipitação Mensal Total', 'mediumseagreen'))

# ------------------------ ABA 2 ------------------------

with aba[4]:
    st.subheader("📅 Médias Diárias por Mês")

    ano_unico = st.selectbox("Selecione um ano para análise detalhada diária", anos_disponiveis)
    df_ano = df[df['Ano'] == ano_unico]

    meses_disponiveis = sorted(df_ano['Mes'].dropna().unique())
    meses_nomes = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    meses_labels = [meses_nomes[m] for m in meses_disponiveis]
    mes_label = st.selectbox("Selecione o mês", meses_labels)
    meses_selecionados = [k for k, v in meses_nomes.items() if v == mes_label]

    df_diario = df_ano[df_ano['Mes'].isin(meses_selecionados)].groupby(['Mes', 'Dia']).agg({
        "Temp. Ins. (C)": "mean",
        "Umi. Ins. (%)": "mean",
        "Radiacao (KJ/m²)": "mean",
        "Chuva (mm)": "sum"
    }).reset_index()

    df_diario.columns = ['Mês', 'Dia', 'Temperatura', 'Umidade', 'Radiação', 'Chuva']

    def plot_diario(df, y, ylabel, title, color):
        fig, ax = plt.subplots(figsize=(8, 4))
        mes = df['Mês'].iloc[0]
        dados_mes = df[df['Mês'] == mes]
        ax.plot(dados_mes['Dia'], dados_mes[y], label=meses_nomes[mes], color=color)
        ax.set_xlabel("Dia do Mês")
        ax.set_ylabel(ylabel)
        ax.set_title(f"{title} - {meses_nomes[mes]} de {ano_unico}")
        ax.grid(True)
        ax.legend()
        plt.tight_layout()
        return fig

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌡️ Temperatura Média Diária")
        st.pyplot(plot_diario(df_diario, 'Temperatura', '°C', 'Temperatura Média Diária', 'red'))
    with col2:
        st.subheader("☀️ Radiação Média Diária")
        st.pyplot(plot_diario(df_diario, 'Radiação', 'KJ/m²', 'Radiação Média Diária', 'orange'))

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("💧 Umidade Média Diária")
        st.pyplot(plot_diario(df_diario, 'Umidade', '%', 'Umidade Média Diária', 'blue'))
    with col4:
        st.subheader("🌧️ Precipitação Diária")
        st.pyplot(plot_diario(df_diario, 'Chuva', 'mm', 'Precipitação Diária', 'green'))

