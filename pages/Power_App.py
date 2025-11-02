import streamlit as st

# Configurações da página
st.set_page_config(
    page_title='Power Apps',       # Título da aba
    page_icon='assets/power_apps.png',   # Ícone da aba (pode ser .ico, .png ou emoji)
    layout='wide'                        # Layout da página (opcional)
)

st.title('📱 Power Apps')

st.markdown('''
Com o **Power Apps**, é possível criar aplicativos corporativos de forma rápida, intuitiva e sem necessidade de programação avançada.
''')

st.subheader('Exemplos de apps')
st.markdown('''
- Checklist de manutenção  
- Cadastro de equipamentos  
- Automação de processos internos
''')

st.subheader('Templates e automações')
st.markdown('''
Modelos prontos para agilizar processos repetitivos.
''')

st.subheader('Integrações')
st.markdown('''
SharePoint, Excel, Dataverse e outras plataformas para potencializar seu fluxo de trabalho.
''')

st.markdown('**Quando não se agrega valor, se agrega custo.**')
