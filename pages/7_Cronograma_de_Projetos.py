from io import BytesIO
import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
import plotly.express as px


# Página limpa e canônica para o dashboard MS Project
import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Cronograma de Projetos", layout="wide")


def carregar_dados_exemplo():
    """Gera um DataFrame de exemplo para demonstração."""
    data = {
        "Tarefa": [
            "Levantamento de Requisitos",
            "Design do Banco de Dados",
            "Desenvolvimento Backend",
            "Desenvolvimento Frontend",
            "Testes",
            "Implantação",
        ],
        "Inicio": [
            "2023-10-01",
            "2023-10-05",
            "2023-10-10",
            "2023-10-15",
            "2023-10-25",
            "2023-11-01",
        ],
        "Fim": [
            "2023-10-05",
            "2023-10-10",
            "2023-10-25",
            "2023-10-30",
            "2023-11-01",
            "2023-11-05",
        ],
        "Recurso": [
            "Ana (Analista)",
            "Carlos (DBA)",
            "Beatriz (Dev)",
            "Beatriz (Dev)",
            "QA Team",
            "DevOps",
        ],
        "Conclusao": [100, 100, 60, 40, 0, 0],
    }
    df = pd.DataFrame(data)
    df["Inicio"] = pd.to_datetime(df["Inicio"])
    df["Fim"] = pd.to_datetime(df["Fim"])
    return df


def processar_arquivo_excel(uploaded_file):
    """Lê e normaliza um Excel exportado do MS Project.

    Mapeia colunas comuns para `Tarefa`, `Inicio`, `Fim`, `Recurso` e `Conclusao`.
    """
    try:
        df = pd.read_excel(uploaded_file)
        mapa_colunas = {
            "Name": "Tarefa",
            "Nome": "Tarefa",
            "Start": "Inicio",
            "Início": "Inicio",
            "Finish": "Fim",
            "Término": "Fim",
            "Resource Names": "Recurso",
            "Nomes dos Recursos": "Recurso",
            "% Complete": "Conclusao",
            "% Concluído": "Conclusao",
        }
        df.rename(columns=mapa_colunas, inplace=True)
        if "Inicio" in df.columns:
            df["Inicio"] = pd.to_datetime(df["Inicio"])
        if "Fim" in df.columns:
            df["Fim"] = pd.to_datetime(df["Fim"])
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None


def main():
    st.title("📊 Cronograma de Projetos (MS Project)")
    st.markdown(
        """
        Esta página transforma dados de projetos em um cronograma interativo (Gantt)
        e em um gráfico de carga por recurso. Exporte seu MS Project para Excel
        e faça o upload para visualizar.
        """
    )

    with st.sidebar:
        st.header("Upload de Arquivo")
        uploaded_file = st.file_uploader(
            "Carregar arquivo Excel (.xlsx)", type=["xlsx"], key="uploader_7_cronograma"
        )
        usar_exemplo = st.checkbox(
            "Usar dados de exemplo", value=True, key="usar_exemplo_7_cronograma"
        )
        st.markdown(
            """
            **Colunas esperadas no arquivo Excel**

            - **Tarefa** (ou `Name`, `Nome`)
            - **Inicio** (ou `Start`, `Início`) — formato `YYYY-MM-DD` ou data do Excel
            - **Fim** (ou `Finish`, `Término`)
            - **Recurso** (ou `Resource Names`, `Nomes dos Recursos`)
            - **Conclusao** (ou `% Complete`, `% Concluído`) — valor numérico (0-100)

            O app tenta mapear colunas comuns automaticamente; garanta que seu arquivo
            contenha ao menos `Tarefa`, `Inicio` e `Fim`.
            """
        )

    df = None
    if uploaded_file is not None:
        df = processar_arquivo_excel(uploaded_file)
    elif usar_exemplo:
        df = carregar_dados_exemplo()

    if df is None:
        st.info("Aguardando carregamento de dados...")
        return

    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    total_tarefas = len(df)
    inicio_projeto = (
        df["Inicio"].min().strftime("%d/%m/%Y") if "Inicio" in df.columns else "-"
    )
    fim_projeto = df["Fim"].max().strftime("%d/%m/%Y") if "Fim" in df.columns else "-"
    media_conclusao = df["Conclusao"].mean() if "Conclusao" in df.columns else 0

    col1.metric("Total de Tarefas", total_tarefas)
    col2.metric("Início do Projeto", inicio_projeto)
    col3.metric("Fim Previsto", fim_projeto)
    col4.metric("Progresso Geral", f"{media_conclusao:.1f}%")

    st.divider()

    # Gantt
    st.subheader("📅 Cronograma Interativo (Gantt)")
    fig_gantt = px.timeline(
        df,
        x_start="Inicio",
        x_end="Fim",
        y="Tarefa",
        color="Conclusao" if "Conclusao" in df.columns else None,
        hover_data=[c for c in ["Recurso", "Conclusao"] if c in df.columns],
        color_continuous_scale="RdBu",
        title="Cronograma de Execução",
    )
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt, use_container_width=True, key="gantt_7_cronograma")

    # Carga por recurso
    st.subheader("👥 Carga de Trabalho por Recurso")
    if "Recurso" in df.columns:
        recursos_df = df["Recurso"].value_counts().reset_index()
        recursos_df.columns = ["Recurso", "Qtd Tarefas"]
        fig_bar = px.bar(recursos_df, x="Recurso", y="Qtd Tarefas", color="Qtd Tarefas")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_7_cronograma")
    else:
        st.info("Coluna 'Recurso' não encontrada nos dados.")

    with st.expander("Ver dados brutos"):
        st.dataframe(df)


if __name__ == "__main__":
    main()
