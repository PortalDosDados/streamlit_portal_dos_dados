import streamlit as st
from utils.ui import load_css, get_asset_path, render_footer

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title='Portal dos Dados - Power Apps',
    page_icon=get_asset_path('power_apps.png'),
    layout='wide',
)

# Carregamento de estilos globais
load_css('style.css')

# Header com ícone e introdução
col_icon, col_title = st.columns([1, 6], vertical_alignment="center")
with col_icon:
    st.image(get_asset_path('power_apps.png'), width=110)
with col_title:
    st.title('Power Apps & Digitalização Operacional')
    st.caption('Eliminando papel, formulários manuais e retrabalho no chão de fábrica através do ecossistema Microsoft Power Platform.')

st.markdown(
    '''
<div class='justificado'>
O <b>Power Apps</b> é o meu principal acelerador para digitalização rápida de processos industriais.
O objetivo central é claro: <i>facilitar a vida do operador e do técnico na ponta, garantindo dados íntegros e em tempo real para a gestão.</i>
</div>
''',
    unsafe_allow_html=True,
)

# Navegação organizada por abas
tab_lub, tab_insp, tab_ferr, tab_pend = st.tabs([
    '🛢️ Catálogo de Lubrificantes',
    '🔍 Inspeção de Equipamentos',
    '🛠️ Controle de Ferramentaria',
    '📋 Gestão de Pendências',
])

# -----------------------------------------------------------
# ABA 1 — CATÁLOGO DE LUBRIFICANTES
# -----------------------------------------------------------
with tab_lub:
    st.subheader('Aplicativo de Catálogo Técnico para Lubrificação Industrial')
    st.markdown(
        '''
        <div class='justificado'>
        Desenvolvido para eliminar o erro humano na seleção e aplicação de graxas e óleos industriais.
        O técnico pesquisa pelo ponto de lubrificação ou pelo equipamento e tem acesso imediato à especificação
        correta, volume, periodicidade e FISPQ correspondente.
        </div>
        ''',
        unsafe_allow_html=True,
    )

    col_v, col_d = st.columns([3, 2], gap='large')
    with col_v:
        st.video('https://www.youtube.com/watch?v=MNXcNj8PiOU')
    with col_d:
        st.markdown('#### 🎯 Benefícios Operacionais')
        st.markdown(
            '''
            * **Confiabilidade:** Previne contaminação cruzada por mistura de bases químicas incompatíveis.
            * **Consulta Ágil:** Acesso instantâneo em tablets ou smartphones na área operacional.
            * **Padronização:** Dados centralizados alinhados ao plano mestre de lubrificação da planta.
            '''
        )

# -----------------------------------------------------------
# ABA 2 — INSPEÇÃO DE EQUIPAMENTOS
# -----------------------------------------------------------
with tab_insp:
    st.subheader('Aplicativo de Inspeção e Rondas de Confiabilidade')
    st.markdown(
        '''
        <div class='justificado'>
        Digitalização das rotinas de inspeção sensitiva (mecânica e elétrica). O inspetor registra medições de temperatura,
        vibração preliminar, ruídos anormais e fotos de anomalias diretamente no local do ativo.
        </div>
        ''',
        unsafe_allow_html=True,
    )

    col_v, col_d = st.columns([3, 2], gap='large')
    with col_v:
        st.video('https://www.youtube.com/watch?v=ZH-m1hMfzvM&t=23s')
    with col_d:
        st.markdown('#### 🎯 Recursos Principais')
        st.markdown(
            '''
            * **Checklist Dinâmico:** Roteiro sequencial de inspeção por equipamento/linha de produção.
            * **Evidência Fotográfica:** Captura de fotos anexadas automaticamente ao registro da falha.
            * **Integração Imediata:** Alimentação direta de tabelas corporativas para disparo de OS corretiva.
            '''
        )

