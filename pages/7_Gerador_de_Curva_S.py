import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime

# ============================================================================
# 1. SETUP INICIAL DA APLICAÇÃO
# ============================================================================
st.set_page_config(
    page_title="Portal dos Dados - Curva S & Tendência",
    page_icon="📈",
    layout="wide",
)


# ============================================================================
# 2. ESTILIZAÇÃO E RECURSOS VISUAIS
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
# 3. FUNÇÕES AUXILIARES E GERAÇÃO DE TEMPLATE
# ============================================================================
def generate_excel_template():
    # Definição do schema do DataFrame para exportação
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
            "Início Planejado": [
                "10/01/2025 - 08:00",
                "10/01/2025 - 09:00",
                "10/01/2025 - 11:00",
                "10/01/2025 - 15:00",
                "11/01/2025 - 01:00",
            ],
            "Término Planejado": [
                "10/01/2025 - 09:00",
                "10/01/2025 - 11:00",
                "10/01/2025 - 15:00",
                "11/01/2025 - 01:00",
                "11/01/2025 - 02:00",
            ],
            "Inicio Real": [
                "10/01/2025 - 08:00",
                "10/01/2025 - 08:30",
                "10/01/2025 - 09:30",
                "10/01/2025 - 13:42",
                None,
            ],
            "Término Real": [
                "10/01/2025 - 08:30",
                "10/01/2025 - 09:30",
                "10/01/2025 - 13:42",
                "11/01/2025 - 01:42",
                None,
            ],
        }
    )

    output = BytesIO()
    # Dependência: pip install xlsxwriter
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_template.to_excel(writer, index=False, sheet_name="Cronograma")

        worksheet = writer.sheets["Cronograma"]
        for i, col in enumerate(df_template.columns):
            column_len = max(df_template[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_len)

    return output.getvalue()


# ============================================================================
# 4. INTERFACE DE USUÁRIO (FRONTEND)
# ============================================================================
st.title("📈 Acompanhamento de Projetos (Curva S)")
st.markdown("Transformando dados de engenharia em **Inteligência Preditiva**.")
st.divider()

# Componentes de interação: Download e Upload
st.download_button(
    "📥 Baixar Modelo em Excel",
    data=generate_excel_template(),
    file_name="modelo_curva_s.xlsx",
)

# Instrução para carga de dados
st.markdown("### Clique aqui 👇 para carregar seu cronograma")

# Widget de Upload
uploaded_file = st.file_uploader("", type=["xlsx"], label_visibility="visible")


# --- SEÇÃO EDUCACIONAL (DOCUMENTAÇÃO INTEGRADA) ---
with st.expander("🎓 Como interpretar este Painel Inteligente?"):
    st.markdown(
        """
    <div style="background-color: #f0f7ff; padding: 20px; border-radius: 10px; border: 1px solid #b3d7ff; margin-bottom: 20px;">
        <p style="color: #004085; font-size: 1.1rem; font-weight: bold;">
            Bem-vindo ao GPS do seu Projeto.
        </p>
        <p style="color: #333; font-size: 0.95rem;">
            Esta ferramenta não apenas mostra o passado, mas usa seus dados para prever o futuro.
            Entenda abaixo como transformamos seus dados brutos em informação de decisão.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # 1. DOCUMENTAÇÃO DO GRÁFICO
    st.markdown("### 📉 1. O Gráfico (A Corrida)")
    st.info(
        """
    Imagine duas linhas correndo em direção à meta (100%):
    * **Linha Azul (Planejado):** É a sua promessa. Onde você *deveria* estar hoje.
    * **Linha Verde (Realizado):** É a realidade. Onde você *realmente* está.

    **A Regra:** Se a linha Verde estiver **abaixo** da Azul, significa que estamos entregando menos do que o prometido para a data (Atraso). Se estiver **acima**, estamos adiantados.
    """
    )

    st.divider()

    # 2. DOCUMENTAÇÃO DOS INDICADORES
    st.markdown("### 🧭 2. O que dizem os Indicadores (Cards)?")
    k1, k2, k3 = st.columns(3)

    with k1:
        st.markdown("**Eficiência (SPI)**")
        st.caption("É o velocímetro da equipe.")
        st.markdown(
            """
        * **1.00:** Velocidade exata.
        * **0.80:** Estamos andando a 80% da velocidade necessária (Lento).
        * **1.10:** Estamos 10% mais rápidos que o plano (Rápido).
        """
        )

    with k2:
        st.markdown("**Desvio Estimado**")
        st.caption("A Previsão do Tempo.")
        st.markdown(
            """
        Se a equipe mantiver o ritmo atual (SPI), qual será o resultado final?
        * **Positivo (+):** O projeto vai atrasar X%.
        * **Negativo (-):** O projeto vai terminar adiantado.
        """
        )

    with k3:
        st.markdown("**Status Geral**")
        st.caption("O Veredito.")
        st.markdown(
            """
        Um resumo automático baseado na gravidade do desvio.
        * 🟢 **No Prazo:** Desvio irrelevante.
        * 🟡 **Atenção:** Pequeno atraso.
        * 🔴 **Crítico:** Atraso que compromete a entrega.
        """
        )

st.divider()

# ============================================================================
# 5. PROCESSAMENTO DE DADOS E REGRAS DE NEGÓCIO
# ============================================================================

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.toast("Arquivo carregado! Iniciando processamento...", icon="🚀")

    # ------------------------------------------------------------------------
    # 5.1. ETL: TRATAMENTO E NORMALIZAÇÃO DE DADOS
    # ------------------------------------------------------------------------

    # Conversão de tipagem temporal (Datetime)
    date_columns = [
        "Início Planejado",
        "Término Planejado",
        "Inicio Real",
        "Término Real",
    ]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], format="%d/%m/%Y - %H:%M", errors="coerce")

    # Ordenação Cronológica (Essencial para cálculo acumulativo)
    df = df.sort_values(by="Início Planejado").reset_index(drop=True)

    # Cálculo da Baseline (Total Planejado)
    total_duracao_planejada = df["Duração Planejada"].sum()

    # Geração da Curva S Planejada (Baseline Acumulada)
    df["% Avanço Planejado Acumulado"] = (
        df["Duração Planejada"].cumsum() / total_duracao_planejada * 100
    )

    # ------------------------------------------------------------------------
    # 5.2. CÁLCULO DE PROGRESSO FÍSICO (REALIZADO)
    # ------------------------------------------------------------------------

    # Aplicação de regra de negócio: Trava de Eficiência (Realizado <= Planejado)
    df["Progresso Computado"] = df.apply(
        lambda x: (
            min(x["Duração Realizada"], x["Duração Planejada"])
            if pd.notnull(x["Duração Realizada"])
            else 0
        ),
        axis=1,
    )

    # Geração da Curva S Realizada (Normalizada pela Baseline)
    df["% Avanço Real Acumulado"] = (
        df["Progresso Computado"].cumsum() / total_duracao_planejada
    ) * 100

    # Tratamento de visualização: Mascaramento de dados futuros (Null Handling)
    # Identificação de registros sem apontamento (Forecast Area)
    mask_futuro = df["Duração Realizada"].isna()

    # Aplicação de máscara para interrupção gráfica
    df.loc[mask_futuro, "% Avanço Real Acumulado"] = None

    # ------------------------------------------------------------------------
    # 5.3. CÁLCULO DE KPIS E INDICADORES DE DESEMPENHO
    # ------------------------------------------------------------------------

    # Determinação da Data de Status (Data de Corte)
    ultimo_idx_valid = df[df["Duração Realizada"].notnull()].index.max()

    if pd.notnull(ultimo_idx_valid):
        # Extração de métricas na Data de Status
        percentual_realizado = df.loc[ultimo_idx_valid, "% Avanço Real Acumulado"]
        percentual_planejado = df.loc[ultimo_idx_valid, "% Avanço Planejado Acumulado"]

        # Cálculo do SPI (Schedule Performance Index)
        # Tratamento para evitar divisão por zero
        spi = (
            (percentual_realizado / percentual_planejado)
            if percentual_planejado > 0
            else 1.0
        )

        # Projeção de Tendência (Forecast)
        # Se SPI < 1, projeta-se extensão do prazo (valor positivo)
        desvio_estimado = (100 / spi) - 100 if spi > 0 else 0

    else:
        # Fallback para cenário sem apontamentos
        spi = 1.0
        desvio_estimado = 0.0

    # Lógica condicional para alertas visuais (Thresholds)
    if desvio_estimado > 5:
        status_text, cor_status = "⚠️ POTENCIAL ATRASO", "#ffa726"
        if desvio_estimado > 15:
            status_text, cor_status = "🔴 CRÍTICO / ATRASO", "#ef5350"
    else:
        status_text, cor_status = "✅ NO PRAZO", "#66bb6a"

    # Renderização dos Cards de Métricas
    k1, k2, k3 = st.columns(3)

    with k1:
        st.markdown(
            f"""<div class="metric-card"><b>Eficiência (SPI)</b><br><h2>{spi:.2f}</h2></div>""",
            unsafe_allow_html=True,
        )

    with k2:
        cor_borda = "#ef5350" if desvio_estimado > 0 else "#66bb6a"
        st.markdown(
            f"""<div class="metric-card" style="border-left-color:{cor_borda}"><b>Desvio Estimado</b><br><h2>{desvio_estimado:+.2f}%</h2></div>""",
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown(
            f"""<div class="metric-card" style="border-left-color:{cor_status}"><b>Status Geral</b><br><h2>{status_text}</h2></div>""",
            unsafe_allow_html=True,
        )

    st.divider()

    # Exibição tabular para auditoria de dados
    st.markdown("#### Visualização dos Dados Brutos")
    st.dataframe(df.drop(columns=["Progresso Computado"]))


# ============================================================================
# 6. TRATAMENTO DE EXCEÇÕES E UX
# ============================================================================

# Feedback caso nenhum arquivo tenha sido carregado
else:
    st.info("💡 Realize o upload para iniciar a análise.")

# ============================================================================
# 7. GRAFICO INTERATIVO DE CURVA S
# ============================================================================

# Renderização condicional do gráfico
if uploaded_file and pd.notnull(ultimo_idx_valid):
    st.markdown("### 📊 Gráfico Interativo de Curva S")

    fig = go.Figure()

    # Linha Planejada
    fig.add_trace(
        go.Scatter(
            x=df["Início Planejado"],
            y=df["% Avanço Planejado Acumulado"],
            mode="lines+markers",
            name="Planejado",
            line=dict(color="green", width=2),
            marker=dict(size=6),
        )
    )

    # Linha Realizada
    fig.add_trace(
        go.Scatter(
            x=df["Início Planejado"],
            y=df["% Avanço Real Acumulado"],
            mode="lines+markers",
            name="Realizado",
            line=dict(color="red", width=2),
            marker=dict(size=6),
        )
    )

    # Layout do gráfico
    fig.update_layout(
        title="Curva S - Planejado vs Realizado",
        xaxis_title="Atividades",
        yaxis_title="% Avanço Acumulado",
        yaxis=dict(range=[0, 110]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        hovermode="x unified",
        template="seaborn",
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# 8. COMPONENTES DE RODAPÉ
# ============================================================================
st.divider()
try:
    st.image("./assets/fundo.jpg", use_container_width=True)
except:
    st.caption("Portal dos Dados | Confiabilidade Aplicada")
