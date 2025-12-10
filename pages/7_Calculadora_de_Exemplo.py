from io import BytesIO
import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
import plotly.express as px


# Página limpa e canônica para o dashboard MS Project
st.set_page_config(
    page_title="Dashboard de Projetos - MS Project", layout="wide")


def carregar_dados_exemplo():
    data = {
        'Tarefa': [
            'Levantamento de Requisitos', 'Design do Banco de Dados',
            'Desenvolvimento Backend', 'Desenvolvimento Frontend',
            'Testes', 'Implantação'
        ],
        'Inicio': ['2023-10-01', '2023-10-05', '2023-10-10', '2023-10-15', '2023-10-25', '2023-11-01'],
        'Fim': ['2023-10-05', '2023-10-10', '2023-10-25', '2023-10-30', '2023-11-01', '2023-11-05'],
        'Recurso': ['Ana (Analista)', 'Carlos (DBA)', 'Beatriz (Dev)', 'Beatriz (Dev)', 'QA Team', 'DevOps'],
        'Conclusao': [100, 100, 60, 40, 0, 0]
    }
    df = pd.DataFrame(data)
    df['Inicio'] = pd.to_datetime(df['Inicio'])
    df['Fim'] = pd.to_datetime(df['Fim'])
    return df


# Página 7: Visualizador MS Project (versão limpa)
st.set_page_config(
    page_title="Dashboard de Projetos - MS Project", layout="wide")


def carregar_dados_exemplo():
    """Gera dados de exemplo"""
    data = {
        'Tarefa': [
            'Levantamento de Requisitos', 'Design do Banco de Dados',
            'Desenvolvimento Backend', 'Desenvolvimento Frontend',
            'Testes', 'Implantação'
        ],
        'Inicio': ['2023-10-01', '2023-10-05', '2023-10-10', '2023-10-15', '2023-10-25', '2023-11-01'],
        'Fim': ['2023-10-05', '2023-10-10', '2023-10-25', '2023-10-30', '2023-11-01', '2023-11-05'],
        'Recurso': ['Ana (Analista)', 'Carlos (DBA)', 'Beatriz (Dev)', 'Beatriz (Dev)', 'QA Team', 'DevOps'],
        'Conclusao': [100, 100, 60, 40, 0, 0]
    }
    df = pd.DataFrame(data)
    df['Inicio'] = pd.to_datetime(df['Inicio'])
    df['Fim'] = pd.to_datetime(df['Fim'])
    return df


def processar_arquivo_excel(uploaded_file):
    """Lê e normaliza o Excel exportado do MS Project (mapeia nomes de colunas comuns)."""
    try:
        df = pd.read_excel(uploaded_file)
        mapa_colunas = {
            'Name': 'Tarefa', 'Nome': 'Tarefa',
            'Start': 'Inicio', 'Início': 'Inicio',
            'Finish': 'Fim', 'Término': 'Fim',
            'Resource Names': 'Recurso', 'Nomes dos Recursos': 'Recurso',
            '% Complete': 'Conclusao', '% Concluído': 'Conclusao'
        }
        df.rename(columns=mapa_colunas, inplace=True)
        if 'Inicio' in df.columns:
            df['Inicio'] = pd.to_datetime(df['Inicio'])
        if 'Fim' in df.columns:
            df['Fim'] = pd.to_datetime(df['Fim'])
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None


st.title("📊 Visualizador de Projetos (MS Project)")
st.markdown(
    """
    Esta aplicação transforma dados de projetos em dashboards gerenciais.
    **Como usar:** Exporte seu MS Project para **Excel** e faça o upload abaixo.
    """
)


with st.sidebar:
    st.header("Upload de Arquivo")
    uploaded_file = st.file_uploader(
        "Carregar arquivo Excel (.xlsx)", type=["xlsx"], key="uploader_msproject_7"
    )
    usar_exemplo = st.checkbox(
        "Usar dados de exemplo", value=True, key="usar_exemplo_7")


df = None
if uploaded_file is not None:
    df = processar_arquivo_excel(uploaded_file)
elif usar_exemplo:
    df = carregar_dados_exemplo()


