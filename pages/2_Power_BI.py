import streamlit as st

# 1. CONFIGURAÇÃO (Sempre a primeira linha do Streamlit)
st.set_page_config(
    page_title='Portal dos Dados - Power BI',
    page_icon='assets/power_bi.png',
    layout='wide'
)

#CSS
with open('style.css', 'r', encoding='utf-8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.image('assets/power_bi.png', width=160)
st.header('Power BI')

st.markdown('''
<div class='justificado'>
O <b>Power BI</b> tem sido a minha principal ferramenta para visualização de dados.
É simples de utilizar e amplamente adotado no mercado.
Aqui apresento alguns projetos que posso compartilhar publicamente.
</div>
''', unsafe_allow_html=True)

# -----------------------------------------------------------
# SEÇÃO 1 — ELEIÇÕES
# -----------------------------------------------------------
st.subheader('Dashboard Eleições Presidenciais')

st.markdown('''
<div class='justificado'>
Análise completa das eleições presidenciais no Brasil, transformando dados dispersos
em visualizações claras e úteis para entender o comportamento do eleitorado.
</div>
''', unsafe_allow_html=True)

st.subheader('Visualização do Dashboard')
st.video('https://www.youtube.com/watch?v=hQVrG6j-OMs')

st.subheader('Principais recursos e análises')
st.markdown('''
- Visão nacional de votos
- Comparação entre candidatos
- Destaque automático do mais votado
- Ranking detalhado
- Treemap por estado
- Filtros interativos (ano, turno, estado)
''')

# -----------------------------------------------------------
# SEÇÃO 2 — LOGÍSTICA
# -----------------------------------------------------------
st.subheader('Dashboard Logístico Interativo')

st.markdown('''
<div class='justificado'>
Análise consolidada do desempenho logístico e financeiro da operação de transporte.
Inclui KPIs, custos, viagens, eficiência e manutenção por marca e tipo de veículo.
</div>
''', unsafe_allow_html=True)

st.video('https://www.youtube.com/watch?v=V6D1s--n_oA&t=12s')

st.subheader('Principais Análises')
st.markdown('''
- Visão Financeira Consolidada
- Volume mensal de viagens
- KPI de eficiência de entregas
- Análise detalhada de custos de manutenção
''')

# -----------------------------------------------------------
# SEÇÃO 3 — EXECUÇÃO FINANCEIRA
# -----------------------------------------------------------
st.subheader('Dashboard de Execução Financeira (Setor Público)')

st.markdown('''
<div class='justificado'>
Dashboard executivo para análise de empenho, pagamento e evolução histórica do orçamento.
''', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.image('assets/fin_01.png', width=700)

with col2:
    st.image('assets/fin_02.png', width=700)

st.subheader('Principais Indicadores')
st.markdown('''
- Total Empenho
- Total a Pagar
- Total Pago
- KPI de eficiência (% empenho pago)
- Histórico anual
''')

# -----------------------------------------------------------
# SEÇÃO 4 — FOLHA DE PAGAMENTO
# -----------------------------------------------------------
st.subheader('Dashboard Análise da Folha de Pagamento')

st.markdown('''
<div class='justificado'>
Pipeline completo de BI: ETL, modelagem em Data Warehouse e visualização interativa
para análise da folha de pagamento da Prefeitura.
</div>
''', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.image('assets/pmf_01.png', width=700)
with col2:
    st.image('assets/pmf_02.jpg', width=700)
with col3:
    st.image('assets/pmf_03.jpg', width=700)

st.subheader('Principais Recursos do Painel')
st.markdown('''
- ETL com Pentaho
- Modelo Estrela (DW)
- Filtros interativos
- KPIs macro
- Análises por grau de instrução e cargo
- Tabela detalhada por servidor
''')
