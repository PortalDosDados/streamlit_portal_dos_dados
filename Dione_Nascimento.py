import streamlit as st

# Função para carregar CSS externo
def load_css(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Configurações da página
st.set_page_config(
    page_title='Dione Nascimento',
    page_icon='assets/portal.png',
    layout='wide'
)

# Carrega o CSS do arquivo style.css
load_css("style.css")

# Criação das colunas com proporção mais impactante
col1, col2 = st.columns([1.2, 3])

with col1:
    st.image('./assets/minha_foto.png', use_container_width=True)

with col2:
    st.markdown('''
<div style="text-align: justify; font-size: 17px;">
<p>Olá! Sou <b>Dione Nascimento</b>, profissional com <b>15 anos de experiência em Manutenção Industrial</b>, especializado em <b>Gestão de Ativos</b> e <b>Análise de Dados</b>. Minha atuação combina metodologias de manutenção com soluções de Business Intelligence para transformar dados operacionais em decisões rápidas e precisas.</p>

<p>Minha trajetória começou no SENAI, onde atuei como <b>jovem aprendiz</b> e depois como <b>professor</b>. Nos últimos 10 anos, venho trabalhando no <b>setor siderúrgico</b>, desenvolvendo projetos focados em:</p>

<ul>
<li>Confiabilidade de equipamentos</li>
<li>Digitalização da manutenção</li>
<li>Automação de análises e indicadores</li>
</ul>

<p>Converto dados de campo em inteligência aplicada, melhoro planos de manutenção e estruturo processos que elevam desempenho e reduzem custos.</p>

<p>Sou também o criador do <b>Portal dos Dados</b>, projeto que conecta <b>Engenharia</b> e <b>Ciência de Dados</b> para ajudar profissionais a tomar decisões orientadas por dados reais e aplicáveis ao dia a dia da manutenção.</p>
</div>
''', unsafe_allow_html=True)

# CTA mais destacado
st.markdown("""
<div style="margin-top: 20px; margin-bottom: 25px;">
    <a href='https://www.linkedin.com/in/dione-nascimento-37287a233' target='_blank'>
        <button style="
            background-color: #0A66C2;
            color: white;
            padding: 12px 22px;
            border: none;
            border-radius: 6px;
            font-size: 17px;
            cursor: pointer;
        ">
        Acessar meu LinkedIn
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

# Banner com largura total
st.image('./assets/fundo.jpg', use_container_width=True)
