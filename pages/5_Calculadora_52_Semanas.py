import streamlit as st
from datetime import datetime

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="WeekFlow | Calculadora",
    page_icon="📅",
    layout="centered"
)

# --- 2. ESTILIZAÇÃO (CSS) ---
st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: #f0f2f6;
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    @media (prefers-color-scheme: dark) {
        div[data-testid="stMetric"] {
            background-color: #262730;
        }
    }
    div[data-testid="stMetricValue"] { 
        font-size: 1.8rem !important; /* Leve ajuste para caber nomes longos */
        font-weight: 700; 
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. INTERFACE E LÓGICA ---
st.title("📅 Calculadora de Datas")
st.markdown("Converta datas para **Padrões de Negócio** instantaneamente.")
st.divider()

with st.container():
    col_input, col_vazia = st.columns([2, 1])
    
    with col_input:
        data_input = st.date_input(
            "Selecione a Data:", 
            datetime.now(), 
            format="DD/MM/YYYY"
        )

    # --- LÓGICA DE CÁLCULO ---
    # 1. Semana ISO
    ano_iso, semana_iso, dia_num_iso = data_input.isocalendar()
    
    # 2. Dia do Ano
    dia_do_ano = data_input.timetuple().tm_yday
    
    # 3. Dia da Semana (Tradução Manual)
    # .weekday() retorna 0 para Segunda e 6 para Domingo
    dias_pt = {
        0: 'Segunda-feira',
        1: 'Terça-feira',
        2: 'Quarta-feira',
        3: 'Quinta-feira',
        4: 'Sexta-feira',
        5: 'Sábado',
        6: 'Domingo'
    }
    nome_dia_semana = dias_pt[data_input.weekday()]

    st.write("") 
    
    # Exibição dos Resultados
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Semana do Ano", value=f"S{semana_iso:02d}")
        
    with col2:
        st.metric(label="Dia do Ano", value=f"Dia {dia_do_ano}")
        
    with col3:
        # AQUI ESTÁ A MUDANÇA
        st.metric(label="Dia da Semana", value=nome_dia_semana)

# --- 4. RODAPÉ ---
st.caption("Nota: Semana ISO inicia na segunda-feira. Útil para planejamento de sprints e logística.")