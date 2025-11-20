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

# Título padrão do canal
st.header('🎬 Fala, pessoal!')

# Conteúdo principal
st.markdown('''
Sejam bem-vindos ao **Portal dos Dados**, um canal do Youtube com o objetivo de compartilhar conteúdos práticos sobre:

- 🐍 **Python**: scripts e automações para simplificar tarefas do dia a dia  
- 📊 **Power BI**: dashboards e análises interativas que dão visão estratégica  
- 📱 **Power Apps**: criação de aplicativos corporativos de forma rápida e prática  
- 🔄 **Power Automate**: automação de processos e integração de dados  
- 🗄️ **SQL**: consultas e manipulação de dados aplicadas à engenharia  
- ⚡ **Dicas de produtividade**: técnicas para otimizar seu trabalho com dados

Este canal é feito para você que quer **aprender na prática, aplicar conhecimento e gerar resultados reais**.

Se você curte dados, tecnologia e soluções inteligentes, aqui é o seu lugar!

**Vamos juntos transformar dados em valor real!**

Clique no link abaixo para saber mais 👇

''')

#Botão do Canal
st.markdown("""
<a href='https://www.youtube.com/@Portal_dos_Dados' target='_blank'>
    <button class="btn-youtube">
        <svg viewBox="0 0 24 24">
            <path d="M23.5 6.2s-.2-1.7-.8-2.4c-.8-.9-1.7-.9-2.1-1C17.4 2.5 12 2.5 12 2.5h-.1s-5.4 0-8.6.3c-.4.1-1.3.1-2.1 1C1.5 
            4.5 1.3 6.2 1.3 6.2S1 8.3 1 10.5v1.9c0 2.2.3 4.3.3 4.3s.2 1.7.8 2.4c.8.9 1.9.9 2.4 
            1C7 20 12 20 12 20s5.4 0 8.6-.3c.4-.1 1.3-.1 2.1-1 .6-.7.8-2.4.8-2.4s.3-2.1.3-4.3v-1.9c0-2.2-.3-4.3-.3-4.3zM9.8 15.3V8.7l6.4 
            3.3-6.4 3.3z"/>
        </svg>
        Conheça meu Canal
    </button>
</a>
""", unsafe_allow_html=True)

