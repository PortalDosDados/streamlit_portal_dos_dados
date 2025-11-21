import streamlit as st


def load_css(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")


# Configures da página
st.set_page_config(
    page_title='Dione Nascimento',
    page_icon='assets/portal.png',
    layout='wide'
)

# Estilo para centralizar o conteúdo e melhorar layout
st.markdown("""
<style>
.main {
    max-width: 1100px;
    margin: 0 auto;
}

p {
    margin-bottom: 10px;
    line-height: 1.45;
}

ul {
    margin-top: 0;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)


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


# Botão do Link
st.markdown("""
<a href='https://www.linkedin.com/in/dione-nascimento-37287a233' target='_blank'>
    <button class="btn-linkedin">
        <svg viewBox="0 0 448 512">
            <path d="M100.28 448H7.4V148.9h92.88zm-46.44-338C24 110 0 85.77 0 56.54A56.52 56.52 0 0 1 53.83 0C82.65 0 106 23.31 
            106 52.13c0 29.23-23.35 53.57-52.16 53.57zM447.9 448h-92.68V302.4c0-34.7-.7-79.2-48.29-79.2-48.29 0-55.72 
            37.7-55.72 76.7V448h-92.78V148.9h89.08v40.8h1.3c12.4-23.5 42.68-48.3 87.88-48.3 
            94 0 111.28 61.9 111.28 142.3z"/>
        </svg>
        Conheça meu LinkedIn
    </button>
</a><p>
""", unsafe_allow_html=True)
