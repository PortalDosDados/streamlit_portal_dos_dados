import streamlit as st

# Configurações da página
st.set_page_config(
    page_title='Dione Nascimento',
    page_icon='assets/portal.png',
    layout='wide'
)



# Cria duas colunas: uma para a imagem e outra para o texto
col1, col2 = st.columns([1, 2])  # Ajuste os números para proporção desejada


st.image('./assets/minha_foto.png', width=300)


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

<p>Olá! Sou <b>Dione Nascimento</b>, profissional com <b>15 anos de experiência em Manutenção Industrial</b>, com foco em <b>Confiabilidade Mecânica e Análise de Dados</b>. Atuo aplicando metodologias de manutenção integradas a soluções de Business Intelligence, transformando dados em informações estratégicas para apoiar a tomada de decisão.</p>

<p>Minha trajetória começou no SENAI, onde fui <b>jovem aprendiz e professor</b>, essas experiências me ensinaram disciplina, prática e o valor de compartilhar conhecimento de forma objetiva.</p>

<p>Nos últimos 10 anos, atuei no <b>ramo siderúrgico</b>, desenvolvendo projetos que combinam <b>confiabilidade de equipamentos, digitalização da manutenção e análise de dados</b>. Transformo informações de campo em indicadores estratégicos, automatizo relatórios e otimizo planos de manutenção, sempre com foco em resultados concretos.</p>

<p>Fora do trabalho, gosto de <b>ler e programar</b>, foi dessa rotina que nasceu meu projeto pessoal, o <b>Portal dos Dados</b>, que conecta <b>Engenharia</b> e <b>Ciência de Dados</b>, ajudando profissionais a tomar decisões estratégicas usando dados de verdade.</p>

</div>
''', unsafe_allow_html=True)

st.markdown('''🔗[Clique aqui para saber mais](https://www.linkedin.com/in/dione-nascimento-37287a233)''')