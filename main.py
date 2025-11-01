import streamlit as st
from utils import style

st.set_page_config(
    page_title="Portal dos Dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

style.load_css()

col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.png", width=100)
with col2:
    st.title("Portal dos Dados")

st.markdown("""
Bem-vindo ao **Portal dos Dados**, um espaço onde compartilho projetos e aprendizados sobre 
**Engenharia de Produção**, **Confiabilidade Mecânica**, **SAP PM**, **Power BI**, **Python** e **Automação de Processos**.
""")

st.info("Acesse as páginas laterais para explorar meus projetos e experiências.")
st.markdown("---")

st.subheader("Últimos projetos em destaque")
st.write("📊 Dashboard de confiabilidade — Power BI")
st.write("🤖 Automação de relatórios SAP PM — Python")
st.write("🧠 Análise de falhas mecânicas — SQL + Power BI")
