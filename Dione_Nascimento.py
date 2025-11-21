import streamlit as st

# Função para carregar estilos personalizados
def load_css(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# Configurações da página
st.set_page_config(
    page_title='Dione Nascimento',
    page_icon='assets/portal.png',
    layout='wide'
)

# Criação das colunas com proporção mais impactante
col1, col2 = st.columns([1.2, 3])

with col1:
    st.image('./assets/minha_foto.png', use_container_width=True)

with col2:
    st.markdown('''
    <div style="
        max-width: 100%; 
        background-color: #f9f9f9; 
        text-align: justify; 
        padding: 5%; 
        border-radius: 12px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        font-size: 1em;
        line-height: 1.6;
        word-wrap: break-word;
    ">
        <p>Olá! Sou <b>Dione Nascimento</b>, profissional com <b>15 anos de experiência em Manutenção Industrial</b>, especializado em <b>Gestão de Ativos</b> e <b>Análise de Dados</b>. Minha atuação combina metodologias de manutenção com soluções de Business Intelligence para transformar dados operacionais em decisões rápidas e precisas.</p>
        <p>Minha trajetória começou no SENAI, onde atuei como <b>jovem aprendiz</b> e depois como <b>professor</b>. Nos últimos 10 anos, venho trabalhando no <b>setor siderúrgico</b>, desenvolvendo projetos focados em:</p>
        <ul>
            <li><b>Confiabilidade de equipamentos</b></li>
            <li><b>Digitalização da manutenção</b></li>
            <li><b>Automação de análises e indicadores</b></li>
        </ul>
        <p>Converto dados de campo em inteligência aplicada, melhoro planos de manutenção e estruturo processos que elevam desempenho e reduzem custos.</p>
        <p>Sou também o criador do <b>Portal dos Dados</b>, projeto que conecta <b>Engenharia</b> e <b>Ciência de Dados</b> para ajudar profissionais a tomar decisões orientadas por dados reais e aplicáveis ao dia a dia da manutenção.</p>
    </div>
    ''', unsafe_allow_html=True)


# Banner principal
st.image('./assets/fundo.jpg', use_container_width=True)

# Apresentação do canal
st.markdown('''
**Portal dos Dados**, um canal do Youtube com o objetivo de compartilhar conteúdos práticos sobre:
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

# Botão do Canal
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
