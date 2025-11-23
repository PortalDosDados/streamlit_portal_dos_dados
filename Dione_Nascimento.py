import streamlit as st

# Configurações iniciais da aplicação.
# Esta chamada deve permanecer no topo para evitar warnings e garantir que
# a configuração de página seja aplicada corretamente.
st.set_page_config(
    page_title='Dione Nascimento',
    page_icon='assets/portal.png',
    layout='wide'
)

# Carrega o arquivo de estilos CSS externo e aplica seu conteúdo ao Streamlit.
def load_css(file_path: str):
    """Carrega e injeta o arquivo CSS especificado na aplicação."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Erro: Arquivo de estilos '{file_path}' não encontrado.")

# Importação do CSS principal da aplicação.
load_css("style.css")

# Estruturação do layout inicial com duas colunas proporcionais.
col1, col2 = st.columns([1, 4])

# Coluna 1: Exibição da imagem principal do perfil.
with col1:
    st.image('./assets/minha_foto.png', use_container_width=True)

# Coluna 2: Card com descrição profissional e objetivos do projeto.
with col2:
    st.markdown("""
        <div class="justificado">
            <p>Olá! Sou <b>Dione Nascimento</b>, profissional com <b>15 anos de experiência em Manutenção Industrial</b>, especializado em <b>Gestão de Ativos</b> e <b>Análise de Dados</b>. Minha atuação combina metodologias de manutenção com soluções de Business Intelligence para transformar dados operacionais em decisões rápidas e precisas.</p>
            <p>Minha trajetória começou no SENAI, onde atuei como <b>jovem aprendiz</b> e depois como <b>professor</b>. 
            Nos últimos 10 anos, venho trabalhando no <b>setor siderúrgico</b>, desenvolvendo projetos focados em:</p>
            <ul>
                <li><b>Confiabilidade de equipamentos</b></li>
                <li><b>Digitalização da manutenção</b></li>
                <li><b>Automação de análises e indicadores</b></li>
            </ul>
            <p>Converto dados de campo em inteligência aplicada, melhoro planos de manutenção e estruturo processos que elevam desempenho e reduzem custos.</p>
            <p>Sou também o criador do <b>Portal dos Dados</b>, projeto que conecta <b>Engenharia</b> e <b>Ciência de Dados</b> para ajudar profissionais a tomar decisões orientadas por dados reais e aplicáveis ao dia a dia da manutenção.</p>
        </div>
    """, unsafe_allow_html=True)

# Exibição do banner principal da página.
st.image('./assets/fundo.jpg', use_container_width=True)

# Seção institucional apresentando o propósito do canal Portal dos Dados.
st.markdown("""
**Portal dos Dados**, um canal do Youtube com o objetivo de compartilhar conteúdos práticos sobre:

- 🐍 **Python**: scripts e automações aplicadas ao dia a dia  
- 📊 **Power BI**: dashboards e análises com foco operacional  
- 📱 **Power Apps**: desenvolvimento rápido de aplicativos corporativos  
- 🔄 **Power Automate**: integração e automação de processos  
- 🗄️ **SQL**: consultas aplicadas à engenharia e manutenção  
- ⚡ **Produtividade**: técnicas para melhorar desempenho profissional

Conteúdo focado em aplicação prática, aprendizado direto e geração de resultados reais.
""")


# Seção de Botões de Redes Sociais
st.markdown("### Conecte-se comigo:")

# Cria 3 colunas para os botões e uma coluna vazia para espaçamento
col_btn1, col_btn2, col_btn3, col_vazia = st.columns([1, 1, 1, 2])

with col_btn1:
    # Botão do LinkedIn
    st.html("""
    <a href='https://www.linkedin.com/in/dione-nascimento-37287a233/' target='_blank' style='text-decoration: none;'>
        <button class="btn-linkedin">
            <svg viewBox="0 0 24 24" width="24" height="24">
                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" fill="white"/>
            </svg>
            <span>LinkedIn</span>
        </button>
    </a>
    """)

with col_btn2:
    # Botão do YouTube
    st.html("""
    <a href='https://www.youtube.com/@Portal_dos_Dados' target='_blank' style='text-decoration: none;'>
        <button class="btn-youtube">
            <svg viewBox="0 0 24 24" width="24" height="24">
                <path d="M23.5 6.2s-.2-1.7-.8-2.4c-.8-.9-1.7-.9-2.1-1C17.4 2.5 12 2.5 12 2.5h-.1s-5.4 0-8.6.3c-.4.1-1.3.1-2.1 1C1.5 
                4.5 1.3 6.2 1.3 6.2S1 8.3 1 10.5v1.9c0 2.2.3 4.3.3 4.3s.2 1.7.8 2.4c.8.9 1.9.9 2.4 
                1C7 20 12 20 12 20s5.4 0 8.6-.3c.4-.1 1.3-.1 2.1-1 .6-.7.8-2.4.8-2.4s.3-2.1.3-4.3v-1.9c0-2.2-.3-4.3-.3-4.3zM9.8 15.3V8.7l6.4 
                3.3-6.4 3.3z" fill="white"/>
            </svg>
            <span>YouTube</span>
        </button>
    </a>
    """)

with col_btn3:
    # Botão do GitHub
    st.html("""
    <a href='https://github.com/PortalDosDados' target='_blank' style='text-decoration: none;'>
        <button class="btn-github">
            <svg viewBox="0 0 24 24" width="24" height="24">
                <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" fill="white"/>
            </svg>
            <span>GitHub</span>
        </button>
    </a>
    """)
