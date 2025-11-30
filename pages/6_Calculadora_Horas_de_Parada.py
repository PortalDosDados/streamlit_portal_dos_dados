import streamlit as st
from datetime import datetime, timedelta, time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="MachineFlow | Pro",
    page_icon="🏭",
    layout="wide"
)

# --- 2. IMPORTAÇÃO DO SEU CSS ORIGINAL ---
def carregar_css(nome_arquivo):
    try:
        with open(nome_arquivo, encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Arquivo style.css não encontrado. O estilo padrão será aplicado.")

carregar_css('style.css')

# --- 3. AJUSTES DE LAYOUT (Apenas geometria, sem cores) ---
# Aqui definimos apenas TAMANHO e ALINHAMENTO para melhorar a UX
st.markdown("""
<style>
    /* Aumenta a fonte e centraliza para facilitar a digitação */
    .stTextInput input {
        font-family: 'Courier New', monospace; /* Fonte boa para números */
        font-weight: bold;
        font-size: 1.4rem;
        text-align: center;
        padding: 10px;
    }

    /* Botão mais alto para facilitar o clique */
    .stButton button {
        width: 100%;
        height: 3.5rem;
        font-weight: bold;
        font-size: 1.1rem;
    }

    /* Remove labels pequenos padrão para usarmos nossos títulos H3 */
    .stTextInput label {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. FUNÇÃO LÓGICA ---
def parse_horario(valor):
    if not valor: return None, ""
    nums = ''.join(filter(str.isdigit, str(valor)))
    try:
        if len(nums) == 4: h, m = int(nums[:2]), int(nums[2:])
        elif len(nums) == 3: h, m = int(nums[:1]), int(nums[1:])
        elif len(nums) <= 2 and nums != "": h, m = int(nums), 0
        else: return None, valor
        if 0 <= h <= 23 and 0 <= m <= 59:
            return time(h, m), f"{h:02d}:{m:02d}"
        return None, valor
    except: return None, valor

# --- 5. INTERFACE ---

st.title("🏭 Controle de Parada")
st.markdown("Digite os horários e processe o cálculo.")
st.divider()

# Container dos Inputs
with st.container():
    col1, col2 = st.columns(2, gap="large")

    with col1:
        # Usando Markdown para títulos em vez de labels do input
        st.markdown("### 🔴 Início")
        d_ini = st.date_input("Data Início", datetime.now(), format="DD/MM/YYYY", key="d_ini")
        t_ini_str = st.text_input("Hora Início", placeholder="08:00", max_chars=5, key="input_ini")

    with col2:
        st.markdown("### 🟢 Fim")
        d_fim = st.date_input("Data Fim", datetime.now(), format="DD/MM/YYYY", key="d_fim")
        t_fim_str = st.text_input("Hora Fim", placeholder="17:30", max_chars=5, key="input_fim")

# --- 6. BOTÃO DE AÇÃO (ALINHADO À ESQUERDA) ---
st.write("")
# Criamos duas colunas iguais. O botão fica na primeira (esquerda)
# e a segunda fica vazia ( _ ), mantendo o alinhamento com o input de cima.
col_btn_esquerda, col_vazia = st.columns(2, gap="large")

with col_btn_esquerda:
    # type="primary" vai puxar a cor principal definida no seu tema/config
    calcular = st.button("⚙️ PROCESSAR DADOS", type="primary")

# --- 7. PROCESSAMENTO E CARD DE RESULTADO ---
if calcular:
    obj_t_ini, str_t_ini = parse_horario(t_ini_str)
    obj_t_fim, str_t_fim = parse_horario(t_fim_str)

    if not obj_t_ini or not obj_t_fim:
        st.error("❌ Formato inválido. Use HHMM (ex: 14:30).")
    else:
        dt_ini = datetime.combine(d_ini, obj_t_ini)
        dt_fim = datetime.combine(d_fim, obj_t_fim)

        if dt_fim < dt_ini:
             st.warning("⚠️ Data final menor que a inicial.")
        else:
            duracao = dt_fim - dt_ini
            segundos = duracao.total_seconds()
            horas_decimais = segundos / 3600
            minutos_totais = int(segundos // 60)

            # Definindo cor da borda (Semáforo)
            if horas_decimais > 1.5:
                cor_borda = "#ef5350" # Vermelho status
                texto_status = "REALIZAR ANÁLISE DE FALHA"
            elif horas_decimais > 1:
                cor_borda = "#ffa726" # Laranja status
                texto_status = "REALIZAR ANÁLISE FCA"
            else:
                cor_borda = "#66bb6a" # Verde status
                texto_status = "REALIZAR APONTAMENTO NO RELATÓRIO DE TURNO"

            st.write("")

            # --- CARD HTML ---
            st.markdown(f"""
            <div style="
                border: 1px solid #ddd;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                background-color: white;
                border-top: 8px solid {cor_borda};
                text-align: center;
                max-width: 700px;
                margin: 0 auto;
                color: #333;
            ">
                <div style="font-size: 0.9rem; text-transform: uppercase; color: #888; margin-bottom: 5px;">
                    Duração da Parada ({texto_status})
                </div>
                <div style="display: flex; justify-content: center; align-items: baseline; gap: 10px;">
                    <span style="font-size: 4rem; font-weight: 800; color: #333;">
                        {horas_decimais:.2f}
                    </span>
                    <span style="font-size: 1.2rem; color: #666;">horas</span>
                </div>
                <div style="margin-top: 10px; font-weight: bold; color: #555;">
                    ⏱️ Total: {minutos_totais} minutos
                </div>
                <hr style="margin: 20px 0; border: 0; border-top: 1px solid #eee;">
                <div style="font-size: 0.85rem; color: #999;">
                    Período: {str_t_ini} às {str_t_fim}
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.toast("Cálculo realizado.", icon="✅")