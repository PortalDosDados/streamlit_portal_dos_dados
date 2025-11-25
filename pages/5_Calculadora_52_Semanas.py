import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import io

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="WeekFlow | Gestão de Paradas", page_icon="🔧", layout="wide")

# --- 2. CSS CENTRALIZADO E LIMPO ---
st.markdown("""
    <style>
    /* Estilo do Card (Metric) */
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    div[data-testid="stMetricValue"] { 
        color: var(--primary-color); 
        font-weight: 700; 
        text-align: center;
        width: 100%;
    }
    div[data-testid="stMetricLabel"] {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    /* Botão de Download ocupando largura total da coluna */
    div.stButton > button:first-child {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. FUNÇÕES CORE ---

def gerar_template_excel():
    df_exemplo = pd.DataFrame({
        'Parada': ['Caldeira', 'Mecânica Geral', 'Elétrica', 'Lubrificação'],
        'Data Planejada': [
            datetime.now(), 
            datetime.now() + timedelta(days=5), 
            datetime.now() + timedelta(days=20),
            datetime.now() + timedelta(days=25)
        ],
        'Data Realizada': [None, None, None, None],
        'Comentário': ['Crítico', 'Equipe A', 'Equipe B', 'Rotina']
    })
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_exemplo.to_excel(writer, index=False, sheet_name='Cronograma_Paradas')
    buffer.seek(0)
    return buffer

def converter_df_para_excel(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Paradas_Processadas')
    buffer.seek(0)
    return buffer

def estilizar_tabela(df):
    """Centraliza texto e cabeçalhos."""
    return df.style.set_properties(**{'text-align': 'center'}) \
                   .set_table_styles([dict(selector='th', props=[('text-align', 'center')])])

def traduzir_datas(df, col_data):
    """Tradução forçada PT-BR."""
    mapa_meses = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
        7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    mapa_dias = {
        0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira', 3: 'Quinta-feira', 
        4: 'Sexta-feira', 5: 'Sábado', 6: 'Domingo'
    }
    df['Mes_Num'] = df[col_data].dt.month
    df['Dia_Num'] = df[col_data].dt.weekday
    df['Mes_Nome'] = df['Mes_Num'].map(mapa_meses)
    df['Dia_Semana'] = df['Dia_Num'].map(mapa_dias)
    return df

def processar_grid_completo(df, col_data, col_nome, col_comentario):
    """Gera o grid anual e agrupa as paradas."""
    df_input = df.copy()
    df_input[col_data] = pd.to_datetime(df_input[col_data], errors='coerce')
    df_input = df_input.dropna(subset=[col_data])
    df_input[col_data] = df_input[col_data].dt.normalize()
    
    df_input[col_nome] = df_input[col_nome].astype(str)
    df_input[col_comentario] = df_input[col_comentario].fillna('').astype(str)
    
    if len(df_input) == 0:
        return df_input, datetime.now().year, col_nome
    
    ano_foco = df_input[col_data].dt.year.mode()[0]
    datas_ano = pd.date_range(start=f'{ano_foco}-01-01', end=f'{ano_foco}-12-31', freq='D')
    df_grid = pd.DataFrame({col_data: datas_ano})
    
    df_agrupado = df_input.groupby(col_data).agg({
        col_nome: lambda x: ' | '.join(x),
        col_comentario: lambda x: ' | '.join(x),
        col_data: 'count'
    }).rename(columns={col_data: 'Qtd_Paradas'}).reset_index()
    
    df_final = pd.merge(df_grid, df_agrupado, on=col_data, how='left')
    df_final['Qtd_Paradas'] = df_final['Qtd_Paradas'].fillna(0)
    df_final[col_nome] = df_final[col_nome].fillna('-')
    
    df_final = traduzir_datas(df_final, col_data)
    iso = df_final[col_data].dt.isocalendar()
    df_final['Semana_Ano'] = iso.week
    
    return df_final, ano_foco, col_nome

def criar_calendario_full(df_completo, col_data, nome_col_parada):
    dias_ordenados_pt = [
        'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 
        'Sexta-feira', 'Sábado', 'Domingo'
    ]
    
    chart = alt.Chart(df_completo).mark_rect(
        cornerRadius=2,
        strokeOpacity=0
    ).encode(
        x=alt.X('Semana_Ano:O', title='Semana do Ano (1-52)', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Dia_Semana:O', sort=dias_ordenados_pt, title=None),
        
        color=alt.condition(
            alt.datum.Qtd_Paradas > 0,
            alt.Color(f'{nome_col_parada}:N', 
                      title='Tipo de Parada', 
                      scale=alt.Scale(scheme='category20'),
                      legend=alt.Legend(
                          orient='bottom', 
                          columns=4,       
                          symbolLimit=0,
                          labelFontSize=12,
                          titleFontSize=13
                      )),
            alt.value('rgba(128, 128, 128, 0.1)')
        ),
        
        tooltip=[
            alt.Tooltip(col_data, title='Data', format='%d/%m/%Y'),
            alt.Tooltip('Mes_Nome', title='Mês'),
            alt.Tooltip('Dia_Semana', title='Dia'),
            alt.Tooltip(nome_col_parada, title='Parada/Equipamento')
        ]
    ).properties(
        width='container',
        height=380
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        grid=False,
        domain=False,
        ticks=False,
        labelFontSize=11
    ).configure(
        background='transparent'
    )
    return chart

# --- 4. INTERFACE ---
st.title("🔧 WeekFlow | Gestão de Paradas")
st.markdown("Mapa Visual de **Cronograma de Manutenção** (Por Tipo de Parada).")
st.divider()

aba1, aba2 = st.tabs(["🔎 Calculadora Rápida", "📂 Mapa de Paradas (Anual)"])

with aba1:
    st.caption("Auxiliar de Planejamento")
    c1, c2, c3 = st.columns(3)
    d = c1.date_input("Data da Parada:", datetime.now())
    a, s, _ = d.isocalendar()
    c2.metric("Semana de Execução", f"S{s}")
    c3.metric("Dia do Ano", d.timetuple().tm_yday)

with aba2:
    col_dl, col_up = st.columns([1, 2])
    with col_dl:
        st.info("Passo 1")
        st.download_button("📥 Baixar Template", gerar_template_excel(), "template_paradas.xlsx", use_container_width=True)
    with col_up:
        st.info("Passo 2")
        arquivo = st.file_uploader("Upload Cronograma (.xlsx)", type=['xlsx'], label_visibility="collapsed")
        
    if arquivo:
        st.divider()
        try:
            df_raw = pd.read_excel(arquivo)
            cols = df_raw.columns.tolist()
            idx_data = cols.index('Data Planejada') if 'Data Planejada' in cols else 0
            idx_nome = cols.index('Parada') if 'Parada' in cols else 0
            idx_com = cols.index('Comentário') if 'Comentário' in cols else 0
            
            c_sel1, c_sel2, c_sel3 = st.columns(3)
            col_data = c_sel1.selectbox("Coluna DATA:", cols, index=idx_data)
            col_nome = c_sel2.selectbox("Coluna NOME DA PARADA:", cols, index=idx_nome)
            col_com = c_sel3.selectbox("Coluna COMENTÁRIO:", cols, index=idx_com)
            
            if st.button("🚀 Gerar Mapa Colorido", type="primary"):
                df_grid, ano, col_nome_final = processar_grid_completo(df_raw, col_data, col_nome, col_com)
                
                st.markdown(f"### 📅 Cronograma de Paradas - {ano}")
                
                # Gráfico
                grafico = criar_calendario_full(df_grid, col_data, col_nome_final)
                st.altair_chart(grafico, use_container_width=True)
                
                # Métricas
                total = df_grid['Qtd_Paradas'].sum()
                ocupacao = len(df_grid[df_grid['Qtd_Paradas'] > 0])
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Intervenções", int(total))
                m2.metric("Dias Bloqueados", ocupacao)
                m3.metric("Máximo Diário", int(df_grid['Qtd_Paradas'].max()))

                with st.expander("📋 Ver Detalhes"):
                    cols_show = [col_data, 'Dia_Semana', col_nome_final]
                    df_exibir = df_grid[df_grid['Qtd_Paradas'] > 0][cols_show].sort_values(col_data)
                    df_exibir[col_data] = df_exibir[col_data].dt.strftime('%d/%m/%Y')
                    st.dataframe(estilizar_tabela(df_exibir), use_container_width=True, hide_index=True)
                
                st.divider()
                
                # Botão único e limpo
                st.download_button(
                    label="✅ Baixar Relatório (Excel)",
                    data=converter_df_para_excel(df_grid),
                    file_name=f"relatorio_paradas_{ano}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
        except Exception as e:
            st.error(f"Erro: {e}")