if df is not None:
    col1, col2, col3, col4 = st.columns(4)
    total_tarefas = len(df)
    inicio_projeto = df['Inicio'].min().strftime(
        '%d/%m/%Y') if 'Inicio' in df.columns else '-'
    fim_projeto = df['Fim'].max().strftime(
        '%d/%m/%Y') if 'Fim' in df.columns else '-'
    media_conclusao = df['Conclusao'].mean(
    ) if 'Conclusao' in df.columns else 0

    col1.metric("Total de Tarefas", total_tarefas)
    col2.metric("Início do Projeto", inicio_projeto)
    col3.metric("Fim Previsto", fim_projeto)
    col4.metric("Progresso Geral", f"{media_conclusao:.1f}%")

    st.divider()

    st.subheader("📅 Cronograma Interativo (Gantt)")
    # Plotly Gantt (timeline)
    fig_gantt = px.timeline(
        df,
        x_start="Inicio",
        x_end="Fim",
        y="Tarefa",
        color="Conclusao",
        hover_data=["Recurso", "Conclusao"],
        color_continuous_scale="RdBu",
        title="Cronograma de Execução",
    )
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt, width='stretch')

    st.subheader("👥 Carga de Trabalho por Recurso")
    recursos_df = df['Recurso'].value_counts().reset_index()
    recursos_df.columns = ['Recurso', 'Qtd Tarefas']
    fig_bar = px.bar(recursos_df, x='Recurso',
                     y='Qtd Tarefas', color='Qtd Tarefas')
    st.plotly_chart(fig_bar, width='stretch')

    with st.expander("Ver dados brutos"):
        st.dataframe(df)
else:
    st.info("Aguardando carregamento de dados...")


# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Projetos - MS Project", layout="wide")


# --- Funções Auxiliares ---
def carregar_dados_exemplo():
    """Gera dados falsos para demonstração se o usuário não tiver um arquivo."""
    data = {
        'Tarefa': ['Levantamento de Requisitos', 'Design do Banco de Dados', 'Desenvolvimento Backend', 'Desenvolvimento Frontend', 'Testes', 'Implantação'],
        'Inicio': ['2023-10-01', '2023-10-05', '2023-10-10', '2023-10-15', '2023-10-25', '2023-11-01'],
        'Fim': ['2023-10-05', '2023-10-10', '2023-10-25', '2023-10-30', '2023-11-01', '2023-11-05'],
        'Recurso': ['Ana (Analista)', 'Carlos (DBA)', 'Beatriz (Dev)', 'Beatriz (Dev)', 'QA Team', 'DevOps'],
        'Conclusao': [100, 100, 60, 40, 0, 0]
    }
    df = pd.DataFrame(data)
    df['Inicio'] = pd.to_datetime(df['Inicio'])
    df['Fim'] = pd.to_datetime(df['Fim'])
    return df


def processar_arquivo_excel(uploaded_file):
    """Lê o arquivo Excel exportado do MS Project."""
    try:
        df = pd.read_excel(uploaded_file)
        mapa_colunas = {
            'Name': 'Tarefa', 'Nome': 'Tarefa',
            'Start': 'Inicio', 'Início': 'Inicio',
            'Finish': 'Fim', 'Término': 'Fim',
            'Resource Names': 'Recurso', 'Nomes dos Recursos': 'Recurso',
            '% Complete': 'Conclusao', '% Concluído': 'Conclusao'
        }
        df.rename(columns=mapa_colunas, inplace=True)
        df['Inicio'] = pd.to_datetime(df['Inicio'])
        df['Fim'] = pd.to_datetime(df['Fim'])
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None


# --- Interface Principal ---
st.title("📊 Visualizador de Projetos (MS Project)")
st.markdown("""
Esta aplicação transforma dados de projetos em dashboards gerenciais.
**Como usar:** Exporte seu MS Project para **Excel** e faça o upload abaixo.
""")


# Sidebar para Upload
with st.sidebar:
    st.header("Upload de Arquivo")
    uploaded_file = st.file_uploader(
        "Carregar arquivo Excel (.xlsx)", type=["xlsx"])
    usar_exemplo = st.checkbox("Usar dados de exemplo", value=True)


# Lógica de Carregamento
df = None
if uploaded_file is not None:
    df = processar_arquivo_excel(uploaded_file)
elif usar_exemplo:
    df = carregar_dados_exemplo()


