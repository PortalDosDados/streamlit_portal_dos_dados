from datetime import datetime, timedelta, time
import streamlit as st
from utils.ui import load_css, get_asset_path, render_footer
from utils.business_rules import parse_horario, classificar_severidade_parada

# ============================================================================
# 1. CONFIGURAÇÃO GERAL DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title='Portal dos Dados - Calculadora de Paradas',
    page_icon='🏭',
    layout='wide',
)

# ============================================================================
# 2. ESTILIZAÇÃO E ASSETS
# ============================================================================
load_css('style.css')

# Injeção de CSS Específico (Tweaks de Interface)
st.markdown(
    '''
<style>
    /* Input: Fonte monoespaçada para alinhamento numérico e centralização */
    .stTextInput input {
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 1.4rem;
        text-align: center;
        padding: 10px;
    }

    /* Botão: Aumento da área de clique para facilitar uso em tablets/touch */
    .stButton button {
        width: 100%;
        height: 3.5rem;
        font-weight: bold;
        font-size: 1.1rem;
    }
</style>
''',
    unsafe_allow_html=True,
)

# ============================================================================
# 3. INTERFACE DO USUÁRIO (FRONTEND)
# ============================================================================
# ============================================================================

st.title('🏭 Controle de Parada de Manutenção')
st.markdown('Calcule e classifique o **Downtime** e a criticidade de intervenções industriais.')
st.divider()

with st.container():
    col_input_esq, col_input_dir = st.columns(2, gap='large')

    with col_input_esq:
        st.markdown('### 🔴 Início da Parada')
        d_ini = st.date_input(
            'Data Início', datetime.today(), format='DD/MM/YYYY', key='d_ini'
        )
        t_ini_str = st.text_input(
            'Hora Início (ex: 0800 ou 08:00)', placeholder='08:00', max_chars=5, key='input_ini'
        )

    with col_input_dir:
        st.markdown('### 🟢 Fim da Parada')
        d_fim = st.date_input(
            'Data Fim', datetime.today(), format='DD/MM/YYYY', key='d_fim'
        )
        t_fim_str = st.text_input(
            'Hora Fim (ex: 1730 ou 17:30)', placeholder='17:30', max_chars=5, key='input_fim'
        )

    st.write('')

    c_btn_esq, _ = st.columns([1, 1], gap='large')
    with c_btn_esq:
        calcular = st.button('⚙️ PROCESSAR TEMPO DE PARADA', type='primary')

# ============================================================================
# 5. PROCESSAMENTO E EXIBIÇÃO DE RESULTADOS
# ============================================================================

if calcular:
    obj_t_ini, str_t_ini = parse_horario(t_ini_str)
    obj_t_fim, str_t_fim = parse_horario(t_fim_str)

    if not obj_t_ini or not obj_t_fim:
        st.error('❌ Formato de horário inválido. Utilize o formato HH:MM ou HHMM (ex: 14:30 ou 0800).')
    else:
        dt_ini = datetime.combine(d_ini, obj_t_ini)
        dt_fim = datetime.combine(d_fim, obj_t_fim)

        if dt_fim < dt_ini:
            st.warning('⚠️ Erro cronológico: A data/hora final é anterior ao início da parada.')
        else:
            duracao = dt_fim - dt_ini
            segundos = duracao.total_seconds()
            horas_decimais = segundos / 3600
            minutos_totais = int(segundos // 60)

            # Matriz de Severidade da Manutenção
            texto_status, cor_borda = classificar_severidade_parada(horas_decimais)

            st.write('')

            st.markdown(
                f'''
            <div style='
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 24px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                background-color: #1e222a;
                border-top: 8px solid {cor_borda};
                text-align: center;
                max-width: 700px;
                margin: 0 auto;
                color: #FAFAFA;
            '>
                <div style='
                    font-size: 0.95rem;
                    text-transform: uppercase;
                    color: {cor_borda};
                    font-weight: bold;
                    margin-bottom: 8px;
                '>
                    Ação Recomendada: {texto_status}
                </div>
                <div style='display: flex; justify-content: center; align-items: baseline; gap: 10px;'>
                    <span style='font-size: 4rem; font-weight: 800; color: #FFFFFF;'>
                        {horas_decimais:.2f}
                    </span>
                    <span style='font-size: 1.3rem; color: #A0AEC0;'>horas</span>
                </div>
                <div style='margin-top: 10px; font-weight: bold; color: #CBD5E0;'>
                    ⏱️ Duração Total: {minutos_totais} minutos
                </div>
                <hr style='margin: 20px 0; border: 0; border-top: 1px solid rgba(255,255,255,0.1);'>
                <div style='font-size: 0.9rem; color: #A0AEC0;'>
                    Período Registrado: <b style="color: #FFF;">{str_t_ini}</b> ({d_ini.strftime('%d/%m/%Y')}) até <b style="color: #FFF;">{str_t_fim}</b> ({d_fim.strftime('%d/%m/%Y')})
                </div>
            </div>
            ''',
                unsafe_allow_html=True,
            )

            st.write('')
            with st.expander('📋 Copiar Apontamento para Relatório de Turno / ERP'):
                resumo_fca = (
                    f"REGISTRO DE PARADA OPERACIONAL\n"
                    f"Início: {d_ini.strftime('%d/%m/%Y')} às {str_t_ini}\n"
                    f"Fim:    {d_fim.strftime('%d/%m/%Y')} às {str_t_fim}\n"
                    f"Duração: {horas_decimais:.2f}h ({minutos_totais} minutos)\n"
                    f"Severidade: {texto_status}\n"
                )
                st.code(resumo_fca, language="text")

            st.toast('Cálculo realizado e validado com sucesso.', icon='✅')

# ============================================================================
# 6. RODAPÉ
# ============================================================================
render_footer()
