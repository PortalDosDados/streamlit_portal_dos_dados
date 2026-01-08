import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import yfinance as yf
import warnings

# ============
# Configuração da página
# ============
st.set_page_config(
    page_title='Portal dos Dados - Séries Temporais',
    page_icon='assets/python.gif',
    layout='wide',
)

# ============
# Carregar CSS externo (UTF-8 para evitar erro de decodificação)
# ============
with open('style.css', 'r', encoding='utf-8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Logo
st.image('assets/python.gif', width=160)

st.title('Análise Técnica de Séries Temporais com Python')

st.markdown(
    '''
<div class='justificado'>
Este script demonstra um pipeline completo de análise de dados financeiros,
incluindo aquisição de dados, tratamento, criação de indicadores e visualização
de séries temporais para análise de tendência.
''',
    unsafe_allow_html=True,
)

# ============
# Entradas
# ============
ticker = st.text_input('Digite o ticker: (Ex:BBAS3.SA)', value='BBAS3.SA')
start_date = st.date_input('Data de início:', value=pd.to_datetime('2020-01-01'))
end_date = st.date_input('Data de fim:', value=pd.to_datetime('2025-12-31'))

# ============
# Botão estilizado herdado via CSS
# ============
if st.button('Gerar gráfico', key='grafico-btn'):

    df = yf.download(ticker, start=start_date, end=end_date)

    if df.empty:
        st.error('Nenhum dado encontrado para este período.')
    else:
        # Ajuste de colunas
        df.columns = df.columns.get_level_values(0)
    df.reset_index(inplace=True)

    df['Ticker'] = ticker
    df = df[['Date', 'Ticker', 'Open', 'Close', 'Low', 'High', 'Volume']]

    # Médias móveis
    df['MA_21'] = df['Close'].rolling(21).mean()
    df['MA_200'] = df['Close'].rolling(200).mean()

    # Criação do gráfico com Plotly
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df['Date'], y=df['Close'], mode='lines', name='Preço de Fechamento'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['Date'], y=df['MA_21'], mode='lines', name='Média Móvel 21 dias'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['Date'], y=df['MA_200'], mode='lines', name='Média Móvel 200 dias'
        )
    )

    fig.update_layout(
        title=f"Preço e Médias Móveis de {ticker}",
        xaxis_title="",
        yaxis_title="Preço",
        template="plotly_white",
        plot_bgcolor="#0B1933",
        paper_bgcolor="#0B1933",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)


# ============
# Explicação
# ============
st.markdown(
    '''
- Aquisição com **yfinance**
- Limpeza, reestruturação e criação de indicadores com **pandas**
- Gráficos com **matplotlib** e **seaborn**
- Médias Móveis de 21 e 200 períodos para análise de tendência
'''
)

# ============================================================================
# RODAPÉ E NOTAS
# ============================================================================
st.space()
# Imagem de fundo (certifique-se que a pasta assets existe)
st.image('./assets/fundo.jpg', use_container_width=True)