# Dashboard
if df is not None:
    col1, col2, col3, col4 = st.columns(4)
    total_tarefas = len(df)
    inicio_projeto = df['Inicio'].min().strftime('%d/%m/%Y')
    fim_projeto = df['Fim'].max().strftime('%d/%m/%Y')
    media_conclusao = df['Conclusao'].mean()

    col1.metric("Total de Tarefas", total_tarefas)
    col2.metric("Início do Projeto", inicio_projeto)
    col3.metric("Fim Previsto", fim_projeto)
    col4.metric("Progresso Geral", f"{media_conclusao:.1f}%")

    st.divider()

    st.subheader("📅 Cronograma Interativo (Gantt)")
    fig_gantt = px.timeline(
        df,
        x_start="Inicio",
        x_end="Fim",
        y="Tarefa",
        color="Conclusao",
        hover_data=["Recurso", "Conclusao"],
        color_continuous_scale="RdBu",
        title="Cronograma de Execução"
    )
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt, use_container_width=True)

    st.subheader("👥 Carga de Trabalho por Recurso")
    recursos_df = df['Recurso'].value_counts().reset_index()
    recursos_df.columns = ['Recurso', 'Qtd Tarefas']
    fig_bar = px.bar(recursos_df, x='Recurso',
                     y='Qtd Tarefas', color='Qtd Tarefas')
    st.plotly_chart(fig_bar, use_container_width=True)

    with st.expander("Ver dados brutos"):
        st.dataframe(df)
else:
    st.info("Aguardando carregamento de dados...")


def processar_arquivo_excel(uploaded_file):
    """Lê o arquivo Excel exportado do MS Project."""
    try:
        df = pd.read_excel(uploaded_file)
        mapa_colunas = {
            'Name': 'Tarefa', 'Nome': 'Tarefa',
            'Start': 'Inicio', 'Início': 'Inicio',
            'Finish': 'Fim', 'Término': 'Fim',
            'Resource Names': 'Recurso', 'Nomes dos Recursos': 'Recurso',
            '% Complete': 'Conclusao', '% Concluído': 'Conclusao'
        }
        df.rename(columns=mapa_colunas, inplace=True)
        df['Inicio'] = pd.to_datetime(df['Inicio'])
        df['Fim'] = pd.to_datetime(df['Fim'])
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None


# --- Interface Principal ---
st.title("📊 Visualizador de Projetos (MS Project)")
st.markdown("""
Esta aplicação transforma dados de projetos em dashboards gerenciais.
**Como usar:** Exporte seu MS Project para **Excel** e faça o upload abaixo.
""")


# Sidebar para Upload
with st.sidebar:
    st.header("Upload de Arquivo")
    uploaded_file = st.file_uploader(
        "Carregar arquivo Excel (.xlsx)", type=["xlsx"])
    usar_exemplo = st.checkbox("Usar dados de exemplo", value=True)


# Lógica de Carregamento
df = None
if uploaded_file is not None:
    df = processar_arquivo_excel(uploaded_file)
elif usar_exemplo:
    df = carregar_dados_exemplo()


# Dashboard
if df is not None:
    col1, col2, col3, col4 = st.columns(4)
    total_tarefas = len(df)
    inicio_projeto = df['Inicio'].min().strftime('%d/%m/%Y')
    fim_projeto = df['Fim'].max().strftime('%d/%m/%Y')
    media_conclusao = df['Conclusao'].mean()

    col1.metric("Total de Tarefas", total_tarefas)
    col2.metric("Início do Projeto", inicio_projeto)
    col3.metric("Fim Previsto", fim_projeto)
    col4.metric("Progresso Geral", f"{media_conclusao:.1f}%")

    st.divider()

    st.subheader("📅 Cronograma Interativo (Gantt)")
    fig_gantt = px.timeline(
        df,
        x_start="Inicio",
        x_end="Fim",
        y="Tarefa",
        color="Conclusao",
        hover_data=["Recurso", "Conclusao"],
        color_continuous_scale="RdBu",
        title="Cronograma de Execução"
    )
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt, use_container_width=True)

    st.subheader("👥 Carga de Trabalho por Recurso")
    recursos_df = df['Recurso'].value_counts().reset_index()
    recursos_df.columns = ['Recurso', 'Qtd Tarefas']
    fig_bar = px.bar(recursos_df, x='Recurso',
                     y='Qtd Tarefas', color='Qtd Tarefas')
    st.plotly_chart(fig_bar, use_container_width=True)

    with st.expander("Ver dados brutos"):
        st.dataframe(df)
else:
    st.info("Aguardando carregamento de dados...")