# -----------------------------------------------------------
# ABA 3 — CONTROLE DE FERRAMENTARIA
# -----------------------------------------------------------
with tab_ferr:
    st.subheader('Sistema Integrado de Controle e Empréstimo de Ferramentaria')
    st.markdown(
        '''
        <div class='justificado'>
        Solução completa para gestão de ativos de ferramentaria: rastreabilidade de posse, controle de estado de conservação,
        histórico de manutenções/aferições e redução de perdas de ferramentas especiais.
        </div>
        ''',
        unsafe_allow_html=True,
    )

    st.markdown('#### 📱 Fluxo de Telas do Aplicativo')
    col1, col2, col3, col4 = st.columns(4, gap='small')
    with col1:
        st.image(get_asset_path('app_ferr_01.jpeg'), caption='1. Boas-vindas e Acesso', use_container_width=True)
    with col2:
        st.image(get_asset_path('app_ferr_02.jpeg'), caption='2. Catálogo & Busca', use_container_width=True)
    with col3:
        st.image(get_asset_path('app_ferr_03.jpeg'), caption='3. Detalhes do Ativo', use_container_width=True)
    with col4:
        st.image(get_asset_path('app_ferr_04.jpeg'), caption='4. Empréstimo & Devolução', use_container_width=True)

    st.markdown('#### ⚙️ Detalhamento dos Módulos')
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        with st.expander('**1. Tela Inicial e Navegação**', expanded=False):
            st.markdown(
                '''
                * Saudação personalizada com base no perfil autenticado do usuário Microsoft 365.
                * Acesso rápido às listas de ferramentas disponíveis e pendências de entrega.
                '''
            )
        with st.expander('**2. Inventário e Pesquisa Rápida**', expanded=False):
            st.markdown(
                '''
                * Busca preditiva por nome da ferramenta, código patrimonial ou status.
                * Badges coloridos indicando disponibilidade imediata, manutenção ou empréstimo.
                * Botão de cadastro ágil de novos itens.
                '''
            )
    with c_m2:
        with st.expander('**3. Ficha Técnica e Histórico**', expanded=False):
            st.markdown(
                '''
                * Consulta rápida de fotos, modelo, última aferição e local de guarda no almoxarifado.
                * Identificação de quem está com a posse atual da ferramenta.
                '''
            )
        with st.expander('**4. Operação de Check-in e Check-out**', expanded=False):
            st.markdown(
                '''
                * Registro do solicitante, data de retirada e prazo estimado de retorno.
                * Campo de apontamento de avarias prévias para preservação de responsabilidades.
                '''
            )

# -----------------------------------------------------------
# ABA 4 — GESTÃO DE PENDÊNCIAS
# -----------------------------------------------------------
with tab_pend:
    st.subheader('Aplicativo de Gerenciamento de Pendências e Ordens de Manutenção')
    st.markdown(
        '''
        <div class='justificado'>
        Painel mobile para acompanhamento contínuo de tarefas pendentes e anomalias de chão de fábrica.
        Garante que nenhuma falha potencial caia no esquecimento entre diferentes turnos de trabalho.
        </div>
        ''',
        unsafe_allow_html=True,
    )

    st.markdown('#### 📱 Visualização da Interface')
    col1, col2, col3 = st.columns(3, gap='medium')
    with col1:
        st.image(get_asset_path('app_pend_01.jpeg'), caption='1. Portal de Entrada', use_container_width=True)
    with col2:
        st.image(get_asset_path('app_pend_02.jpeg'), caption='2. Backlog de Ocorrências', use_container_width=True)
    with col3:
        st.image(get_asset_path('app_pend_03.jpeg'), caption='3. Formulário de Abertura', use_container_width=True)

    st.markdown('#### 📋 Recursos Operacionais')
    with st.expander('**Visão Geral do Backlog e Registro**', expanded=False):
        st.markdown(
            '''
            * **Filtros por Criticidade:** Identificação imediata de pendências atrasadas, prioritárias ou de rotina.
            * **Campos Padronizados:** TAG do ativo, setor industrial, descrição do sintoma e responsável técnico designado.
            * **Controle de Prazos:** Notificação visual de prazos acordados para execução da melhoria.
            '''
        )

# -----------------------------------------------------------
# RODAPÉ
# -----------------------------------------------------------
render_footer()
