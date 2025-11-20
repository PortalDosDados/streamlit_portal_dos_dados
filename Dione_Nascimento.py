import streamlit as st

# Configurações da página
st.set_page_config(
    page_title='Dione Nascimento',
    page_icon='assets/portal.png',
    layout='wide'
)


# Cria duas colunas
col1, col2 = st.columns([1, 2])  # Ajuste os números para proporção desejada

with col1:
    st.image('./assets/minha_foto.png', width=300)
with col2:
    st.image('./assets/fundo.jpg', width=300)

# Estilo global para parágrafos e listas
st.markdown('''
<style>
p {
    margin-bottom: 8px;
}
ul {
    margin-top: 0;
    margin-bottom: 8px;
}
</style>
''', unsafe_allow_html=True)

# Conteúdo "Sobre mim"
st.markdown('''
<div style="text-align: justify;">
<p>Olá! Sou <b>Dione Nascimento</b>, profissional com <b>15 anos de experiência em Manutenção Industrial</b>, especializado em <b>Gestão de Ativos</b> e <b>Análise de Dados</b>. Trabalho integrando metodologias de manutenção com soluções de Business Intelligence, transformando dados operacionais em informações estratégicas para decisões rápidas e precisas.</p>

<p>Minha trajetória começou no SENAI, onde atuei como <b>jovem aprendiz</b> e posteriormente como <b>professor</b>, nos últimos 10 anos venho atuando no <b>setor siderúrgico</b>, desenvolvendo projetos voltados à <b>confiabilidade de equipamentos</b>, <b>digitalização da manutenção</b> e <b>automação de análises</b>. 
<p>Converto dados de campo em indicadores, aprimoro planos de manutenção e estruturo processos que elevam desempenho e reduzem custos.</p>

<p>Fora do ambiente corporativo, gosto de <b>ler</b> e <b>programar</b>, dessa rotina nasceu o <b>Portal dos Dados</b>, meu projeto pessoal que conecta <b>Engenharia</b> e <b>Ciência de Dados</b>, ajudando profissionais a tomar decisões estratégicas baseadas em dados reais e aplicáveis ao dia a dia da manutenção.</p>

</div>
''', unsafe_allow_html=True)

st.markdown('''🔗[Clique aqui para saber mais](https://www.linkedin.com/in/dione-nascimento-37287a233)''')