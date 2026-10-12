import streamlit as st
from utils.ui import load_css, get_asset_path, render_footer

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title='Portal dos Dados - Power BI',
    page_icon=get_asset_path('power_bi.png'),
    layout='wide',
)

# Carregamento de estilos globais
load_css('style.css')

# Header com ícone e introdução
col_icon, col_title = st.columns([1, 6], vertical_alignment="center")
with col_icon:
    st.image(get_asset_path('power_bi.png'), width=110)
with col_title:
    st.title('Power BI & Business Intelligence')
    st.caption('Soluções analíticas de ponta a ponta: do ETL e modelagem dimensional aos dashboards executivos.')

st.markdown(
    '''
<div class='justificado'>
O <b>Power BI</b> é uma das ferramentas centrais do meu ecossistema de dados.
Aqui estão projetos públicos demonstrando modelagem dimensional (Star Schema),
indicadores de performance (KPIs), visualizações interativas e integração com engenharia de dados.
</div>
''',
    unsafe_allow_html=True,
)

# Navegação organizada por abas temáticas
tab_eleicoes, tab_logistica, tab_financeiro, tab_rh = st.tabs([
    '🗳️ Eleições Presidenciais',
    '🚚 Operações Logísticas',
    '💰 Execução Orçamentária',
    '👥 Folha de Pagamento',
])

# -----------------------------------------------------------
# ABA 1 — ELEIÇÕES
# -----------------------------------------------------------
with tab_eleicoes:
    st.subheader('Dashboard de Análise Eleitoral Presidencial')
    st.markdown(
        '''
        <div class='justificado'>
        Análise exploratória e visual das eleições presidenciais brasileiras, consolidando milhões de registros
        em uma interface rápida e intuitiva para acompanhamento da dinâmica dos votos em diferentes recortes federativos.
        </div>
        ''',
        unsafe_allow_html=True,
    )

    col_vid, col_det = st.columns([3, 2], gap='large')
    with col_vid:
        st.video('https://www.youtube.com/watch?v=hQVrG6j-OMs')
    with col_det:
        st.markdown('#### 🎯 Destaques e Funcionalidades')
        st.markdown(
            '''
            * **Visão Macro e Micro:** Distribuição nacional agregada e recorte granular por estado.
            * **Comparação Direta:** Benchmark dinâmico entre candidatos com apuração percentual e absoluta.
            * **Treemaps & Rankings:** Visualização proporcional da representatividade de votos.
            * **Filtros Sincronizados:** Segmentação por ano eleitoral, turno e unidade federativa.
            '''
        )

# -----------------------------------------------------------
# ABA 2 — LOGÍSTICA
# -----------------------------------------------------------
with tab_logistica:
    st.subheader('Painel de Gestão e Eficiência de Frotas')
    st.markdown(
        '''
        <div class='justificado'>
        Visão integrada para gestão de transporte e manutenção pesada. O painel correlaciona custos operacionais,
        quilometragem rodada e paradas de manutenção para otimização do custo por quilômetro (R$/km) e disponibilidade da frota.
        </div>
        ''',
        unsafe_allow_html=True,
    )

    col_vid, col_det = st.columns([3, 2], gap='large')
    with col_vid:
        st.video('https://www.youtube.com/watch?v=V6D1s--n_oA&t=12s')
    with col_det:
        st.markdown('#### 🎯 Indicadores Monitorados')
        st.markdown(
            '''
            * **Custos de Manutenção:** Acompanhamento por fabricante, modelo e categoria de peça.
            * **Volumetria Operacional:** Total de viagens expedidas e taxa de cumprimento de rotas.
            * **Disponibilidade Física:** Ocorrências de paradas corretivas x preventivas.
            * **KPI de Eficiência:** Cumprimento de prazos de entrega (On-Time Delivery).
            '''
        )

# -----------------------------------------------------------
# ABA 3 — EXECUÇÃO FINANCEIRA
# -----------------------------------------------------------
with tab_financeiro:
    st.subheader('Execução Orçamentária e Gestão de Despesas Públicas')
    st.markdown(
        '''
        <div class='justificado'>
        Painel executivo voltado para a transparência e fiscalização do ciclo orçamentário
        (Fixação, Empenho, Liquidação e Pagamento). Permite acompanhar o ritmo de consumo dos recursos e restos a pagar.
        </div>
        ''',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap='medium')
    with col1:
        st.image(get_asset_path('fin_01.png'), caption='Visão Geral de Empenhos e Saldos', use_container_width=True)
    with col2:
        st.image(get_asset_path('fin_02.png'), caption='Evolução Histórica e Restos a Pagar', use_container_width=True)

    st.markdown('#### 📊 Indicadores-Chave (KPIs)')
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.info('**Total Empenhado:** Compromissos formalizados pelo órgão')
    col_kpi2.warning('**Total a Liquidar/Pagar:** Passivo pendente de quitação')
    col_kpi3.success('**Índice de Execução:** % de empenhos efetivamente liquidados')

# -----------------------------------------------------------
# ABA 4 — FOLHA DE PAGAMENTO
# -----------------------------------------------------------
with tab_rh:
    st.subheader('Data Warehouse & BI de Folha de Pagamento Municipal')
    st.markdown(
        '''
        <div class='justificado'>
        Arquitetura analítica completa: pipeline de ingestão e transformação via <b>Pentaho Data Integration (PDI)</b>,
        modelagem em esquema estrela (Star Schema) e front-end com drill-down detalhado da folha funcional.
        </div>
        ''',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3, gap='small')
    with col1:
        st.image(get_asset_path('pmf_01.png'), caption='Visão Consolidada da Folha', use_container_width=True)
    with col2:
        st.image(get_asset_path('pmf_02.jpg'), caption='Distribuição por Grau de Instrução', use_container_width=True)
    with col3:
        st.image(get_asset_path('pmf_03.jpg'), caption='Detalhamento Individual e Lotação', use_container_width=True)

    st.markdown('#### 🛠️ Pilha Tecnológica do Projeto')
    st.markdown(
        '''
        * **Engenharia de Dados:** ETL automatizado com Pentaho Data Integration limpando bases legadas.
        * **Modelagem Dimensional:** Fato Folha de Pagamento conectada a dimensões Cargo, Secretaria e Servidor.
        * **Segurança e Governança:** Agregações seguras preservando a conformidade legal.
        '''
    )

# -----------------------------------------------------------
# RODAPÉ
# -----------------------------------------------------------
render_footer()
