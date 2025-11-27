import streamlit as st
import streamlit.components.v1 as components

def inject_analytics():
    # Verifica se a chave existe nos segredos
    if "GOOGLE_ANALYTICS_ID" not in st.secrets:
        return

    ga_id = st.secrets["GOOGLE_ANALYTICS_ID"]
    
    # -----------------------------------------------------------
    # ATENÇÃO ÀS MUDANÇAS ABAIXO:
    # 1. Usei {ga_id} também no link do script para garantir consistência.
    # 2. Usei chaves duplas {{ }} para o Javascript não quebrar o Python.
    # 3. Coloquei aspas '{ga_id}' dentro do JS.
    # 4. Adicionei cookie_flags para funcionar no Streamlit Cloud.
    # -----------------------------------------------------------
    ga_code = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());

        gtag('config', '{ga_id}', {{
            'cookie_flags': 'SameSite=None;Secure'
        }});
    </script>
    """
    
    components.html(ga_code, height=0, width=0)