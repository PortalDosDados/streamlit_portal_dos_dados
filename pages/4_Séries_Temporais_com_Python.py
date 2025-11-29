import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import warnings

# ============  
# Configuração da página  
# ============  
st.set_page_config(
    page_title='Dione Nascimento - Python',
    page_icon='assets/python.gif',
    layout='wide'
)

# ============  
# Carregar CSS externo (UTF-8 para evitar erro de decodificação)  
# ============  
with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Logo  
st.image('assets/python.gif', width=160)

st.subheader('Análise Técnica de Séries Temporais com Python')

st.markdown("""
<div class="justificado">
Este script demonstra um pipeline completo de análise de dados financeiros,
incluindo aquisição de dados, tratamento, criação de indicadores e visualização
de séries temporais para análise de tendência.
""", unsafe_allow_html=True)

# ============  
# Entradas  
# ============  
ticker = st.text_input('Digite o ticker: (Ex:BBAS3.SA)', value='BBAS3.SA')
start_date = st.date_input('Data de início:', value=pd.to_datetime('2020-01-01'))
end_date = st.date_input('Data de fim:', value=pd.to_datetime('2025-12-31'))

# ============  
# Botão estilizado herdado via CSS  
# ============  
if st.button('Gerar gráfico', key="grafico-btn"):

    df = yf.download(ticker, start=start_date, end=end_date)

    if df.empty:
        st.error('Nenhum dado encontrado para este período.')
    else:
        df.columns = df.columns.get_level_values(0)
        df.reset_index(inplace=True)

        df['Ticker'] = ticker
        df = df[['Date', 'Ticker', 'Open', 'Close', 'Low', 'High', 'Volume']]

        df['MA_21'] = df['Close'].rolling(21).mean()
        df['MA_200'] = df['Close'].rolling(200).mean()

        sns.set_style('whitegrid')
        plt.figure(figsize=(12, 6))

        sns.lineplot(x=df['Date'], y=df['Close'], label='Preço de Fechamento')
        sns.lineplot(x=df['Date'], y=df['MA_21'], label='Média Móvel 21 dias')
        sns.lineplot(x=df['Date'], y=df['MA_200'], label='Média Móvel 200 dias')

        plt.title(f'Preço e Médias Móveis de {ticker}', fontsize=16)
        plt.xlabel('Data')
        plt.ylabel('Preço')
        plt.legend()
        plt.tight_layout()

        st.pyplot(plt)

# ============  
# Explicação  
# ============  
st.markdown("""
- Aquisição com **yfinance**
- Limpeza, reestruturação e criação de indicadores com **pandas**
- Gráficos com **matplotlib** e **seaborn**
- Médias Móveis de 21 e 200 períodos para análise de tendência
""")

