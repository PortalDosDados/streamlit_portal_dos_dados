import streamlit as st


# Configurações da página
st.set_page_config(
    page_title='Dione Nascimento - Power BI',       # Título da aba
    page_icon='assets/power_bi.png',   # Ícone da aba (pode ser .ico, .png ou emoji)
    layout='wide'                        # Layout da página (opcional)
)

st.image('assets/power_bi.png', width= 160)
st.title("Power BI")
st.markdown("""
O **Power BI** permite visualizar dados de forma clara, interativa e estratégica. Com dashboards inteligentes, você consegue transformar números em decisões.
""")

st.subheader("Dashboards e relatórios")
st.markdown("""
- Indicadores e KPIs aplicados à manutenção e produção.
- Relatórios interativos para análise rápida.
""")

st.subheader("Análise de dados")
st.markdown("""
Interprete métricas, descubra tendências e tome decisões baseadas em fatos.
""")

st.subheader("Integração de dados")
st.markdown("""
Combine fontes diversas, como Excel, SQL e APIs externas, para uma visão completa.
""")

st.markdown("**Quando não se agrega valor, se agrega custo.**")
