import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

# ============================================================================
# 1. CONFIGURAÇÃO GERAL DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Portal dos Dados - Curva S & Tendência",
    page_icon="📈",
    layout="wide",
)


# ============================================================================
# 2. ESTILIZAÇÃO E ASSETS
# ============================================================================
def carregar_css(nome_arquivo):
    """Carrega o CSS global para manter a identidade visual do portal."""
    try:
        with open(nome_arquivo, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


carregar_css("style.css")

# CSS específico para os cards de indicadores de performance
st.markdown(
    """
<style>
    .stButton button { width: 100%; height: 3.5rem; font-weight: bold; font-size: 1.1rem; }
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #00CC96;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        color: #333;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================================
# 3. LÓGICA DE NEGÓCIO (AUXILIARES)
# ============================================================================
def generate_excel_template():
    """Gera o modelo de Excel para preenchimento de cronograma industrial."""
    df_template = pd.DataFrame(
        {
            "Atividade": [
                "Bloqueio",
                "C.Peso",
                "Passagem 1ª bobina",
                "Vulcanizar 1ª emenda",
                "Desbloqueio",
            ],
            "Duração Planejada": [1.0, 2.0, 4.0, 10.0, 1.0],
            "Duração Realizada": [0.5, 1.0, 4.2, 12.0, None],
        }
    )
    output = BytesIO()
    # Utiliza o engine xlsxwriter conforme discutido para garantir compatibilidade
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_template.to_excel(writer, index=False, sheet_name="Cronograma")
    return output.getvalue()


# ============================================================================
# 4. INTERFACE DO USUÁRIO
# ============================================================================
st.title("📈 Acompanhamento de Projetos (Curva S)")
st.markdown(
    "Analise o **SPI (Eficiência)** e a **Projeção de Tendência** para garantir a disponibilidade do ativo."
)

# Layout Superior: Download do Modelo e Upload de Dados
col_desc, col_down = st.columns([3, 1])
with col_down:
    st.download_button(
        "📥 Baixar Modelo Excel",
        data=generate_excel_template(),
        file_name="modelo_curva_s_portal_dados.xlsx",
    )

uploaded_file = st.file_uploader(
    "Upload do Cronograma", type=["xlsx"], label_visibility="collapsed"
)

st.divider()

if uploaded_file:
    # 1. Carregamento e Tratamento de Dados
    df = pd.read_excel(uploaded_file)

    # Sanitização: Força conversão para numérico para evitar erros de cálculo
    df["Duração Planejada"] = pd.to_numeric(
        df["Duração Planejada"], errors="coerce"
    ).fillna(0)
    df["Duração Realizada"] = pd.to_numeric(df["Duração Realizada"], errors="coerce")

    # 2. Cálculos Acumulados de Curva S
    total_pl = df["Duração Planejada"].sum()
    df["% Pl Acum"] = (df["Duração Planejada"] / total_pl).cumsum() * 100
    df["% Re Acum"] = (df["Duração Realizada"] / total_pl).cumsum() * 100

    # 3. Identificação do Ponto Atual e Cálculo de Tendência
    ultimo_idx = df[df["Duração Realizada"].notnull()].index.max()

    if pd.notnull(ultimo_idx):
        # SPI (Schedule Performance Index)
        spi = (
            df.loc[ultimo_idx, "% Re Acum"] / df.loc[ultimo_idx, "% Pl Acum"]
            if df.loc[ultimo_idx, "% Pl Acum"] > 0
            else 1
        )

        # Inicializa coluna de Tendência
        df["Tendencia"] = df["% Re Acum"]
        val_ref = df.loc[ultimo_idx, "% Re Acum"]

        # Projeção Matemática baseada na velocidade atual
        for i in range(ultimo_idx + 1, len(df)):
            incremento_teorico = df.loc[i, "Duração Planejada"] / total_pl * 100
            val_ref += incremento_teorico / spi if spi > 0 else incremento_teorico
            df.loc[i, "Tendencia"] = val_ref

        # --- EXIBIÇÃO DE INDICADORES (KPIs) ---
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(
                f"<div class='metric-card'><b>Eficiência (SPI)</b><br><h2>{spi:.2f}</h2></div>",
                unsafe_allow_html=True,
            )
        with m2:
            desvio_final = df["Tendencia"].iloc[-1] - 100
            cor_d = "#ef5350" if desvio_final > 0 else "#66bb6a"
            st.markdown(
                f"<div class='metric-card' style='border-left-color:{cor_d}'><b>Desvio Final Estimado</b><br><h2>{desvio_final:+.1f}%</h2></div>",
                unsafe_allow_html=True,
            )
        with m3:
            status_text = "⚠️ ATRASO" if spi < 0.95 else "✅ NO PRAZO"
            st.markdown(
                f"<div class='metric-card'><b>Status Geral</b><br><h2>{status_text}</h2></div>",
                unsafe_allow_html=True,
            )

        st.write("")

        # --- GRÁFICO PLOTLY INTERATIVO ---
        fig = go.Figure()

        # Curva Planejada (Benchmark)
        fig.add_trace(
            go.Scatter(
                x=df["Atividade"],
                y=df["% Pl Acum"],
                name="Planejado",
                line=dict(color="#BDC3C7", dash="dash"),
            )
        )

        # Curva Realizada (Execução Atual)
        fig.add_trace(
            go.Scatter(
                x=df.loc[:ultimo_idx, "Atividade"],
                y=df.loc[:ultimo_idx, "% Re Acum"],
                name="Realizado",
                line=dict(color="#00CC96", width=4),
            )
        )

        # Projeção de Tendência (Futuro)
        fig.add_trace(
            go.Scatter(
                x=df.loc[ultimo_idx:, "Atividade"],
                y=df.loc[ultimo_idx:, "Tendencia"],
                name="Tendência",
                line=dict(color="#EF5350", dash="dot"),
            )
        )

        fig.update_layout(
            template="plotly_white",
            margin=dict(l=20, r=20, t=40, b=20),
            height=500,
            hovermode="x unified",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- TABELA DE DADOS COM CORREÇÃO DE FORMATAÇÃO ---
        with st.expander("🔍 Auditoria de Dados"):
            # Identifica colunas numéricas para evitar o ValueError 'f' com strings
            cols_numericas = [
                "Duração Planejada",
                "Duração Realizada",
                "% Pl Acum",
                "% Re Acum",
                "Tendencia",
            ]
            cols_presentes = [c for c in cols_numericas if c in df.columns]

            st.dataframe(df.style.format("{:.2f}", subset=cols_presentes, na_rep="-"))

    else:
        st.warning(
            "⚠️ O arquivo carregado não possui dados executados na coluna 'Duração Realizada'."
        )

else:
    st.info(
        "💡 Lancelot, baixe o modelo acima, preencha as durações e faça o upload para gerar a análise estratégica."
    )

# ============================================================================
# 5. RODAPÉ
# ============================================================================
st.divider()
try:
    st.image("./assets/fundo.jpg", use_container_width=True)
except:
    st.caption(
        "Portal dos Dados | Precisão da Engenharia, Agilidade da Análise de Dados."
    )
