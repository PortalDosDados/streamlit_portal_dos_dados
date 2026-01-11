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
    # Definindo a estrutura conforme solicitado
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
            ],  # Exemplo com "Overburn" na vulcanização
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

        # Ajuste cosmético de colunas
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

# --- EXPANDER EXPLICATIVO ---
with st.expander("🎓 Fundamentos Técnicos e Lógica dos Cálculos"):
    st.markdown(
        """
    <div style="background-color: #f0f7ff; padding: 20px; border-radius: 10px; border: 1px solid #b3d7ff;">
        <p style="color: #004085; font-size: 1.1rem; font-weight: bold;">
            Metodologia de Cálculo (Confiabilidade):
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    col_log1, col_log2 = st.columns(2)
    with col_log1:
        st.markdown("### 📊 Correção de Avanço Físico")
        st.write(
            """
        Para evitar distorções (falsos avanços), aplicamos uma trava lógica:
        **O avanço realizado de uma tarefa nunca excede o seu peso planejado.**
        Se uma tarefa de 10h leva 12h, computamos 10h de avanço e 2h de ineficiência.
        """
        )
    with col_log2:
        st.markdown("### 🚀 Ordenação Cronológica")
        st.write(
            "O algoritmo reordena automaticamente as tarefas pelo Término Planejado para garantir a integridade matemática da curva acumulada (S-Curve)."
        )

st.divider()

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 1. Tratamento e Ordenação
    # Converter para datetime para permitir ordenação correta
    df["Término Planejado"] = pd.to_datetime(
        df["Término Planejado"], format="%d/%m/%Y - %H:%M", errors="coerce"
    )

    # ORDENAÇÃO: Crucial para a Curva S fazer sentido
    df.sort_values(by="Término Planejado", inplace=True)
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
    # Lógica: Se realizei 12h mas era 10h, considero 10h para progresso físico.
    df["Progresso Computado"] = df.apply(
        lambda x: (
            min(x["Duração Realizada"], x["Duração Planejada"])
            if pd.notnull(x["Duração Realizada"])
            else 0
        ),
        axis=1,
    )

    # Calcula o realizado acumulado apenas até onde temos dados (para não zerar o gráfico no futuro)
    df["% Re Acum"] = (df["Progresso Computado"] / total_pl).cumsum() * 100

    # Mascaremos o futuro (onde não houve input de realizado) com NaN para o gráfico cortar a linha
    mask_realizado = df["Duração Realizada"].notnull()
    df.loc[~mask_realizado, "% Re Acum"] = None

    # Último índice válido (para cálculo de SPI e Projeção)
    ultimo_idx_valid = df[mask_realizado].index.max()

    if pd.notnull(ultimo_idx_valid):
        # Definição dos valores de referência no ponto de corte (Data Status)
        valor_real_atual = df.loc[ultimo_idx_valid, "% Re Acum"]
        valor_plan_atual = df.loc[ultimo_idx_valid, "% Pl Acum"]

        # SPI - Schedule Performance Index
        spi = (valor_real_atual / valor_plan_atual) if valor_plan_atual > 0 else 1

        # Cálculo da Tendência (Forecast)
        # Copia o realizado até o ponto de corte
        df["Tendencia"] = df["% Re Acum"]

        # Projeta o futuro
        val_projecao = valor_real_atual
        for i in range(ultimo_idx_valid + 1, len(df)):
            peso_tarefa = (df.loc[i, "Duração Planejada"] / total_pl) * 100

            # Se SPI > 0, aplicamos a eficiência. Se SPI for ruim, a curva inclina.
            fator_ajuste = spi if spi > 0 else 1.0

            # Incremento projetado = Peso / SPI (Se SPI < 1, gasta mais "tempo" para o mesmo peso, mas aqui plotamos avanço físico x tempo)
            # Na curva S física x cronograma, a projeção mostra quando atingiremos 100%.
            # Simplificação linear para visualização no mesmo eixo X de atividades:
            val_projecao += peso_tarefa  # Assume que completaremos o escopo restante

            # Nota: Uma projeção temporal real exigiria alterar o eixo X (Datas).
            # Aqui projetamos a "Tendência de Atingimento" se o cronograma fosse mantido fixo.
            df.loc[i, "Tendencia"] = val_projecao

            # Ajuste fino: Se o SPI for muito baixo, visualmente poderíamos mostrar que não chega a 100% no prazo.
            # Vamos aplicar o SPI ao inverso: Desvio Final.

        # O Desvio Final real é melhor calculado comparando: (100% / SPI) vs 100%.
        # Ex: Se SPI é 0.8, levarei 125% do tempo.
        previsao_termino_teorico = 100 / spi if spi > 0 else 100
        desvio_final = previsao_termino_teorico - 100  # +25% de atraso, por exemplo.

        # Regras de Status
        if desvio_final > 5:  # Tolerância de 5%
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
            st.markdown(
                f"""<div class="metric-card" style="border-left-color:{cor_borda}"><b>Desvio de Prazo Est.</b><br><h2>{desvio_final:+.1f}%</h2></div>""",
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
                x=df["Atividade"],
                y=df["% Pl Acum"],
                name="Planejado (Baseline)",
                line=dict(color="#1f77b4", dash="dash"),
                hovertemplate="Planejado: %{y:.2f}%<extra></extra>",
            )
        )

        # Realizado
        fig.add_trace(
            go.Scatter(
                x=df["Atividade"],  # Plota todos os eixos X
                y=df["% Re Acum"],  # Onde é None, o Plotly não desenha a linha
                name="Realizado (Físico)",
                mode="lines+markers",
                line=dict(color="#00CC96", width=4),
                hovertemplate="Realizado: %{y:.2f}%<extra></extra>",
            )
        )

        # Para a projeção visual no gráfico de Atividades (Eixo X Categórico),
        # é difícil mostrar "atraso temporal" (deslocamento para direita).
        # Vamos mostrar apenas o ponto final esperado.

        fig.update_layout(
            template="plotly_white",
            height=500,
            title="Curva S de Avanço Físico",
            hovermode="x unified",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            yaxis=dict(title="% Avanço Acumulado", ticksuffix="%", range=[0, 110]),
            xaxis=dict(title="Sequência de Atividades"),
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
    st.info("💡 Lancelot, realize o upload para iniciar a análise.")

# ============================================================================
# 5. RODAPÉ
# ============================================================================
st.divider()
try:
    st.image("./assets/fundo.jpg", use_container_width=True)
except:
    st.caption("Portal dos Dados | Confiabilidade Aplicada")
