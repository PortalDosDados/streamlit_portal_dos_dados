import streamlit as st

# Função para carregar CSS externo
def load_css(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carrega o style.css
load_css("style.css")

# Configurações da página
st.set_page_config(
    page_title='Dione Nascimento - Portal dos Dados',
    page_icon='assets/portal.png',
    layout='wide'
)

# Banner principal (ajuste o caminho conforme sua estrutura real)
st.image('assets/fundo.jpg', use_container_width=True)

