from datetime import datetime
from io import BytesIO
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from utils.ui import load_css, get_asset_path, render_footer, render_metric_card
from utils.business_rules import calcular_metricas_curva_s

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
load_css("style.css")


# ============================================================================
# 3. FUNÇÕES DE APOIO (BACKEND)
# ============================================================================
@st.cache_data
def generate_excel_template():
    """Gera o binário do arquivo Excel modelo para download com cache de performance."""
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
    try:
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_template.to_excel(writer, index=False, sheet_name="Cronograma")
    except Exception:
        with pd.ExcelWriter(output) as writer:
            df_template.to_excel(writer, index=False, sheet_name="Cronograma")

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

# Painel Educacional (Versão Premium com Explicação Matemática)
with st.expander("🎓 Guia de Interpretação e Tomada de Decisão"):

    # Organização em Abas
    tab_conceito, tab_kpi, tab_estrategia = st.tabs(
        ["📖 Leitura da Curva S", "🧭 Indicadores & Cálculo", "🧠 Estratégia"]
    )

    with tab_conceito:
        st.markdown(
            """
        ### O que o gráfico está dizendo?
        A Curva S é a representação visual da "saúde" física do seu projeto.

        * 🟢 **Linha Verde (Planejado/Baseline)**
        * 🔴 **Linha Vermelha (Realizado)**

        **Regra de Ouro:**
        Se a 🔴 **Vermelha** estiver **ABAIXO** da 🟢 **Verde** $\\rightarrow$ **O Projeto está ATRASADO.**
        """
        )

    with tab_kpi:
        col_spi, col_forecast = st.columns(2)

        with col_spi:
            st.markdown("#### ⚡ SPI (Índice de Desempenho)")
            st.markdown(
                """
            * 🟢 **SPI $\ge$ 1.00:** Eficiência Excelente.
            * 🟡 **SPI 0.90 - 0.99:** Atenção.
            * 🔴 **SPI < 0.90:** Crítico.
            """
            )

        with col_forecast:
            st.markdown("#### 🔮 Desvio Estimado (Forecast)")
            st.markdown(
                """
            Responde: *"Quando terminaremos se mantivermos esse ritmo?"*
            * **Valor Positivo:** Tempo extra necessário (Atraso).
            * **Valor Negativo:** Término antecipado.
            """
            )

        st.divider()
        st.markdown("### 🧮 Entenda a Matemática (Engenharia de Custos)")
        st.markdown(
            r"""
        O cálculo utiliza a metodologia de **Valor Agregado (EVM)** para projeção linear:

        $$
        SPI = \frac{\% \text{ Realizado}}{\% \text{ Planejado}}
        $$

        $$
        \text{Desvio Estimado \%} = \left( \frac{100}{SPI} \right) - 100
        $$

        **Exemplo:** Se você planejou 50% mas fez 40% ($SPI=0.8$), precisará de **+25%** de tempo extra para concluir os 100% do escopo.
        """
        )

    with tab_estrategia:
        st.markdown(
            """
        ### Como agir baseada nos dados?

        1.  **Analise o "Degrau":** Se a linha realizada ficar reta por muito tempo, houve bloqueio.
        2.  **Ajuste de Recursos:** Se SPI < 0.8, apenas hora extra não resolve. Revise o método.
        3.  **Confiabilidade:** O cálculo ignora "futuro". Tarefas não finalizadas não somam progresso.

        *Lembre-se: "Quando não se agrega valor, se agrega custo."*
        """
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
    # Remove espaços em branco invisíveis nos nomes das colunas
    df.columns = df.columns.str.strip()

    # Definição das colunas obrigatórias
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
        st.stop()

    st.toast("Arquivo validado com sucesso! Processando...", icon="🚀")

    # ------------------------------------------------------------------------
    # 5.1. ETL & NORMALIZAÇÃO
    # ------------------------------------------------------------------------
    date_columns = [
        "Início Planejado",
        "Término Planejado",
        "Inicio Real",
        "Término Real",
    ]
    for col in date_columns:
        if not pd.api.types.is_datetime64_any_dtype(df[col]):
            parsed = pd.to_datetime(df[col], format="%d/%m/%Y - %H:%M", errors="coerce")
            mask_failed = parsed.isna() & df[col].notna()
            if mask_failed.any():
                parsed.loc[mask_failed] = pd.to_datetime(
                    df.loc[mask_failed, col], dayfirst=True, errors="coerce"
                )
            df[col] = parsed

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
    # Regra de Negócio: Trava de Eficiência
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
    ultimo_idx_valid = df[df["Duração Realizada"].notnull()].index.max()

    if pd.notnull(ultimo_idx_valid):
        percentual_realizado = df.loc[ultimo_idx_valid, "% Avanço Real Acumulado"]
        percentual_planejado = df.loc[ultimo_idx_valid, "% Avanço Planejado Acumulado"]

        # SPI
        metricas = calcular_metricas_curva_s(
            percentual_realizado, percentual_planejado, total_duracao_planejada
        )
    else:
        metricas = calcular_metricas_curva_s(0.0, 0.0, total_duracao_planejada)

    spi = metricas["spi"]
    desvio_estimado = metricas["desvio_estimado"]
    gap_horas = metricas["gap_horas"]
    status_text = metricas["status_text"]
    cor_status = metricas["cor_status"]

    # Renderização dos Cards (KPIs)
    cor_borda = "#ef5350" if desvio_estimado > 0 else "#66bb6a"
    c1, c2, c3 = st.columns(3)
    with c1:
        cor_spi = "#00CC96" if spi >= 1.0 else "#ffa726" if spi >= 0.9 else "#ef5350"
        render_metric_card("Eficiência (SPI)", f"{spi:.2f}", subtitle="Índice de Prazo EVM", border_color=cor_spi)
    with c2:
        render_metric_card("Desvio Estimado", f"{desvio_estimado:+.2f}%", subtitle=f"Impacto: {gap_horas:+.1f}h", border_color=cor_borda)
    with c3:
        render_metric_card("Status Geral", status_text, subtitle="Classificação Preditiva", border_color=cor_status)

    st.divider()

    # ------------------------------------------------------------------------
    # 6. ENGENHARIA DE DADOS PARA O GRÁFICO
    # ------------------------------------------------------------------------
    # Preparação da Tabela para Exibição (Sem colunas de cálculo interno)
    df_curva_s = df.drop(
        columns=["Progresso Computado", "Duração Planejada", "Duração Realizada"]
    ).copy()

    # Cria rótulos legíveis para o Eixo X (Marcos)
    df["Marco Temporal"] = (
        df["Início Planejado"].dt.strftime("%d/%m %H:%M")
        + " - "
        + df["Término Planejado"].dt.strftime("%H:%M")
    )

    # Criação do "Ponto Zero" (Início do Projeto = 0%)
    inicio_projeto = df["Início Planejado"].min()
    label_zero = inicio_projeto.strftime("%d/%m %H:%M") + " (Início)"

    df_zero = pd.DataFrame(
        {
            "Marco Temporal": [label_zero],
            "% Avanço Planejado Acumulado": [0.0],
            "% Avanço Real Acumulado": [0.0],
        }
    )

    # União dos Dados: [Ponto Zero] + [Dados do Projeto]
    cols_plot = [
        "Marco Temporal",
        "% Avanço Planejado Acumulado",
        "% Avanço Real Acumulado",
    ]
    df_plot = pd.concat([df_zero, df[cols_plot]], ignore_index=True)

    # ------------------------------------------------------------------------
    # 7. VISUALIZAÇÃO GRÁFICA (PLOTLY)
    # ------------------------------------------------------------------------
    if pd.notnull(ultimo_idx_valid):
        st.markdown("### 📊 Gráfico Interativo de Curva S")

        fig = go.Figure()

        # Série Planejada
        fig.add_trace(
            go.Scatter(
                x=df_plot["Marco Temporal"],
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
            template="plotly_dark",
        )

        st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------------
    # 8. EXIBIÇÃO DA TABELA (POSICIONADA ABAIXO DO GRÁFICO)
    # ------------------------------------------------------------------------
    st.divider()
    st.markdown("#### Tabela de Dados Processados")
    st.dataframe(df_curva_s, use_container_width=True)


# Feedback caso nenhum arquivo tenha sido carregado
else:
    st.info("💡 Realize o upload para iniciar a análise.")

render_footer()
