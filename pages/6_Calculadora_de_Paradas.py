import streamlit as st
from datetime import datetime, timedelta, time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title='Portal dos Dados - Calculadora de Paradas',
    page_icon='🏭',
    layout='wide'
)

# --- 2. IMPORTAÇÃO DO CSS EXTERNO ---
def carregar_css(nome_arquivo):
    try:
        with open(nome_arquivo, encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning('⚠️ Arquivo style.css não encontrado.')

carregar_css('style.css')

# Injeção de CSS específico para os inputs (Layout Geométrico)
st.markdown('''
<style>
    /* Estilo numérico "retrô" e centralizado */
    .stTextInput input {
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 1.4rem;
        text-align: center;
        padding: 10px;
    }
    /* Botão robusto */
    .stButton button {
        width: 100%;
        height: 3.5rem;
        font-weight: bold;
        font-size: 1.1rem;
    }
    /* Oculta labels padrão para usar Markdown personalizado */
    .stTextInput label { display: none; }
</style>
''', unsafe_allow_html=True)

# --- 3. INTERFACE E LÓGICA ---
st.title('🏭 Controle de Parada')
st.markdown('Digite os horários e processe o cálculo de **Downtime**.')
st.divider()

# Função auxiliar de parsing (mantida interna para organização)
def parse_horario(valor):
    if not valor: return None, ''
    nums = ''.join(filter(str.isdigit, str(valor)))
    try:
        if len(nums) == 4: h, m = int(nums[:2]), int(nums[2:])
        elif len(nums) == 3: h, m = int(nums[:1]), int(nums[1:])
        elif len(nums) <= 2 and nums != '': h, m = int(nums), 0
        else: return None, valor
        if 0 <= h <= 23 and 0 <= m <= 59:
            return time(h, m), f'{h:02d}:{m:02d}' # Mantém o separador :
        return None, valor
    except: return None, valor


# --- ÁREA DE INPUTS (Seguindo o padrão de colunas do exemplo) ---
with st.container():
    # Usando a proporção [0.5, 1] ou [1, 1] controlada para não esticar demais
    # No seu exemplo de data era [0.5, 1], aqui como são dois inputs lado a lado,
    # faremos um bloco contido.

    col_inputs, col_vazia = st.columns([2, 1]) # Ajuste de foco visual

    with col_inputs:
        c1, c2 = st.columns(2, gap='large')

        with c1:
            st.markdown('### 🔴 Início')
            d_ini = st.date_input('Data Início', datetime.now(), format='DD/MM/YYYY', key='d_ini')
            t_ini_str = st.text_input('Hora Início', placeholder='08:00', max_chars=5, key='input_ini')

        with c2:
            st.markdown('### 🟢 Fim')
            d_fim = st.date_input('Data Fim', datetime.now(), format='DD/MM/YYYY', key='d_fim')
            t_fim_str = st.text_input('Hora Fim', placeholder='17:30', max_chars=5, key='input_fim')

        st.write('')

        # Botão alinhado com a primeira coluna de inputs (Esquerda)
        sub_c1, sub_c2 = st.columns(2, gap='large')
        with sub_c1:
            calcular = st.button('⚙️ PROCESSAR DADOS', type='primary')

    # --- LÓGICA DE CÁLCULO E RESULTADO ---
    if calcular:
        obj_t_ini, str_t_ini = parse_horario(t_ini_str)
        obj_t_fim, str_t_fim = parse_horario(t_fim_str)

        if not obj_t_ini or not obj_t_fim:
            st.error('❌ Formato inválido. Use HHMM (ex: 14:30).')
        else:
            dt_ini = datetime.combine(d_ini, obj_t_ini)
            dt_fim = datetime.combine(d_fim, obj_t_fim)

            if dt_fim < dt_ini:
                 st.warning('⚠️ Data final menor que a inicial.')
            else:
                duracao = dt_fim - dt_ini
                segundos = duracao.total_seconds()
                horas_decimais = segundos / 3600
                minutos_totais = int(segundos // 60)

                # Regras de Negócio (Cores e Textos)
                if horas_decimais > 1.5:
                    cor_borda = '#ef5350' # Vermelho
                    texto_status = 'REALIZAR ANÁLISE DE FALHA'
                elif horas_decimais > 1:
                    cor_borda = '#ffa726' # Laranja
                    texto_status = 'REALIZAR ANÁLISE FCA'
                else:
                    cor_borda = '#66bb6a' # Verde
                    texto_status = 'APONTAMENTO NO RELATÓRIO DE TURNO'

                st.write('')

                # ... (código anterior permanece igual)

            # --- CARD HTML ---
            st.markdown(f'''
            <div style='
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
            '>
                <div style='
                    font-size: 0.9rem;
                    text-transform: uppercase;
                    color: {cor_borda};
                    font-weight: bold;
                    margin-bottom: 5px;
                '>
                    Ação Recomendada: {texto_status}
                </div>
                <div style='display: flex; justify-content: center; align-items: baseline; gap: 10px;'>
                    <span style='font-size: 4rem; font-weight: 800; color: #333;'>
                        {horas_decimais:.2f}
                    </span>
                    <span style='font-size: 1.2rem; color: #666;'>horas</span>
                </div>
                <div style='margin-top: 10px; font-weight: bold; color: #555;'>
                    ⏱️ Total: {minutos_totais} minutos
                </div>
                <hr style='margin: 20px 0; border: 0; border-top: 1px solid #eee;'>
                <div style='font-size: 0.85rem; color: #999;'>
                    Período: {str_t_ini} às {str_t_fim}
                </div>
            </div>
            ''', unsafe_allow_html=True)

            st.toast('Cálculo realizado com sucesso.', icon='✅')