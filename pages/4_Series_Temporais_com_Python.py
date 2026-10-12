from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from utils.ui import load_css, get_asset_path, render_footer

# 1. Configuração da página
st.set_page_config(
    page_title='Portal dos Dados - Séries Temporais',
    page_icon=get_asset_path('python.gif'),
    layout='wide',
)

# Carregamento de estilos globais
load_css('style.css')

# Header com ícone e introdução
col_icon, col_title = st.columns([1, 6], vertical_alignment="center")
with col_icon:
    st.image(get_asset_path('python.gif'), width=120)
with col_title:
    st.title('Análise Técnica de Séries Temporais com Python')
    st.caption('Pipeline quantitativo: ingestão de dados de mercado, cálculo de médias móveis e visualização interativa.')

st.markdown(
    '''
<div class='justificado'>
Este módulo demonstra um pipeline completo de análise de dados financeiros.
Os dados são requisitados dinamicamente via API, pré-processados e enriquecidos com indicadores técnicos
(Médias Móveis Simples de curto e longo prazo), alimentando um dashboard interativo construído com Plotly.
</div>
''',
    unsafe_allow_html=True,
)


# 2. Ingestão de Dados com Cache
@st.cache_data(ttl=3600, show_spinner=False)
def carregar_dados_ativo(ticker_symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
    """
    Busca dados de cotações com cache em memória (TTL: 1 hora) para máxima velocidade
    e para evitar limitações de taxa (rate limiting) na API externa.
    """
    df = yf.download(ticker_symbol, start=start, end=end, progress=False)
    if df is None or df.empty:
        return pd.DataFrame()

    # Normalização de MultiIndex (caso gerado por versões recentes do yfinance)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()
    return df


# 3. Formulário de Parâmetros
with st.container():
    col_tick, col_ini, col_fim = st.columns([2, 1, 1])

    with col_tick:
        ticker = st.text_input(
            'Ticker do Ativo (Ex: PETR4.SA, BBAS3.SA, VALE3.SA, AAPL):',
            value='BBAS3.SA',
        ).strip().upper()

    with col_ini:
        start_date = st.date_input('Data de Início:', value=datetime(2023, 1, 1))

    with col_fim:
        end_date = st.date_input('Data de Fim:', value=datetime.today())

    col_btn, col_opts = st.columns([1, 2], vertical_alignment="center")
    with col_btn:
        executar = st.button('🚀 Atualizar Análise Gráfica', type='primary', use_container_width=True)

# 4. Execução e Visualização
if executar or ticker:
    if start_date >= end_date:
        st.error('A data de início deve ser rigorosamente anterior à data de fim.')
    else:
        with st.spinner(f'Consultando histórico de cotações para "{ticker}"...'):
            try:
                df = carregar_dados_ativo(ticker, start_date, end_date)

                if df.empty:
                    st.warning(f'Nenhum dado encontrado para o ticker "{ticker}" no período selecionado. Verifique o código do ativo.')
                elif 'Close' not in df.columns:
                    st.error('A coluna de fechamento (Close) não foi localizada no conjunto de dados retornado.')
                else:
                    # Engenharia de Features: Médias Móveis
                    df['MA_21'] = df['Close'].rolling(window=21, min_periods=1).mean()
                    df['MA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()

                    # Métricas Principais
                    ultimo_preco = float(df['Close'].iloc[-1])
                    primeiro_preco = float(df['Close'].iloc[0])
                    variacao = ((ultimo_preco - primeiro_preco) / primeiro_preco) * 100
                    preco_max = float(df['Close'].max())
                    preco_min = float(df['Close'].min())

                    st.markdown('### 📊 Indicadores do Período')
                    k1, k2, k3, k4 = st.columns(4)
                    k1.metric('Último Fechamento', f'R$ {ultimo_preco:.2f}')
                    k2.metric('Variação no Período', f'{variacao:+.2f}%')
                    k3.metric('Máxima do Período', f'R$ {preco_max:.2f}')
                    k4.metric('Mínima do Período', f'R$ {preco_min:.2f}')

                    # Gráfico Interativo com Plotly
                    fig = go.Figure()

                    fig.add_trace(
                        go.Scatter(
                            x=df['Date'],
                            y=df['Close'],
                            mode='lines',
                            name='Preço de Fechamento',
                            line=dict(color='#00D4FF', width=2),
                        )
                    )

                    fig.add_trace(
                        go.Scatter(
                            x=df['Date'],
                            y=df['MA_21'],
                            mode='lines',
                            name='Média Móvel Rápida (21 períodos)',
                            line=dict(color='#FFA500', width=1.5),
                        )
                    )

                    fig.add_trace(
                        go.Scatter(
                            x=df['Date'],
                            y=df['MA_200'],
                            mode='lines',
                            name='Média Móvel Lenta (200 períodos)',
                            line=dict(color='#FF4B4B', width=1.5, dash='dash'),
                        )
                    )

                    fig.update_layout(
                        title=f'Série Histórica e Tendência — {ticker}',
                        xaxis_title='Data de Negociação',
                        yaxis_title='Preço Unitário (R$ / US$)',
                        template='plotly_dark',
                        hovermode='x unified',
                        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                        margin=dict(l=40, r=40, t=60, b=40),
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    # Tabela de Amostra com Expander
                    with st.expander('🔍 Visualizar Dados Tabulares (Últimos Registros)'):
                        st.dataframe(
                            df[['Date', 'Open', 'High', 'Low', 'Close', 'MA_21', 'MA_200']].tail(15),
                            use_container_width=True,
                        )

            except Exception as e:
                st.error(f'Falha ao carregar ou processar os dados do ativo: {e}')

st.markdown('---')
st.markdown(
    '''
### 📌 Metodologia e Tecnologias
- **Aquisição de Dados:** API do `yfinance` com cache inteligente de 1 hora para otimização de requisições.
- **Engenharia de Features:** `pandas` para alinhamento temporal e cálculo de médias móveis de curto e longo prazo.
- **Visualização Analítica:** `Plotly` interativo com modo hover unificado, zoom dinâmico e suporte a tema escuro.
'''
)

# Rodapé
render_footer()
