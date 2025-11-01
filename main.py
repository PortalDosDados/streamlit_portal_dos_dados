import streamlit as st

# Foto no topo
st.image("../streamlit_portal_dos_dados/assets/minha_foto.jpg", width=160)

# Configurações da página
st.set_page_config(
    page_title="Portal dos Dados",       # Título da aba
    page_icon="assets/portal.png",   # Ícone da aba (pode ser .ico, .png ou emoji)
    layout="wide"                        # Layout da página (opcional)
)

# Texto de introdução
st.markdown('''
Olá! Sou **Dione Nascimento**, um profissional com **15 anos de experiência em Manutenção Industrial**. 

Tenho um canal no YouTube chamado **Portal dos Dados** , onde produzo conteúdos educativos voltados para **profissionais de engenharia e dados**, mostrando como transformar informações em decisões estratégicas e resultados reais.  



**Meu objetivo é ajudar pessoas compartilhando conhecimento, assim como outros fizeram por mim ao longo da minha trajetória**.  
''')
