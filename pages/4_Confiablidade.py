import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- Configuração da Página e Persona ---
st.set_page_config(
    page_title="Lancelot - Reliability Analytics",
    page_icon="⚙️",
    layout="wide"
)

# Estilo CSS personalizado para dar um ar profissional
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Cabeçalho ---
col_h1, col_h2 = st.columns([1, 5])
with col_h1:
    st.markdown("# 🛡️")
with col_h2:
    st.title("Sistema de Análise de Confiabilidade")
    st.markdown("**Powered by Lancelot** | Foco em MTBF, MTTR e Disponibilidade")
st.markdown("---")

# --- Função de Carregamento de Dados (Cache) ---
@st.cache_data
def load_data(file):
    try:
        if file.name.endswith('.xlsx'):
            return pd.read_excel(file)
        elif file.name.endswith('.csv'):
            return pd.read_csv(file, sep=None, engine='python')
    except Exception as e:
        return None

# --- Sidebar: Configuração e Filtros ---
st.sidebar.header("1. Configuração de Dados")
uploaded_file = st.sidebar.file_uploader("Carregue o ficheiro de dados (CSV/Excel)", type=["xlsx", "csv"])

if uploaded_file is not None:
    df_raw = load_data(uploaded_file)
    
    if df_raw is not None:
        st.sidebar.success("Ficheiro carregado com sucesso!")
        
        # Mapeamento de Colunas
        st.sidebar.subheader("Mapeamento de Colunas")
        all_cols = df_raw.columns.tolist()
        
        col_equip = st.sidebar.selectbox("Coluna: Equipamento/Tag", all_cols, index=0)
        col_start = st.sidebar.selectbox("Coluna: Início da Falha", all_cols, index=1 if len(all_cols) > 1 else 0)
        col_end = st.sidebar.selectbox("Coluna: Fim do Reparo", all_cols, index=2 if len(all_cols) > 2 else 0)

        # Tratamento Inicial
        try:
            df = df_raw.copy()
            df[col_start] = pd.to_datetime(df[col_start], errors='coerce')
            df[col_end] = pd.to_datetime(df[col_end], errors='coerce')
            df = df.dropna(subset=[col_start, col_end])
            
            # Ordenação essencial para cálculo de TBF
            df = df.sort_values(by=[col_equip, col_start])
            
            # Filtros
            st.sidebar.markdown("---")
            st.sidebar.header("2. Filtros de Análise")
            
            # Filtro de Data
            min_date = df[col_start].min().date()
            max_date = df[col_end].max().date()
            
            date_range = st.sidebar.date_input(
                "Período de Análise",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            # Filtro de Equipamento
            unique_equips = df[col_equip].unique()
            selected_equips = st.sidebar.multiselect(
                "Selecionar Equipamentos",
                options=unique_equips,
                default=unique_equips
            )
            
            if not selected_equips:
                st.warning("Por favor, selecione pelo menos um equipamento.")
                st.stop()

            # Aplicação dos Filtros
            if len(date_range) == 2:
                mask_date = (df[col_start].dt.date >= date_range[0]) & (df[col_end].dt.date <= date_range[1])
                df_filtered = df[mask_date & df[col_equip].isin(selected_equips)].copy()
            else:
                df_filtered = df[df[col_equip].isin(selected_equips)].copy()

            if df_filtered.empty:
                st.warning("Nenhum dado encontrado para os filtros selecionados.")
                st.stop()

        except Exception as e:
            st.error(f"Erro no processamento dos dados: {e}")
            st.stop()

        # --- Cálculos de Engenharia ---
        
        # 1. Tempo de Reparo (TTR)
        df_filtered['TTR_Horas'] = (df_filtered[col_end] - df_filtered[col_start]).dt.total_seconds() / 3600
        df_filtered = df_filtered[df_filtered['TTR_Horas'] > 0] # Remove inconsistências

        # 2. Tempo Entre Falhas (TBF)
        # O TBF é calculado por equipamento.
        df_filtered['Fim_Anterior'] = df_filtered.groupby(col_equip)[col_end].shift(1)
        df_filtered['TBF_Horas'] = (df_filtered[col_start] - df_filtered['Fim_Anterior']).dt.total_seconds() / 3600
        
        # Ajuste: Se for a primeira falha do grupo ou se houver sobreposição negativa, TBF é NaN
        df_filtered.loc[df_filtered['TBF_Horas'] < 0, 'TBF_Horas'] = np.nan

        # --- Dashboard Principal ---
        
        # Cálculos Globais (Média Ponderada pelos eventos)
        total_falhas = len(df_filtered)
        total_ttr = df_filtered['TTR_Horas'].sum()
        # Para MTBF, consideramos apenas intervalos válidos
        tbf_series = df_filtered['TBF_Horas'].dropna()
        total_tbf = tbf_series.sum()
        count_tbf = len(tbf_series)

        kpi_mttr = total_ttr / total_falhas if total_falhas > 0 else 0
        kpi_mtbf = total_tbf / count_tbf if count_tbf > 0 else 0
        
        # Disponibilidade = MTBF / (MTBF + MTTR) * 100
        if (kpi_mtbf + kpi_mttr) > 0:
            kpi_availability = (kpi_mtbf / (kpi_mtbf + kpi_mttr)) * 100
        else:
            kpi_availability = 0

        # Exibição de KPIs
        st.subheader("Indicadores Globais de Performance (KPIs)")
        c1, c2, c3, c4 = st.columns(4)
        
        c1.metric("Disponibilidade (Inerente)", f"{kpi_availability:.2f}%", help="Cálculo: MTBF / (MTBF + MTTR)")
        c2.metric("MTBF (Médio)", f"{kpi_mtbf:.2f} h", help="Tempo Médio Entre Falhas")
        c3.metric("MTTR (Médio)", f"{kpi_mttr:.2f} h", delta_color="inverse", help="Tempo Médio Para Reparo")
        c4.metric("Total de Falhas", f"{total_falhas}", help="Número total de ordens/eventos")

        st.markdown("---")

        # --- Gráficos Avançados (Plotly) ---
        
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.subheader("📊 Pareto de Falhas (Top Equipamentos)")
            pareto_data = df_filtered[col_equip].value_counts().reset_index()
            pareto_data.columns = ['Equipamento', 'Falhas']
            fig_pareto = px.bar(pareto_data, x='Equipamento', y='Falhas', 
                                color='Falhas', title="Frequência de Falhas por Ativo")
            st.plotly_chart(fig_pareto, use_container_width=True)

        with col_g2:
            st.subheader("📉 Dispersão de Tempos de Reparo")
            fig_scatter = px.scatter(df_filtered, x=col_start, y='TTR_Horas', 
                                     color=col_equip, size='TTR_Horas',
                                     title="Distribuição do MTTR ao longo do tempo",
                                     labels={'TTR_Horas': 'Horas de Reparo'})
            st.plotly_chart(fig_scatter, use_container_width=True)

        # --- Análise Detalhada Tabela ---
        st.subheader("📋 Dados Processados")
        with st.expander("Visualizar Tabela de Dados Completa"):
            st.dataframe(df_filtered[[col_equip, col_start, col_end, 'TTR_Horas', 'TBF_Horas']].style.format({
                'TTR_Horas': '{:.2f}',
                'TBF_Horas': '{:.2f}'
            }))

    else:
        st.error("O formato do ficheiro não é suportado. Utilize CSV ou Excel.")

else:
    # Tela de Boas-vindas
    st.info("👋 Bem-vindo, Lorde Soberano. Aguardando o carregamento do ficheiro de dados na barra lateral.")
    st.markdown("""
    ### Formato Esperado do Ficheiro:
    O seu ficheiro Excel ou CSV deve conter colunas para:
    * **Identificação:** Nome ou Tag do equipamento.
    * **Início:** Data e Hora do início da falha.
    * **Fim:** Data e Hora da conclusão do reparo.
    """)