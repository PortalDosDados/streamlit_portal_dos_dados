import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import warnings

# Configurações da página
st.set_page_config(
    page_title='Dione Nascimento - Python',       # Título da aba
    page_icon='assets/python.gif',       # Ícone da aba (pode ser .ico, .png ou emoji)
    layout='wide'                        # Layout da página (opcional)
)

st.image('assets/python.gif', width= 160)

st.header('Python')

# ---------------------------
# Título do dashboard
# ---------------------------
st.markdown('''
    <h2 style='color:#00E0B8; font-family: Montserrat, sans-serif;'>🧠 Análise Técnica de Séries Temporais com Python</h2>
''', unsafe_allow_html=True)

st.markdown('''
Este script é um projeto prático que demonstra o pipeline completo de uma análise de dados financeiros,
desde a aquisição de dados da web até a visualização de indicadores técnicos.
O objetivo é analisar a tendência de preço dos ativos, calculando e plotando 
Médias Móveis Simples (MMS) para identificar tendências de curto e longo prazo.         
            
            
''')

# ---------------------------
# Entradas do usuário
# ---------------------------
ticker = st.text_input('Digite o ticker: (Ex:BBAS3.SA)', value='BBAS3.SA')
start_date = st.date_input('Data de início: (Ex: ANO-MES-DIA)', value=pd.to_datetime('2020-01-01'))
end_date = st.date_input('Data de fim: (Ex: ANO-MES-DIA)', value=pd.to_datetime('2025-12-31'))

# ---------------------------
# Botão para rodar análise
# ---------------------------
if st.button('Gerar gráfico'):

    # Baixando dados
    df = yf.download(ticker, start=start_date, end=end_date)

    if df.empty:
        st.error('Nenhum dado encontrado para este período.')
    else:
        # Remove o nível superior do MultiIndex, se existir
        df.columns = df.columns.get_level_values(0)
        df.reset_index(inplace=True)

        df['Ticker'] = ticker
        df = df[['Date', 'Ticker', 'Open', 'Close', 'Low', 'High', 'Volume']]

        # Médias móveis
        df['MA_21'] = df['Close'].rolling(window=21).mean()
        df['MA_50'] = df['Close'].rolling(window=50).mean()
        df['MA_200'] = df['Close'].rolling(window=200).mean()

        # ---------------------------
        # Plot com Seaborn e Matplotlib
        # ---------------------------
        sns.set_style('whitegrid')
        plt.figure(figsize=(12, 6))

        sns.lineplot(x=df['Date'], y=df['Close'], label='Preço de Fechamento', color='blue', linewidth=2)
        sns.lineplot(x=df['Date'], y=df['MA_21'], label='Média Móvel 21 dias', color='orange', linewidth=2)
        sns.lineplot(x=df['Date'], y=df['MA_50'], label='Média Móvel 50 dias', color='green', linewidth=2)
        sns.lineplot(x=df['Date'], y=df['MA_200'], label='Média Móvel 200 dias', color='red', linewidth=2)

        plt.title(f'Preço de Fechamento e Médias Móveis de {ticker}', fontsize=16)
        plt.xlabel('Data', fontsize=12)
        plt.ylabel('Preço de Fechamento (USD)', fontsize=12)
        plt.legend()
        plt.tight_layout()

        # Exibir o gráfico no Streamlit
        st.pyplot(plt)
        
st.markdown('''

- Aquisição de Dados:

    - A biblioteca yfinance é utilizada para se conectar à API do Yahoo Finance e baixar o histórico de cotações do ticker.

- Tratamento e Preparação (Data Wrangling):

    - A biblioteca pandas é usada para organizar os dados, o DataFrame baixado é limpo, o índice é redefinido e as colunas são reestruturadas para focar apenas nas informações essenciais (Data, Ticker, Preços de Abertura/Fechamento, etc.).

- Engenharia de Features (Criação de Indicadores):

    - Para entender as tendências, novas colunas são criadas usando a função .rolling() do pandas:

    - Média Móvel de 21 dias (MA_21): Um indicador de tendência de curto prazo.

    - Média Móvel de 200 dias (MA_200): Um indicador de tendência de longo prazo.

- Visualização de Dados:

    - Utilizando matplotlib e seaborn, um gráfico de linha é gerado para visualizar a análise.

    - O gráfico plota o Preço de Fechamento diário (em azul) sobreposto pelas duas médias móveis (em laranja e vermelho).

    - Esta visualização permite identificar rapidamente a tendência principal do ativo (se a MA_200 está subindo ou descendo) e sinais de momentum de curto prazo (se o preço está acima ou abaixo da MA_21).

- Bibliotecas Utilizadas (Tech Stack)
    - yfinance: Para aquisição de dados financeiros de forma automatizada.

    - Pandas: Para manipulação, limpeza e análise dos dados (cálculo das médias móveis).

    - Matplotlib & Seaborn: Para a criação da visualização de dados.

    - Warnings: Utilizada para suprimir avisos e limpar a saída do console.
     
''')