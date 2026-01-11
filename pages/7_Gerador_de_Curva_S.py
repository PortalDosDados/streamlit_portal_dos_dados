import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime

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
    # Estrutura padrão para download
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
            "Duração Realizada": [
                0.5,
                1.0,
                4.2,
                12.0,
                None,
            ],
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
    # Requer: pip install xlsxwriter
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_template.to_excel(writer, index=False, sheet_name="Cronograma")

        worksheet = writer.sheets["Cronograma"]
        for i, col in enumerate(df_template.columns):
            column_len = max(df_template[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_len)

    return output.getvalue()


# ============================================================================
# 4. INTERFACE DO USUÁRIO
# ============================================================================
st.title("📈 Acompanhamento de Projetos (Curva S)")
st.markdown("Transformando dados de engenharia em **Inteligência Preditiva**.")
st.markdown("---")

# LAYOUT VERTICAL: Botão acima do Upload
st.download_button(
    "📥 Baixar Modelo Excel",
    data=generate_excel_template(),
    file_name="modelo_curva_s.xlsx",
)

uploaded_file = st.file_uploader(
    "Upload do Cronograma", type=["xlsx"], label_visibility="visible"
)

# --- EXPANDER EXPLICATIVO ---
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

    # 1. O GRÁFICO
    st.markdown("### 📉 1. O Gráfico (A Corrida)")
    st.info(
        """
    Imagine duas linhas correndo em direção à meta (100%):
    * **Linha Azul (Planejado):** É a sua promessa. Onde você *deveria* estar hoje.
    * **Linha Verde (Realizado):** É a realidade. Onde você *realmente* está.

    **A Regra:** Se a linha Verde estiver **abaixo** da Azul, significa que estamos entregando menos do que o prometido para a data (Atraso). Se estiver **acima**, estamos adiantados.
    """
    )

    st.markdown("---")

    # 2. OS INDICADORES
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

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 1. Tratamento e Ordenação
    # Converter para datetime
    df["Início Planejado"] = pd.to_datetime(
        df["Início Planejado"], format="%d/%m/%Y - %H:%M", errors="coerce"
    )
    # Se houver erro no formato específico, tenta genérico
    mask_nat = df["Início Planejado"].isna()
    if mask_nat.any():
        df.loc[mask_nat, "Início Planejado"] = pd.to_datetime(
            df.loc[mask_nat, "Início Planejado"], errors="coerce", dayfirst=True
        )

    # ORDENAÇÃO: Para Curva de Aderência, usamos o Eixo do Planejado
    df.sort_values(by="Início Planejado", inplace=True)
    df.reset_index(drop=True, inplace=True)

    # 2. Conversão Numérica
    df["Duração Planejada"] = pd.to_numeric(
        df["Duração Planejada"], errors="coerce"
    ).fillna(0)
    df["Duração Realizada"] = pd.to_numeric(df["Duração Realizada"], errors="coerce")

    # 3. Cálculo dos Pesos (Weight)
    total_pl = df["Duração Planejada"].sum()

    # 4. Acumulado Planejado (Baseline)
    df["% Pl Acum"] = (df["Duração Planejada"] / total_pl).cumsum() * 100

    # 5. Acumulado Realizado (Com trava de Overburn)
    df["Progresso Computado"] = df.apply(
        lambda x: (
            min(x["Duração Realizada"], x["Duração Planejada"])
            if pd.notnull(x["Duração Realizada"])
            else 0
        ),
        axis=1,
    )

    df["% Re Acum"] = (df["Progresso Computado"] / total_pl).cumsum() * 100

    # Mascarar futuro
    mask_realizado = df["Duração Realizada"].notnull()
    df.loc[~mask_realizado, "% Re Acum"] = None

    # Último índice válido
    ultimo_idx_valid = df[mask_realizado].index.max()

    if pd.notnull(ultimo_idx_valid):
        # Valores de Referência
        valor_real_atual = df.loc[ultimo_idx_valid, "% Re Acum"]
        valor_plan_atual = df.loc[ultimo_idx_valid, "% Pl Acum"]

        # SPI
        spi = (valor_real_atual / valor_plan_atual) if valor_plan_atual > 0 else 1

        # Estimativas (Forecast)
        previsao_termino_teorico = 100 / spi if spi > 0 else 100
        desvio_final = previsao_termino_teorico - 100

        # --- CÁLCULO DE HORAS (GAP) ---
        estimativa_horas_total = total_pl / spi if spi > 0 else total_pl
        gap_horas = estimativa_horas_total - total_pl
        # ----------------------------

        # Regras de Status
        if desvio_final > 5:
            status_text, cor_status = "⚠️ POTENCIAL ATRASO", "#ffa726"
            if desvio_final > 15:
                status_text, cor_status = "🔴 CRÍTICO / ATRASO", "#ef5350"
        else:
            status_text, cor_status = "✅ NO PRAZO", "#66bb6a"

        # KPIs
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(
                f"""<div class="metric-card"><b>Eficiência (SPI)</b><br><h2>{spi:.2f}</h2></div>""",
                unsafe_allow_html=True,
            )
        with m2:
            cor_borda = "#ef5350" if desvio_final > 0 else "#66bb6a"
            # Exibe % e Horas
            st.markdown(
                f"""<div class="metric-card" style="border-left-color:{cor_borda}"><b>Desvio Estimado (Prazo)</b><br><h2>{desvio_final:+.1f}% <span style="font-size:0.6em; color:#555">({gap_horas:+.1f}h)</span></h2></div>""",
                unsafe_allow_html=True,
            )
        with m3:
            st.markdown(
                f"""<div class="metric-card" style="border-left-color:{cor_status}"><b>Status Geral</b><br><h2>{status_text}</h2></div>""",
                unsafe_allow_html=True,
            )

        # GRÁFICO
        fig = go.Figure()

        # Planejado
        fig.add_trace(
            go.Scatter(
                x=df["Início Planejado"],
                y=df["% Pl Acum"],
                name="Planejado (Baseline)",
                line=dict(color="#1f77b4", dash="dash"),
                hovertemplate="Planejado: %{y:.2f}%<extra></extra>",
            )
        )

        # Realizado
        fig.add_trace(
            go.Scatter(
                x=df["Início Planejado"],
                y=df["% Re Acum"],
                name="Realizado (Físico)",
                mode="lines+markers",
                line=dict(color="#00CC96", width=4),
                hovertemplate="Realizado: %{y:.2f}%<extra></extra>",
            )
        )

        fig.update_layout(
            template="plotly_white",
            height=500,
            title="Curva S de Aderência (Físico vs Planejado)",
            hovermode="x unified",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            yaxis=dict(title="% Avanço Acumulado", ticksuffix="%", range=[0, 110]),
            xaxis=dict(title="Cronograma (Data Planejada)"),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Auditoria
        with st.expander("🔍 Auditoria de Dados (Processado)"):
            cols_view = [
                "Atividade",
                "Duração Planejada",
                "Duração Realizada",
                "Progresso Computado",
                "% Pl Acum",
                "% Re Acum",
            ]
            st.dataframe(
                df[cols_view].style.format(
                    "{:.2f}",
                    subset=[
                        "Duração Planejada",
                        "Duração Realizada",
                        "Progresso Computado",
                        "% Pl Acum",
                        "% Re Acum",
                    ],
                    na_rep="-",
                )
            )

    else:
        st.warning('⚠️ Planilha carregada, mas sem dados na coluna "Duração Realizada".')
else:
    st.info("💡 Realize o upload para iniciar a análise.")

# ============================================================================
# 5. RODAPÉ
# ============================================================================
st.divider()
try:
    st.image("./assets/fundo.jpg", use_container_width=True)
except:
    st.caption("Portal dos Dados | Confiabilidade Aplicada")
