import streamlit as st
import pandas as pd
from pathlib import Path
from utils.ui import load_css, get_project_root, render_footer
from utils.business_rules import validar_alocacao

# Configuração global da página
st.set_page_config(
    page_title="Portal dos Dados - Planejador de Aulas",
    page_icon="🏫",
    layout="wide",
)

# Carregamento de estilos
load_css("style.css")


# 1. Carregamento dos Dados
@st.cache_data
def carregar_dados():
    root = get_project_root()
    data_dir = root / "data"

    # Busca arquivos primeiro em data/, depois na raiz do projeto
    def find_file(name: str):
        candidates = [data_dir / name, root / name, Path(name)]
        for c in candidates:
            if c.exists():
                return c
        return None

    f_lotacao = find_file("DB_Alocacao_Escolar_Dione_Lotacao_Ambientes.csv")
    f_ambientes = find_file("DB_Alocacao_Escolar_Dione_Ambientes.csv")
    f_docentes = find_file("DB_Alocacao_Escolar_Dione_Docentes.csv")

    if f_lotacao and f_ambientes and f_docentes:
        df_lotacao = pd.read_csv(f_lotacao)
        df_ambientes = pd.read_csv(f_ambientes)
        df_docentes = pd.read_csv(f_docentes)
    else:
        # Dados padrão de demonstração caso os arquivos originais não estejam presentes
        df_ambientes = pd.DataFrame(
            [
                {"Nome_Ambiente": "Laboratório de Informática 01", "Capacidade_Fisica": 35, "Tipo": "Informática"},
                {"Nome_Ambiente": "Laboratório de Automação", "Capacidade_Fisica": 25, "Tipo": "Técnico"},
                {"Nome_Ambiente": "Sala de Metrologia", "Capacidade_Fisica": 20, "Tipo": "Técnico"},
                {"Nome_Ambiente": "Sala de Aula 101", "Capacidade_Fisica": 40, "Tipo": "Teórica"},
                {"Nome_Ambiente": "Oficina Mecânica Industrial", "Capacidade_Fisica": 30, "Tipo": "Oficina"},
            ]
        )

        df_docentes = pd.DataFrame(
            [
                {"Nome": "Dione Nascimento", "Especialidade": "Manutenção & Ciência de Dados"},
                {"Nome": "Carlos Alberto", "Especialidade": "Automação Industrial"},
                {"Nome": "Mariana Souza", "Especialidade": "Eletrotécnica"},
                {"Nome": "Roberto Lima", "Especialidade": "Metrologia"},
            ]
        )

        df_lotacao = pd.DataFrame(
            [
                {
                    "Turma": "MEC-2024.1",
                    "Disciplina": "Gestão de Ativos",
                    "Dia da Semana": "Segunda",
                    "Turno": "Noite",
                    "Ambiente": "Laboratório de Informática 01",
                    "Docente": "Dione Nascimento",
                    "Alunos": 28,
                    "Vagas Disponíveis": 7,
                },
                {
                    "Turma": "AUT-2024.1",
                    "Disciplina": "Sensores e Atuadores",
                    "Dia da Semana": "Terça",
                    "Turno": "Noite",
                    "Ambiente": "Laboratório de Automação",
                    "Docente": "Carlos Alberto",
                    "Alunos": 22,
                    "Vagas Disponíveis": 3,
                },
                {
                    "Turma": "ELE-2024.2",
                    "Disciplina": "Eletrotécnica Geral",
                    "Dia da Semana": "Quarta",
                    "Turno": "Noite",
                    "Ambiente": "Sala de Aula 101",
                    "Docente": "Mariana Souza",
                    "Alunos": 35,
                    "Vagas Disponíveis": 5,
                },
                {
                    "Turma": "MET-2024.1",
                    "Disciplina": "Controle Dimensional",
                    "Dia da Semana": "Quinta",
                    "Turno": "Manhã",
                    "Ambiente": "Sala de Metrologia",
                    "Docente": "Roberto Lima",
                    "Alunos": 18,
                    "Vagas Disponíveis": 2,
                },
                {
                    "Turma": "MEC-2024.2",
                    "Disciplina": "PCM Aplicado",
                    "Dia da Semana": "Sexta",
                    "Turno": "Noite",
                    "Ambiente": "Oficina Mecânica Industrial",
                    "Docente": "Dione Nascimento",
                    "Alunos": 26,
                    "Vagas Disponíveis": 4,
                },
            ]
        )

    return df_lotacao, df_ambientes, df_docentes


