import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta, date
import base64
import io
import vl_convert as vlc

# ---------------------------------------------
# FUNÇÃO PARA CALCULAR A SEMANA DO ANO (ISO 8601)
# ---------------------------------------------
def calcular_semana_iso(data):
    return data.isocalendar().week

# ---------------------------------------------
# FUNÇÃO PARA GERAR O DATAFRAME DO CALENDÁRIO
# ---------------------------------------------
def gerar_calendario(ano, df_paradas):
    inicio = date(ano, 1, 1)
    fim = date(ano, 12, 31)

    dias = []
    atual = inicio
    while atual <= fim:
        dias.append({
            "data": atual,
            "dia": atual.day,
            "mes": atual.month,
            "semana_ano": calcular_semana_iso(atual),
            "dia_semana": atual.weekday()
        })
        atual += timedelta(days=1)

    df_cal = pd.DataFrame(dias)

    df_final = df_cal.merge(df_paradas, on="data", how="left")
    df_final["tipo_parada"] = df_final["tipo_parada"].fillna("Nenhuma")

    return df_final

# ---------------------------------------------
# FUNÇÃO PARA GERAR O HEATMAP
# ---------------------------------------------
def gerar_grafico(df, ano):
    return (
        alt.Chart(df)
        .mark_rect()
        .encode(
            x=alt.X("dia:O", title="Dia do mês"),
            y=alt.Y("semana_ano:O", title="Semana do ano"),
            color=alt.Color("tipo_parada:N", title="Tipo da Parada"),
            tooltip=["data", "tipo_parada"]
        )
        .properties(
            width=900,
            height=600,
            title=f"Mapa de Calor de Paradas - {ano}"
        )
    )

# ---------------------------------------------
# INTERFACE STREAMLIT
# ---------------------------------------------
st.title("WeekFlow | Gestão de Paradas")

uploaded_file = st.file_uploader("Envie o Excel com as paradas:", type=["xlsx"])

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)

    # Aqui assumo os nomes das colunas: "data" e "tipo_parada"
    df_raw["data"] = pd.to_datetime(df_raw["data"]).dt.date

    ano = st.selectbox("Selecione o ano:", [2024, 2025])

    df_cal = gerar_calendario(ano, df_raw)

    grafico = gerar_grafico(df_cal, ano)
    st.altair_chart(grafico, use_container_width=True)

    col_btn_img = st.container()

    with col_btn_img:
        try:
            grafico_export = grafico.configure(background="white") \
                .configure_axis(labelColor="black", titleColor="black") \
                .configure_legend(labelColor="black", titleColor="black") \
                .configure_title(color="black")

            png_data = vlc.vegalite_to_png(
                grafico_export.to_json(),
                scale=3   # AUMENTA A RESOLUÇÃO DA IMAGEM
            )

            st.download_button(
                "📷 Baixar Mapa (Imagem)",
                png_data,
                f"mapa_{ano}.png",
                "image/png",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Erro ao gerar imagem: {e}")
