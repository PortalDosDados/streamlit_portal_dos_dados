import streamlit as st
from datetime import datetime, timedelta, time

# ============================================================================
# 1. CONFIGURAÇÃO GERAL DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title='Portal dos Dados - Calculadora de Paradas',
    page_icon='🏭',
    layout='wide'
)

# ============================================================================
# 2. ESTILIZAÇÃO E ASSETS
# ============================================================================

def carregar_css(nome_arquivo):
    """
    Carrega um arquivo CSS externo para personalização do tema.

    Args:
        nome_arquivo (str): Caminho relativo do arquivo .css
    """
    try:
        with open(nome_arquivo, encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning('⚠️ Aviso: Arquivo style.css não encontrado. O tema padrão será aplicado.')

# Carrega o CSS global (cores da marca, fundos, etc.)
carregar_css('style.css')

# Injeção de CSS Específico (Tweaks de Interface)
# Foco: Melhorar a UX de inputs numéricos e botões de ação (CTA)
st.markdown('''
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

    /* UX: Remove labels pequenos padrão para utilizar títulos H3 personalizados */
    .stTextInput label { display: none; }
</style>
''', unsafe_allow_html=True)

# ============================================================================
# 3. LÓGICA DE NEGÓCIO (BACKEND HELPER)
# ============================================================================

def parse_horario(valor):
    """
    Interpreta entradas de horário em diversos formatos (HHMM, HMM, HH)
    e converte para objeto datetime.time e string formatada.

    Args:
        valor (str): Entrada bruta do usuário (ex: '1430', '800', '14')

    Returns:
        tuple: (objeto time, string 'HH:MM') ou (None, valor_original) em caso de erro.
    """
    if not valor: return None, ''

    # Sanitização: Remove qualquer caractere não numérico
    nums = ''.join(filter(str.isdigit, str(valor)))

    try:
        # Lógica de Parsing Inteligente
        if len(nums) == 4:     # Formato HHMM (ex: 1430)
            h, m = int(nums[:2]), int(nums[2:])
        elif len(nums) == 3:   # Formato HMM (ex: 830)
            h, m = int(nums[:1]), int(nums[1:])
        elif len(nums) <= 2 and nums != '': # Formato HH (ex: 14)
            h, m = int(nums), 0
        else:
            return None, valor

        # Validação de limites de hora/minuto
        if 0 <= h <= 23 and 0 <= m <= 59:
            return time(h, m), f'{h:02d}:{m:02d}'

        return None, valor
    except:
        return None, valor

# ============================================================================
# 4. INTERFACE DO USUÁRIO (FRONTEND)
# ============================================================================

st.title('🏭 Controle de Parada')
st.markdown('Digite os horários e processe o cálculo de **Downtime**.')
st.divider()

# Container Principal - Área de Inputs
# Utiliza st.container para agrupamento lógico dos elementos
with st.container():

    # Layout: Grid de 2 colunas para distribuição uniforme (Full Width)
    col_input_esq, col_input_dir = st.columns(2, gap='large')

    # --- Coluna Esquerda: INÍCIO ---
    with col_input_esq:
        st.markdown('### 🔴 Início')
        d_ini = st.date_input('Data Início', datetime.now(), format='DD/MM/YYYY', key='d_ini')
        t_ini_str = st.text_input('Hora Início', placeholder='08:00', max_chars=5, key='input_ini')

    # --- Coluna Direita: FIM ---
    with col_input_dir:
        st.markdown('### 🟢 Fim')
        d_fim = st.date_input('Data Fim', datetime.now(), format='DD/MM/YYYY', key='d_fim')
        t_fim_str = st.text_input('Hora Fim', placeholder='17:30', max_chars=5, key='input_fim')

    st.write('') # Espaçador visual

    # Área do Botão de Ação
    # Cria novas colunas para alinhar o botão com a coluna esquerda acima
    c_btn_esq, c_btn_dir = st.columns(2, gap='large')

    with c_btn_esq:
        # Botão Primário (Action)
        calcular = st.button('⚙️ PROCESSAR DADOS', type='primary')

# ============================================================================
# 5. PROCESSAMENTO E EXIBIÇÃO DE RESULTADOS
# ============================================================================

if calcular:
    # 1. Parsing dos horários
    obj_t_ini, str_t_ini = parse_horario(t_ini_str)
    obj_t_fim, str_t_fim = parse_horario(t_fim_str)

    # 2. Validação de Integridade
    if not obj_t_ini or not obj_t_fim:
        st.error('❌ Formato inválido. Utilize o padrão HHMM (ex: 14:30 ou 08:00).')
    else:
        # Combinação de Data + Hora para cálculo preciso (timestamps)
        dt_ini = datetime.combine(d_ini, obj_t_ini)
        dt_fim = datetime.combine(d_fim, obj_t_fim)

        # Validação Cronológica
        if dt_fim < dt_ini:
             st.warning('⚠️ Erro: A Data Final é anterior à Data Inicial.')
        else:
            # 3. Cálculo Matemático
            duracao = dt_fim - dt_ini
            segundos = duracao.total_seconds()

            # Conversão para Horas Decimais (Base para custo) e Minutos Totais
            horas_decimais = segundos / 3600
            minutos_totais = int(segundos // 60)

            # 4. Regras de Negócio (Matriz de Escalabilidade)
            # Define cores e ações baseadas na severidade da parada
            if horas_decimais > 1.5:
                cor_borda = '#ef5350' # Vermelho (Crítico)
                texto_status = 'REALIZAR ANÁLISE DE FALHA'
            elif horas_decimais > 1:
                cor_borda = '#ffa726' # Laranja (Atenção)
                texto_status = 'REALIZAR ANÁLISE FCA'
            else:
                cor_borda = '#66bb6a' # Verde (Rotina)
                texto_status = 'APONTAMENTO NO RELATÓRIO DE TURNO'

            st.write('')

            # 5. Renderização do Relatório (Card HTML Customizado)
            # Utiliza HTML/CSS injetado para criar um visual de Dashboard
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
                    Período Registrado: {str_t_ini} às {str_t_fim}
                </div>
            </div>
            ''', unsafe_allow_html=True)

            # Feedback Tátil/Visual
            st.toast('Cálculo realizado e validado com sucesso.', icon='✅')

# ============================================================================
# 6. RODAPÉ E NOTAS
# ============================================================================
st.space()
# Imagem de fundo (certifique-se que a pasta assets existe)
st.image('./assets/fundo.jpg', use_container_width=True)