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
        <div style="text-align: justify;">
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
