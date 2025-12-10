import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================================
# 1. CONFIGURAÇÃO GERAL DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Portal dos Dados - Cronograma de Projetos",
    page_icon="📅",
    layout="wide",
)


# ============================================================================
# 2. FUNÇÕES AUXILIARES
# ============================================================================


def carregar_dados_exemplo():
    """Gera um DataFrame de exemplo para demonstração."""
    # Exemplo voltado para manutenção industrial
    data = {
        "Tarefa": [
            "Parada Programada - Linha de Produção 1",
            "Troca de Rolamentos - Compressor A",
            "Inspeção Elétrica - Subestação",
            "Calibração Instrumentação - Tanque T-5",
            "Manutenção Preventiva - Motor M2",
            "Teste e Comissionamento - Sistema de Combustão",
        ],
        "Inicio": [
            "2025-11-10",
            "2025-11-12",
            "2025-11-15",
            "2025-11-20",
            "2025-11-25",
            "2025-12-02",
        ],
        "Fim": [
            "2025-11-11",
            "2025-11-13",
            "2025-11-16",
            "2025-11-20",
            "2025-11-26",
            "2025-12-05",
        ],
        "Recurso": [
            "Equipe Mecânica",
            "Fornecedor (OEM)",
            "Equipe Elétrica",
            "Técnico de Instrumentação",
            "Equipe Mecânica",
            "Equipe de Comissionamento",
        ],
        "Conclusao": [100, 80, 100, 60, 40, 20],
    }
    df = pd.DataFrame(data)
    df["Inicio"] = pd.to_datetime(df["Inicio"])
    df["Fim"] = pd.to_datetime(df["Fim"])
    return df


def processar_arquivo_excel(uploaded_file):
    """Lê e normaliza um Excel exportado do MS Project.

    Valida presença das colunas obrigatórias e mapeia nomes comuns.
    Retorna `None` e exibe uma mensagem caso falte alguma coluna necessária.
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
        # Normalização simples de nomes (remove acentos, espaços extras e lowercase)

        def norm(col: str) -> str:
            if not isinstance(col, str):
                return ""
            s = col.strip().lower()
            s = unicodedata.normalize("NFKD", s)
            s = "".join(ch for ch in s if not unicodedata.combining(ch))
            return s

        cols_norm = {norm(c): c for c in df.columns}

        # Colunas esperadas pelo usuário (nomes preferenciais)
        required = [
            "nome da tarefa",
            "duracao",
            "início",
            "termino",
            "predecessoras",
            "nomes dos recursos",
            "% concluido",
        ]

        # Também aceite variações sem acento / alternativas comuns
        alias_map = {
            "name": "nome da tarefa",
            "nome": "nome da tarefa",
            "start": "início",
            "inicio": "início",
            "finish": "termino",
            "termino": "termino",
            "resource names": "nomes dos recursos",
            "nomes dos recursos": "nomes dos recursos",
            "% complete": "% concluido",
            "% concluido": "% concluido",
            "% concluido": "% concluido",
        }

        # Build mapping from existing df columns to preferred canonical names
        col_rename = {}
        for n_norm, orig in cols_norm.items():
            if n_norm in alias_map:
                canonical = alias_map[n_norm]
                col_rename[orig] = canonical
            elif n_norm in required:
                col_rename[orig] = n_norm

        # Check which required canonical names are present after mapping
        present = set(col_rename.values())
        missing = [r for r in required if r not in present]
        if missing:
            st.error(
                f"Colunas obrigatórias ausentes no arquivo: {', '.join(missing)}.\n"
                "Renomeie as colunas ou use o template de importação."
            )
            return None

        # Renomear para nomes internos consistentes (sem acentos)
        rename_to_internal = {
            "nome da tarefa": "Tarefa",
            "duracao": "Duracao",
            "início": "Inicio",
            "inicio": "Inicio",
            "termino": "Fim",
            "término": "Fim",
            "predecessoras": "Predecessoras",
            "nomes dos recursos": "Recurso",
            "% concluido": "Conclusao",
        }

        # Apply renames
        df.rename(
            columns={
                orig: rename_to_internal[canon] for orig, canon in col_rename.items()
            },
            inplace=True,
        )

        # Convert dates
        if "Inicio" in df.columns:
            df["Inicio"] = pd.to_datetime(df["Inicio"], errors="coerce")
        if "Fim" in df.columns:
            df["Fim"] = pd.to_datetime(df["Fim"], errors="coerce")

        return df


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
            **Colunas OBRIGATÓRIAS (nomes esperados no Excel)**

            - `Nome da Tarefa`
            - `Duração`
            - `Início`
            - `Término`
            - `Predecessoras`
            - `Nomes dos Recursos`
            - `% Concluído`

            O dashboard exige essas colunas (use os nomes com acentuação como mostrado).
            Caso seu arquivo use outros nomes, o sistema tentará mapear algumas variações
            automaticamente, mas é recomendado seguir exatamente este padrão.
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
