import streamlit as st
from datetime import datetime

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title=" Portal dos Dados - Calculadora 52 Semanas",
    page_icon="📅",
    layout="wide",  # <--- MUDANÇA AQUI (era 'centered')
)


# --- 2. IMPORTAÇÃO DO CSS EXTERNO ---
def carregar_css(nome_arquivo):
    # A MUDANÇA ESTÁ AQUI: adicionamos encoding='utf-8'
    with open(nome_arquivo, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Chamada da função (certifique-se que style.css está na mesma pasta)
carregar_css("style.css")

# --- 3. INTERFACE E LÓGICA ---
st.title("📅 Calculadora de Datas")
st.markdown("Converta datas para **Padrões de Negócio** instantaneamente.")
st.divider()

with st.container():
    col_input, col_vazia = st.columns([0.5, 1])

    with col_input:
        data_input = st.date_input(
            "Selecione a Data:", datetime.now(), format="DD/MM/YYYY"
        )

    # --- LÓGICA DE CÁLCULO ---
    ano_iso, semana_iso, dia_num_iso = data_input.isocalendar()
    dia_do_ano = data_input.timetuple().tm_yday

    dias_pt = {
        0: "Segunda-feira",
        1: "Terça-feira",
        2: "Quarta-feira",
        3: "Quinta-feira",
        4: "Sexta-feira",
        5: "Sábado",
        6: "Domingo",
    }
    nome_dia_semana = dias_pt[data_input.weekday()]

    st.write("")

    # Exibição dos Resultados (O CSS externo vai estilizar isso aqui)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Semana do Ano", value=f"S{semana_iso:02d}")

    with col2:
        st.metric(label="Dia do Ano", value=f"Dia {dia_do_ano}")

    with col3:
        st.metric(label="Dia da Semana", value=nome_dia_semana)

# --- 4. RODAPÉ ---
st.caption(
    "Nota: Semana ISO inicia na segunda-feira. Útil para planejamento de sprints e logística."
)

# Imagem de fundo (certifique-se que a pasta assets existe)
st.image("./assets/fundo.jpg", use_container_width=True)
