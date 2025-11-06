import streamlit as st

# Configurações da página
st.set_page_config(
    page_title='Dione Nascimento - Power Apps',       # Título da aba
    page_icon='assets/power_apps.png',   # Ícone da aba (pode ser .ico, .png ou emoji)
    layout='wide'                        # Layout da página (opcional)
)

st.image('assets/power_apps.png', width= 160)
st.header('Power Apps')
st.markdown('''
Com o **Power Apps**, é possível criar aplicativos corporativos de forma rápida, intuitiva e sem necessidade de programação avançada.
''')

# Criando três colunas para as imagens
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image('./assets/app_ferr_01.jpeg', width=700)

with col2:
    st.image('./assets/app_ferr_02.jpeg', width=700)

with col3:
    st.image('./assets/app_ferr_03.jpeg', width=700)

with col4:
    st.image('./assets/app_ferr_04.jpeg', width=700)