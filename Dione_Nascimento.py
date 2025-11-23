import streamlit as st

# Configurações iniciais da aplicação.
st.set_page_config(
    page_title='Dione Nascimento',
    page_icon='assets/portal.png',
    layout='wide'
)

# Carrega o arquivo de estilos CSS externo.
def load_css(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Erro: Arquivo de estilos '{file_path}' não encontrado.")

load_css("style.css")

# Layout principal
col1, col2 = st.columns([1, 4])

with col1:
    st.image('./assets/minha_foto.png', use_container_width=True)

with col2:
    st.markdown("""
    <div class="justificado">

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
    """, unsafe_allow_html=True)


# Banner
st.image('./assets/fundo.jpg', use_container_width=True)

# Seção institucional
st.markdown("""
**Portal dos Dados**, um canal do Youtube com o objetivo de compartilhar conteúdos práticos sobre:

- 🐍 **Python**
- 📊 **Power BI**
- 📱 **Power Apps**
- 🔄 **Power Automate**
- 🗄️ **SQL**
- ⚡ **Produtividade**
""")

# Título redes sociais
st.markdown("### Conecte-se comigo:")

# Botões nas 3 colunas
col_btn1, col_btn2, col_btn3, _ = st.columns([1, 1, 1, 2])

# LINKEDIN
with col_btn1:
    st.html("""
    <a href='https://www.linkedin.com/in/dione-nascimento-37287a233/' target='_blank' style='text-decoration: none;'>
        <button class="btn-linkedin">
            <svg viewBox="0 0 24 24" width="24" height="24">
                <path d="M19 0h-14c-2.761... (mesmo SVG) ..." fill="white"/>
            </svg>
            <span>LinkedIn</span>
        </button>
    </a>
    """)

# YOUTUBE
with col_btn2:
    st.html("""
    <a href='https://www.youtube.com/@Portal_dos_Dados' target='_blank' style='text-decoration: none;'>
        <button class="btn-youtube">
            <svg viewBox="0 0 24 24" width="24" height="24">
                <path d="M23.5 6.2s-.2-1.7... (mesmo SVG) ..." fill="white"/>
            </svg>
            <span>YouTube</span>
        </button>
    </a>
    """)

# GITHUB
with col_btn3:
    st.html("""
    <a href='https://github.com/PortalDosDados' target='_blank' style='text-decoration: none;'>
        <button class="btn-github">
            <svg viewBox="0 0 24 24" width="24" height="24">
                <path d="M12 .297c-6.63 0-12... (mesmo SVG) ..." fill="white"/>
            </svg>
            <span>GitHub</span>
        </button>
    </a>
    """)
