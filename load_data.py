import pandas as pd

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