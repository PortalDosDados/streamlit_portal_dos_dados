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
    try:
        with open(nome_arquivo, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


carregar_css("style.css")

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
    .logic-box {
        background-color: #e3f2fd;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #90caf9;
        color: #0d47a1;
        font-size: 0.95rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================================
# 3. LÓGICA DE NEGÓCIO (AUXILIARES)
# ============================================================================
def generate_excel_template():
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
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_template.to_excel(writer, index=False, sheet_name="Cronograma")
    return output.getvalue()


# ============================================================================
# 4. INTERFACE DO USUÁRIO
# ============================================================================
st.title("📈 Acompanhamento de Projetos (Curva S)")
st.markdown("Transformando dados de engenharia em **Inteligência Preditiva**.")

col_desc, col_down = st.columns([3, 1])
with col_down:
    st.download_button(
        "📥 Baixar Modelo Excel",
        data=generate_excel_template(),
        file_name="modelo_curva_s.xlsx",
    )

uploaded_file = st.file_uploader(
    "Upload do Cronograma", type=["xlsx"], label_visibility="collapsed"
)

# --- CAMPO DE EXPLICAÇÃO DA LÓGICA REFINADO ---
with st.expander("🎓 Fundamentos Técnicos e Lógica dos Cálculos"):
    st.markdown(
        """
    <div style='background-color: #f0f7ff; padding: 20px; border-radius: 10px; border: 1px solid #b3d7ff;'>
        <p style='color: #004085; font-size: 1.1rem; font-weight: bold;'>
            Como transformamos dados brutos em inteligência preditiva:
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_log1, col_log2 = st.columns(2)

    with col_log1:
        st.markdown("### 📊 Avanço Físico")
        st.write(
            """
        O **Percentual Acumulado** representa o peso de cada tarefa concluída em relação ao escopo total do projeto.
        Diferente de somas simples, nossa lógica recalcula o acúmulo cronológico para garantir que a curva seja sempre ascendente, corrigindo eventuais falhas de input manual.
        """
        )
        st.latex(r"\%Acumulado = \frac{\sum Duração\ Realizada}{Total\ Planejado}")

    with col_log2:
        st.markdown("### 🚀 Eficiência (SPI)")
        st.write(
            """
        O **SPI** (*Schedule Performance Index*) é o termômetro do seu prazo. Ele indica a velocidade de entrega atual:
        - **SPI > 1.0**: Execução acima do ritmo planejado (Adiantado).
        - **SPI < 1.0**: Execução abaixo do ritmo planejado (Atrasado).
        """
        )
        st.latex(r"SPI = \frac{\%Realizado\ Acumulado}{\%Planejado\ Acumulado}")

    st.divider()

    col_log3, col_log4 = st.columns(2)

    with col_log3:
        st.markdown("### 🔮 Projeção de Tendência")
        st.write(
            """
        Utilizamos estatística descritiva para prever o futuro. O sistema projeta as atividades restantes aplicando a **eficiência real (SPI)** sobre o plano original.
        Se o seu SPI é 0.8, o sistema entende que as próximas tarefas levarão 25% a mais de tempo do que o previsto.
        """
        )

    with col_log4:
        st.markdown("### ⚠️ Desvio Final Estimado")
        st.write(
            """
        Este indicador revela o "estouro" ou "ganho" previsto para o final do projeto.
        - **Positivo (+)**: O projeto tende a terminar com atraso.
        - **Negativo (-)**: O projeto tende a terminar antes do prazo.
        """
        )
        st.latex(r"Desvio = \%Tendência\ Final - 100\%")

st.divider()

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df["Duração Planejada"] = pd.to_numeric(
        df["Duração Planejada"], errors="coerce"
    ).fillna(0)
    df["Duração Realizada"] = pd.to_numeric(df["Duração Realizada"], errors="coerce")

    total_pl = df["Duração Planejada"].sum()
    df["% Pl Acum"] = (df["Duração Planejada"] / total_pl).cumsum() * 100
    df["% Re Acum"] = (df["Duração Realizada"] / total_pl).cumsum() * 100

    ultimo_idx = df[df["Duração Realizada"].notnull()].index.max()

    if pd.notnull(ultimo_idx):
        spi = (
            df.loc[ultimo_idx, "% Re Acum"] / df.loc[ultimo_idx, "% Pl Acum"]
            if df.loc[ultimo_idx, "% Pl Acum"] > 0
            else 1
        )

        df["Tendencia"] = df["% Re Acum"]
        val_ref = df.loc[ultimo_idx, "% Re Acum"]
        for i in range(ultimo_idx + 1, len(df)):
            incremento_teorico = df.loc[i, "Duração Planejada"] / total_pl * 100
            val_ref += incremento_teorico / spi if spi > 0 else incremento_teorico
            df.loc[i, "Tendencia"] = val_ref

        desvio_final = df["Tendencia"].iloc[-1] - 100

        # Regras de Status
        if desvio_final > 0.5:
            status_text, cor_status = "⚠️ POTENCIAL ATRASO", "#ffa726"
            if spi < 0.90:
                status_text, cor_status = "🔴 CRÍTICO / ATRASO", "#ef5350"
        else:
            status_text, cor_status = "✅ NO PRAZO", "#66bb6a"

        # KPIs
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(
                f"<div class='metric-card'><b>Eficiência (SPI)</b><br><h2>{spi:.2f}</h2></div>",
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f"<div class='metric-card' style='border-left-color:{'#ef5350' if desvio_final > 0 else '#66bb6a'}'><b>Desvio Final Estimado</b><br><h2>{desvio_final:+.1f}%</h2></div>",
                unsafe_allow_html=True,
            )
        with m3:
            st.markdown(
                f"<div class='metric-card' style='border-left-color:{cor_status}'><b>Status Geral</b><br><h2>{status_text}</h2></div>",
                unsafe_allow_html=True,
            )

        # --- CONFIGURAÇÃO DO GRÁFICO ATUALIZADA ---
        fig = go.Figure()

        # Planejado (AZUL)
        fig.add_trace(
            go.Scatter(
                x=df["Atividade"],
                y=df["% Pl Acum"],
                name="Planejado",
                line=dict(color="#1f77b4", dash="dash"),
                hovertemplate="Planejado: %{y:.2f}%<extra></extra>",
            )
        )

        # Realizado (VERDE)
        fig.add_trace(
            go.Scatter(
                x=df.loc[:ultimo_idx, "Atividade"],
                y=df.loc[:ultimo_idx, "% Re Acum"],
                name="Realizado",
                line=dict(color="#00CC96", width=4),
                hovertemplate="Realizado: %{y:.2f}%<extra></extra>",
            )
        )

        # Projeção (VERMELHO)
        fig.add_trace(
            go.Scatter(
                x=df.loc[ultimo_idx:, "Atividade"],
                y=df.loc[ultimo_idx:, "Tendencia"],
                name="Projeção",
                line=dict(color="#EF5350", dash="dot"),
                hovertemplate="Projeção: %{y:.2f}%<extra></extra>",
            )
        )

        fig.update_layout(
            template="plotly_white",
            height=500,
            hovermode="x unified",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            yaxis=dict(ticksuffix="%"),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Auditoria
        with st.expander("🔍 Auditoria de Dados"):
            cols_num = [
                "Duração Planejada",
                "Duração Realizada",
                "% Pl Acum",
                "% Re Acum",
                "Tendencia",
            ]
            st.dataframe(
                df.style.format(
                    "{:.2f}",
                    subset=[c for c in cols_num if c in df.columns],
                    na_rep="-",
                )
            )
    else:
        st.warning("⚠️ Planilha sem dados de execução.")
else:
    st.info("💡 Lancelot, realize o upload para iniciar a análise.")

# ============================================================================
# 5. RODAPÉ
# ============================================================================
st.divider()
try:
    st.image("./assets/fundo.jpg", use_container_width=True)
except:
    st.caption("Portal dos Dados | Confiabilidade Aplicada")
