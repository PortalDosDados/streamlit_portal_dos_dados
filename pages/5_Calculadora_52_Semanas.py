from datetime import datetime
import streamlit as st
from utils.ui import load_css, render_footer

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title='Portal dos Dados - Calculadora 52 Semanas',
    page_icon='📅',
    layout='wide',
)

# --- 2. ESTILOS GLOBAIS ---
load_css('style.css')

# --- 3. INTERFACE E LÓGICA ---
st.title('📅 Calculadora de Semanas (PCM)')
st.markdown('Converta datas para **Padrões Industriais e Semanas ISO** de manutenção e planejamento.')
st.divider()

with st.container():
    col_input, col_info = st.columns([1, 1], gap='medium')

    with col_input:
        data_input = st.date_input(
            'Selecione a Data:', datetime.today(), format='DD/MM/YYYY'
        )

        ano_iso, semana_iso, dia_num_iso = data_input.isocalendar()
        dia_do_ano = data_input.timetuple().tm_yday

        dias_pt = {
            0: 'Segunda-feira',
            1: 'Terça-feira',
            2: 'Quarta-feira',
            3: 'Quinta-feira',
            4: 'Sexta-feira',
            5: 'Sábado',
            6: 'Domingo',
        }
        nome_dia_semana = dias_pt[data_input.weekday()]

    with col_info:
        st.info(
            f"**Data Selecionada:** {data_input.strftime('%d/%m/%Y')}  \n"
            f"**Padrão:** Calendário Industrial ISO 8601 (52 Semanas)  \n"
            f"**Aplicação:** Cronogramas de Manutenção Preventiva, Sprints e Planejamento Operacional."
        )

    st.write('')

    # Exibição dos Resultados em Métricas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label='Semana do Ano', value=f'S{semana_iso:02d}')

    with col2:
        st.metric(label='Dia do Ano', value=f'{dia_do_ano}º dia')

    with col3:
        st.metric(label='Dia da Semana', value=nome_dia_semana)

    with col4:
        st.metric(label='Ano ISO', value=f'{ano_iso}')

# --- 4. NOTAS E RODAPÉ ---
st.caption(
    'Nota: O calendário ISO 8601 inicia a semana sempre na segunda-feira. Essencial para controle de Ordens de Serviço (OS) no plano de 52 semanas.'
)

render_footer()
