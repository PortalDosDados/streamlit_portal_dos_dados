import streamlit as st


# Foto no topo
st.image("../streamlit_portal_dos_dados/assets/minha_foto.png", width=200)

# Configurações da página
st.set_page_config(
    page_title="Dione Nascimento",       # Título da aba
    page_icon="assets/portal.png",   # Ícone da aba (pode ser .ico, .png ou emoji)
    layout="wide"                        # Layout da página (opcional)
)

# Página Sobre no estilo direto, sem mencionar paixão
st.markdown('''
Olá! Sou **Dione Nascimento**, profissional com **15 anos de experiência em Manutenção Industrial**.  

Durante esse tempo, atuei como **professor no SENAI**, experiências que marcou minha trajetória e reforçou meu compromisso com aprendizado e compartilhamento de conhecimento.  

Nos últimos 10 anos, atuo no **ramo siderúrgico**, desenvolvendo projetos de **confiabilidade mecânica** e aplicando metodologias de manutenção para gerar resultados reais.  

No meu tempo livre, gosto de **ler e programar**, atividades que me levaram a criar meu projeto pessoal, o **Portal dos Dados**, integrando Engenharia e Ciência de Dados para capacitar profissionais a usar informações de forma estratégica.
''')
# Foto no topo
st.image('../streamlit_portal_dos_dados/assets/fundo.jpg', width=1000)