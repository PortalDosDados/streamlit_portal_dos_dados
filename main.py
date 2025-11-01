"""
Portal dos Dados - Versão completa
Requisitos: streamlit, pandas, plotly, openpyxl, xlsxwriter, kaleido, pillow
Execute: python -m streamlit run main.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64
from datetime import datetime, timedelta

# ----------------------------
# Configuração da página
# ----------------------------
st.set_page_config(
    page_title="Portal dos Dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Tema / CSS
# ----------------------------
PRIMARY = "#1f77b4"     # azul LinkedIn-like
SECONDARY = "#f5f7fb"   # cinza suave
CARD_BG = "#ffffff"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {SECONDARY}; }}
    .css-1d391kg {{ color: {PRIMARY}; font-weight:600; }}
    .stButton>button {{ background-color: {PRIMARY}; color: white; border-radius:6px; }}
    .card {{
        background: {CARD_BG};
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Funções utilitárias
# ----------------------------
def sample_maintenance_data(n_machines=6, months=12):
    """Gera dataset de exemplo plausível para manutenção."""
    end = pd.Timestamp.today().normalize()
    start = end - pd.DateOffset(months=months-1)
    periods = pd.date_range(start=start, end=end, freq='MS')
    rows = []
    machines = [f"MAQ-{i:02d}" for i in range(1, n_machines+1)]
    for m in machines:
        mtbf_base = int(100 + (hash(m) % 50))  # variação por máquina
        for d in periods:
            failures = max(0, int(abs((hash((m,d.month)) % 6) - 1)))
            mtbf = max(20, mtbf_base + (d.month % 7) * 3 - failures * 5)
            mttr = round(2 + (failures * 0.8) + ((hash(d.month) % 3) * 0.5), 1)
            availability = round(90 + (mtbf/200)*10 - failures*0.8, 1)
            cost = round(2000 + failures * 350 + (1000/(mtbf/100+1)), 2)
            rows.append({
                "data_mes": d,
                "maquina": m,
                "falhas": failures,
                "mtbf": mtbf,
                "mttr": mttr,
                "disponibilidade_pct": availability,
                "custo_manutencao": cost
            })
    df = pd.DataFrame(rows)
    return df

def df_to_excel_bytes(df: pd.DataFrame) -> bytes:
    out = BytesIO()
    with pd.ExcelWriter(out, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Dados")
    out.seek(0)
    return out.getvalue()

def fig_to_png_bytes(fig) -> bytes:
    """Converte gráfico Plotly para PNG (necessita kaleido)."""
    return fig.to_image(format="png", width=1200, height=600, scale=1)

# ----------------------------
# Sidebar estilizada
# ----------------------------
st.sidebar.markdown("## 📌 Portal dos Dados")
section = st.sidebar.radio("Navegar", (
    "Dashboard", "Uploads & Data", "Power BI (placeholders)",
    "SAP PM Insights", "Gestão de Ativos", "Sobre"
))

st.sidebar.markdown("---")
st.sidebar.markdown("**Tema:** Azul / Cinza — padrão LinkedIn")
st.sidebar.markdown("**Contato:** [LinkedIn](https://www.linkedin.com/in/dione-nascimento-37287a233)")

# ----------------------------
# Cabeçalho
# ----------------------------
st.markdown("<div style='display:flex;align-items:center; gap:16px;'>"
            f"<h1 style='margin:0;padding:0'>📊 Portal dos Dados</h1>"
            f"<div style='color:gray'>- Insights aplicados à manutenção e gestão de ativos</div>"
            "</div>", unsafe_allow_html=True)

st.markdown("---")

# ----------------------------
# Conteúdo por seção
# ----------------------------
if section == "Dashboard":
    # Carregar dados: se houver upload, usar; senão, usar amostra
    st.subheader("Dashboard Interativo - Exemplo de Indicadores de Manutenção")
    col1, col2 = st.columns([3,1])
    with col2:
        st.info("Selecione filtros")
        date_range_months = st.slider("Meses (histórico)", min_value=3, max_value=24, value=12)
        machine_filter = st.multiselect("Máquinas (filtro)", options=None, default=None)
    # Se houver arquivo carregado no Uploads & Data, tentaremos usar (cache)
    if "uploaded_df" in st.session_state and st.session_state["uploaded_df"] is not None:
        df = st.session_state["uploaded_df"].copy()
    else:
        df = sample_maintenance_data(months=date_range_months)

    # preparar dados
    df["ano_mes"] = df["data_mes"].dt.strftime("%Y-%m")
    machines = sorted(df["maquina"].unique().tolist())
    if machine_filter:
        df = df[df["maquina"].isin(machine_filter)]
    else:
        # preencher seleção com todas se nenhum filtro
        machine_filter = machines

    # KPIs agregados
    agg = df.groupby("maquina").agg({
        "falhas": "sum",
        "mtbf": "mean",
        "mttr": "mean",
        "disponibilidade_pct": "mean",
        "custo_manutencao": "sum"
    }).reset_index()
    total_falhas = int(df["falhas"].sum())
    avg_mtbf = round(df["mtbf"].mean(),1)
    avg_mttr = round(df["mttr"].mean(),1)
    avg_avail = round(df["disponibilidade_pct"].mean(),1)
    total_cost = round(df["custo_manutencao"].sum(),2)

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Falhas (total)", f"{total_falhas}")
    k2.metric("MTBF (média)", f"{avg_mtbf} h")
    k3.metric("MTTR (média)", f"{avg_mttr} h")
    k4.metric("Disponibilidade (%)", f"{avg_avail}%")
    k5.metric("Custo (R$)", f"{total_cost:,.2f}")

    st.markdown("### Gráficos")
    # gráfico 1: séries temporais (disponibilidade média por mês)
    timeseries = df.groupby("ano_mes").agg({
        "disponibilidade_pct": "mean",
        "falhas": "sum",
        "custo_manutencao": "sum"
    }).reset_index()

    fig1 = px.line(timeseries, x="ano_mes", y="disponibilidade_pct",
                   title="Disponibilidade média por mês", markers=True)
    fig1.update_layout(xaxis_title="Mês", yaxis_title="Disponibilidade (%)", template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

    # gráfico 2: comparação por máquina (mtbf média)
    fig2 = px.bar(agg.sort_values("mtbf", ascending=False), x="maquina", y="mtbf",
                  title="MTBF médio por máquina", text="mtbf")
    fig2.update_layout(template="plotly_white", xaxis_title="Máquina", yaxis_title="MTBF (h)")
    st.plotly_chart(fig2, use_container_width=True)

    # Tabela com opção de download
    st.markdown("### Tabela de dados (amostra)")
    st.dataframe(df.head(200))

    excel_bytes = df_to_excel_bytes(df)
    st.download_button("⬇️ Baixar dados (Excel)", data=excel_bytes,
                       file_name=f"portal_dados_{datetime.now().strftime('%Y%m%d')}.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Exportar último gráfico como PNG
    st.markdown("Exportar gráfico como imagem (PNG)")
    img_bytes = fig1.to_image(format="png", width=1200, height=600, scale=1)
    st.download_button("⬇️ Baixar gráfico (PNG)", data=img_bytes,
                       file_name=f"disponibilidade_{datetime.now().strftime('%Y%m%d')}.png",
                       mime="image/png")

elif section == "Uploads & Data":
    st.subheader("Uploads & Data")
    st.write("Faça upload de arquivos CSV ou Excel. Os dados serão usados pelo Dashboard.")
    uploaded = st.file_uploader("Upload CSV / XLSX", type=["csv", "xlsx"], accept_multiple_files=False)
    if uploaded:
        try:
            if uploaded.name.lower().endswith(".csv"):
                df_uploaded = pd.read_csv(uploaded, parse_dates=True, dayfirst=False)
            else:
                df_uploaded = pd.read_excel(uploaded, sheet_name=0)
            st.success("Arquivo carregado com sucesso.")
            st.session_state["uploaded_df"] = df_uploaded
            st.dataframe(df_uploaded.head(200))
            st.markdown("🔽 Baixar (reenvio processado)")
            st.download_button("⬇️ Baixar (Excel)", data=df_to_excel_bytes(df_uploaded),
                               file_name=f"uploaded_{uploaded.name}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {e}")
    else:
        st.info("Nenhum arquivo enviado. Você pode usar o dataset de exemplo no Dashboard.")

elif section == "Power BI (placeholders)":
    st.subheader("Dashboards Power BI")
    st.write("Espaço para incorporar links/imagens de relatórios Power BI Service.")
    st.info("Sugestão: inserir iFrame ou links para relatórios publicados (Power BI Premium/Service).")
    st.image("https://docs.streamlit.io/en/stable/_static/branding/streamlit-mark-color.png", width=240)

elif section == "SAP PM Insights":
    st.subheader("SAP PM Insights")
    st.write("Dicas práticas, parametrizações e pequenos how-tos.")
    st.markdown("- Checklist para otimização de ordens de manutenção\n- Boas práticas de planejamento\n- KPIs relevantes: MTBF, MTTR, Disponibilidade, Backlog")
    st.success("Exemplo: ajuste de prioridades e roteiros reduz MTTR em demonstração controlada.")

elif section == "Gestão de Ativos":
    st.subheader("Gestão de Ativos / Confiabilidade")
    st.write("Metodologias, indicadores e análises estratégicas.")
    st.markdown("- Implementação de gestão do ciclo de vida\n- Monitoramento preditivo com sensores e análise de dados\n- Priorizar ativos por criticidade e custo")
    st.info("Objetivo: transformar dados em ações que reduzam custos operacionais.")

elif section == "Sobre":
    st.subheader("Sobre o Portal dos Dados")
    st.markdown("""
    **Portal dos Dados** — Plataforma de demonstração criada por Dione Nascimento.
    
    Foco: integração entre SAP PM, análises em Python e visualizações em Power BI visando resultados concretos em manutenção.
    """)
    st.write("**Quando não se agrega valor, se agrega custo.**")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/dione-nascimento-37287a233) | [GitHub](https://github.com/)")

# ----------------------------
# Rodapé
# ----------------------------
st.markdown("---")
st.markdown("<div style='text-align:right;color:gray;font-size:12px'>Portal dos Dados • Versão demo • Desenvolvido em Streamlit</div>", unsafe_allow_html=True)