df_lotacao_init, df_ambientes, df_docentes = carregar_dados()

if "df_lotacao" not in st.session_state:
    st.session_state["df_lotacao"] = df_lotacao_init.copy()

df_lotacao = st.session_state["df_lotacao"]

# 2. Navegação e Título
st.title("🏫 Gestão de Alocação de Ambientes e Docentes")
st.markdown("Sistema inteligente para distribuição de turmas, controle de lotação máxima e prevenção de conflitos de grade.")
st.divider()

menu = st.radio("Selecione a operação:", ["Acompanhamento de Ocupação", "Lançamento de Turma"], horizontal=True)

# 3. Interface de Acompanhamento
if menu == "Acompanhamento de Ocupação":
    st.subheader("Acompanhamento de Infraestrutura e Capacidade")

    # KPIs Rápidos
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ambientes Monitorados", len(df_ambientes))
    col2.metric("Docentes Ativos", len(df_docentes))
    col3.metric("Turmas Alocadas", len(df_lotacao))
    vagas_media = round(df_lotacao["Vagas Disponíveis"].mean(), 1) if not df_lotacao.empty else 0
    col4.metric("Vagas Remanescentes (Média)", vagas_media)

    st.markdown("---")

    # Filtros para análise de dados
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        dias_disponiveis = ["Todos"] + list(df_lotacao["Dia da Semana"].dropna().unique())
        dia_selecionado = st.selectbox("Filtrar por Dia da Semana:", dias_disponiveis)
    with col_f2:
        turnos_disponiveis = ["Todos"] + list(df_lotacao["Turno"].dropna().unique())
        turno_selecionado = st.selectbox("Filtrar por Turno:", turnos_disponiveis)

    df_exibicao = df_lotacao
    if dia_selecionado != "Todos":
        df_exibicao = df_exibicao[df_exibicao["Dia da Semana"] == dia_selecionado]
    if turno_selecionado != "Todos":
        df_exibicao = df_exibicao[df_exibicao["Turno"] == turno_selecionado]

    st.dataframe(df_exibicao, use_container_width=True)

    # Exportação dos Dados
    csv_bytes = df_lotacao.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Exportar Grade Completa (CSV)",
        data=csv_bytes,
        file_name="grade_alocacao_turmas.csv",
        mime="text/csv",
    )

# 4. Interface de Lançamento
elif menu == "Lançamento de Turma":
    st.subheader("Nova Alocação de Turma com Validação de Regras")

    with st.form("form_nova_alocacao"):
        st.markdown("##### Dados da Alocação")
        col1, col2 = st.columns(2)

        with col1:
            dia = st.selectbox("Dia da Semana", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"])
            turno = st.selectbox("Turno", ["Manhã", "Tarde", "Noite"])
            horario = st.time_input("Horário de Início")
            turma_id = st.text_input("Identificação da Turma (Ex: MEC-2024.1)")

        with col2:
            ambiente = st.selectbox("Ambiente Destino", df_ambientes["Nome_Ambiente"].tolist())
            docente = st.selectbox("Docente Designado", df_docentes["Nome"].tolist())
            disciplina = st.text_input("Disciplina")
            alunos_alocados = st.number_input("Quantidade de Alunos", min_value=1, step=1, value=25)

        submitted = st.form_submit_button("Validar e Registrar Alocação", type="primary")

        # 5. Validação de Regras de Negócio e Conflitos
        if submitted:
            if not turma_id or not disciplina:
                st.error("Preencha a identificação da turma e a disciplina.")
            else:
                valido, msg_erro, vagas = validar_alocacao(
                    st.session_state["df_lotacao"],
                    df_ambientes,
                    dia,
                    turno,
                    ambiente,
                    docente,
                    alunos_alocados,
                )

                if not valido:
                    st.error(msg_erro)
                else:
                    nova_linha = {
                        "Turma": turma_id,
                        "Disciplina": disciplina,
                        "Dia da Semana": dia,
                        "Turno": turno,
                        "Ambiente": ambiente,
                        "Docente": docente,
                        "Alunos": int(alunos_alocados),
                        "Vagas Disponíveis": vagas,
                    }
                    st.session_state["df_lotacao"] = pd.concat(
                        [st.session_state["df_lotacao"], pd.DataFrame([nova_linha])],
                        ignore_index=True,
                    )
                    st.success(f"✅ Alocação da turma '{turma_id}' registrada com sucesso!")
                    st.info(f"Vagas remanescentes no ambiente '{ambiente}': **{vagas}**")

render_footer()