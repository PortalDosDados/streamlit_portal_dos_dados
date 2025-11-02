import streamlit as st

# Configurações da página
st.set_page_config(
    page_title='Dione Nascimento - Python',       # Título da aba
    page_icon='assets/python.gif',       # Ícone da aba (pode ser .ico, .png ou emoji)
    layout='wide'                        # Layout da página (opcional)
)

st.image('assets/python.gif', width= 160)

st.title("Python")
st.markdown("""
**Python** é a ferramenta para automatizar tarefas, analisar dados e desenvolver soluções eficientes que aumentam produtividade.
""")

st.subheader("Automação")
st.markdown("""
- Scripts que reduzem trabalho manual e repetitivo.
""")

st.subheader("Análise de dados")
st.markdown("""
- Manipulação de dados, geração de relatórios e insights estratégicos.
""")

st.subheader("Integrações")
st.markdown("""
- Conexão com APIs, banco de dados, Power Platform e ferramentas corporativas.
""")

st.markdown("**Quando não se agrega valor, se agrega custo.**")
