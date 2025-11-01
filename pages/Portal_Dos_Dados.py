import streamlit as st


# Foto no topo
st.image("../streamlit_portal_dos_dados/assets/portal.png", width=160)

# Configurações da página
st.set_page_config(
    page_title="Portal dos Dados",       # Título da aba
    page_icon="assets/portal.png",   # Ícone da aba (pode ser .ico, .png ou emoji)
    layout="wide"                        # Layout da página (opcional)
)

st.markdown("""
🎬 **Fala, pessoal!** 
 
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
 
Clique no link abaixo 👇
 
[Portal dos Dados no YouTube](https://www.youtube.com/@Portal_dos_Dados)

""")
