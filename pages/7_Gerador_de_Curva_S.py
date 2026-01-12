import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime

# ============================================================================
# 1. SETUP E CONFIGURAÇÕES GERAIS
# ============================================================================
st.set_page_config(
    page_title="Portal dos Dados - Curva S & Tendência",
    page_icon="📈",
    layout="wide",
)


# ============================================================================
# 2. ESTILIZAÇÃO (CSS) E ASSETS
# ============================================================================
def carregar_css(nome_arquivo):
    """Carrega arquivo CSS externo para estilização personalizada."""
    try:
        with open(nome_arquivo, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


# Carrega CSS externo e aplica estilos inline para KPIs e Botões
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
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================================
# 3. FUNÇÕES DE APOIO (BACKEND)
# ============================================================================
def generate_excel_template():
    """Gera o binário do arquivo Excel modelo para download."""
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
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_template.to_excel(writer, index=False, sheet_name="Cronograma")
        # Ajuste automático de largura de colunas
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

# Botão de Download
st.download_button(
    "📥 Baixar Modelo em Excel",
    data=generate_excel_template(),
    file_name="modelo_curva_s.xlsx",
)

# Widget de Upload
st.markdown("### Clique aqui 👇 para carregar seu cronograma")
uploaded_file = st.file_uploader("", type=["xlsx"], label_visibility="visible")

# Painel Educacional
with st.expander("🎓 Como interpretar este Painel Inteligente?"):
    st.markdown(
        """
        <div style="background-color: #f0f7ff; padding: 20px; border-radius: 10px; border: 1px solid #b3d7ff;">
            <p style="color: #004085; font-weight: bold;">Bem-vindo ao GPS do seu Projeto.</p>
            <p style="color: #333;">Esta ferramenta compara o Avanço Físico (Realizado) contra o Cronograma (Planejado).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(
        "Regra de Ouro: Linha Verde abaixo da Azul indica atraso. Acima, indica adiantamento."
    )
    st.divider()
    k1, k2, k3 = st.columns(3)
    k1.markdown(
        "**Eficiência (SPI)**: <br>Velocímetro do projeto (1.0 = Pontual).",
        unsafe_allow_html=True,
    )
    k2.markdown(
        "**Desvio Estimado**: <br>Quanto % o projeto tende a atrasar ou adiantar.",
        unsafe_allow_html=True,
    )
    k3.markdown(
        "**Status Geral**: <br>Diagnóstico automático de criticidade.",
        unsafe_allow_html=True,
    )

st.divider()

# ============================================================================
# 5. MOTOR DE PROCESSAMENTO DE DADOS (CORE)
# ============================================================================

if uploaded_file:
    # Leitura do Arquivo
    df = pd.read_excel(uploaded_file)

    # ------------------------------------------------------------------------
    # 5.0. HIGIENIZAÇÃO E VALIDAÇÃO DE ESTRUTURA (BLINDAGEM)
    # ------------------------------------------------------------------------
    # Remove espaços em branco invisíveis nos nomes das colunas (ex: "Início " -> "Início")
    df.columns = df.columns.str.strip()

    # Definição das colunas obrigatórias para o algoritmo
    required_cols = [
        "Início Planejado",
        "Término Planejado",
        "Inicio Real",
        "Término Real",
        "Duração Planejada",
        "Duração Realizada",
    ]

    # Verifica se alguma coluna obrigatória está faltando
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        st.error("❌ **Erro na Estrutura do Arquivo**")
        st.warning(
            f"O arquivo carregado não possui as colunas obrigatórias: **{missing_cols}**"
        )
        st.info(
            "💡 Dica: Verifique se os nomes estão idênticos ao modelo (inclusive acentos)."
        )
        st.stop()  # Interrompe a execução imediatamente para evitar o crash (KeyError)

    st.toast("Arquivo validado com sucesso! Processando...", icon="🚀")

    # ------------------------------------------------------------------------
    # 5.1. ETL & NORMALIZAÇÃO
    # ------------------------------------------------------------------------
    # Conversão de Strings para Datetime
    date_columns = [
        "Início Planejado",
        "Término Planejado",
        "Inicio Real",
        "Término Real",
    ]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], format="%d/%m/%Y - %H:%M", errors="coerce")

    # Ordenação Cronológica Fundamental
    df = df.sort_values(by="Início Planejado").reset_index(drop=True)

    # Cálculo da Baseline Total (Denominador)
    total_duracao_planejada = df["Duração Planejada"].sum()

    # Cálculo da Curva Planejada (Acumulado)
    df["% Avanço Planejado Acumulado"] = (
        (df["Duração Planejada"].cumsum() / total_duracao_planejada * 100)
    ).round(2)

    # ------------------------------------------------------------------------
    # 5.2. CÁLCULO DE PROGRESSO FÍSICO (REALIZADO)
    # ------------------------------------------------------------------------
    # Regra de Negócio: Trava de Eficiência (Realizado nunca excede o Planejado por tarefa)
    df["Progresso Computado"] = df.apply(
        lambda x: (
            min(x["Duração Realizada"], x["Duração Planejada"])
            if pd.notnull(x["Duração Realizada"])
            else 0
        ),
        axis=1,
    )

    # Cálculo da Curva Realizada (Acumulado)
    df["% Avanço Real Acumulado"] = (
        (df["Progresso Computado"].cumsum() / total_duracao_planejada) * 100
    ).round(2)

    # Mascaramento de Futuro (Forecast Area)
    mask_futuro = df["Duração Realizada"].isna()
    df.loc[mask_futuro, "% Avanço Real Acumulado"] = None

    # ------------------------------------------------------------------------
    # 5.3. CÁLCULO DE KPIS E DASHBOARD
    # ------------------------------------------------------------------------
    # Identifica a Data de Status (Corte)
    ultimo_idx_valid = df[df["Duração Realizada"].notnull()].index.max()

    if pd.notnull(ultimo_idx_valid):
        # Captura snapshots na data de corte
        percentual_realizado = df.loc[ultimo_idx_valid, "% Avanço Real Acumulado"]
        percentual_planejado = df.loc[ultimo_idx_valid, "% Avanço Planejado Acumulado"]

        # SPI (Schedule Performance Index)
        spi = (
            (percentual_realizado / percentual_planejado)
            if percentual_planejado > 0
            else 1.0
        )

        # Forecast (Estimativa de Desvio Final)
        desvio_estimado = (100 / spi) - 100 if spi > 0 else 0
    else:
        spi = 1.0
        desvio_estimado = 0.0

    # Definição de Cores e Status
    if desvio_estimado > 5:
        status_text, cor_status = "⚠️ POTENCIAL ATRASO", "#ffa726"
        if desvio_estimado > 15:
            status_text, cor_status = "🔴 CRÍTICO / ATRASO", "#ef5350"
    else:
        status_text, cor_status = "✅ NO PRAZO", "#66bb6a"

    # Renderização dos Cards (KPIs)
    c1, c2, c3 = st.columns(3)
    c1.markdown(
        f"""<div class="metric-card"><b>Eficiência (SPI)</b><br><h2>{spi:.2f}</h2></div>""",
        unsafe_allow_html=True,
    )

    cor_borda = "#ef5350" if desvio_estimado > 0 else "#66bb6a"
    c2.markdown(
        f"""<div class="metric-card" style="border-left-color:{cor_borda}"><b>Desvio Estimado</b><br><h2>{desvio_estimado:+.2f}%</h2></div>""",
        unsafe_allow_html=True,
    )

    c3.markdown(
        f"""<div class="metric-card" style="border-left-color:{cor_status}"><b>Status Geral</b><br><h2>{status_text}</h2></div>""",
        unsafe_allow_html=True,
    )

    st.divider()

    # ------------------------------------------------------------------------
    # 6. TABELA ANALÍTICA
    # ------------------------------------------------------------------------
    # Prepara DF limpo para exibição
    df_curva_s = df.drop(
        columns=["Progresso Computado", "Duração Planejada", "Duração Realizada"]
    ).copy()

    # ------------------------------------------------------------------------
    # 7. ENGENHARIA DE DADOS PARA O GRÁFICO (PONTO ZERO + MARCOS)
    # ------------------------------------------------------------------------

    # 1. Cria rótulos legíveis para o Eixo X (Marcos: Início -> Fim)
    df["Marco Temporal"] = (
        df["Início Planejado"].dt.strftime("%d/%m %H:%M")
        + " - "
        + df["Término Planejado"].dt.strftime("%H:%M")
    )

    # 2. Criação do "Ponto Zero" (Início do Projeto = 0%)
    # Isso garante que o gráfico nasça na origem (0%) antes da primeira entrega
    inicio_projeto = df["Início Planejado"].min()
    label_zero = inicio_projeto.strftime("%d/%m %H:%M") + " (Início)"

    df_zero = pd.DataFrame(
        {
            "Marco Temporal": [label_zero],
            "% Avanço Planejado Acumulado": [0.0],
            "% Avanço Real Acumulado": [0.0],
        }
    )

    # 3. União dos Dados: [Ponto Zero] + [Dados do Projeto]
    cols_plot = [
        "Marco Temporal",
        "% Avanço Planejado Acumulado",
        "% Avanço Real Acumulado",
    ]
    df_plot = pd.concat([df_zero, df[cols_plot]], ignore_index=True)

    # ------------------------------------------------------------------------
    # 8. PLOTAGEM DO GRÁFICO (PLOTLY)
    # ------------------------------------------------------------------------
    if pd.notnull(ultimo_idx_valid):
        st.markdown("### 📊 Gráfico Interativo de Curva S")

        fig = go.Figure()

        # Série Planejada
        fig.add_trace(
            go.Scatter(
                x=df_plot["Marco Temporal"],  # Eixo X Categórico (Marcos)
                y=df_plot["% Avanço Planejado Acumulado"],
                mode="lines+markers",
                name="Planejado",
                line=dict(color="green", width=2),
                marker=dict(size=6),
            )
        )

        # Série Realizada
        fig.add_trace(
            go.Scatter(
                x=df_plot["Marco Temporal"],
                y=df_plot["% Avanço Real Acumulado"],
                mode="lines+markers",
                name="Realizado",
                line=dict(color="red", width=2),
                marker=dict(size=6),
            )
        )

        # Configuração de Layout
        fig.update_layout(
            title="Curva S - Marcos de Entrega",
            xaxis_title="Marcos Temporais (Início -> Entregas)",
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

    # ------------------------------------------------------------------------
    # 9. EXIBIÇÃO DA TABELA DE DADOS
    st.markdown("#### Tabela de Dados Processados")
    st.dataframe(df_curva_s, use_container_width=True)


# Feedback caso nenhum arquivo tenha sido carregado
else:
    st.info("💡 Realize o upload para iniciar a análise.")

# ============================================================================
# 9. RODAPÉ
# ============================================================================
st.divider()
try:
    st.image("./assets/fundo.jpg", use_container_width=True)
except:
    st.caption("Portal dos Dados | Confiabilidade Aplicada")
