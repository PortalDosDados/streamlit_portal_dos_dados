import streamlit as st
import streamlit.components.v1 as components

def inject_analytics():
    # Tenta pegar a chave, se não tiver, não faz nada
    if "GOOGLE_ANALYTICS_ID" not in st.secrets:
        return

    ga_id = st.secrets["GOOGLE_ANALYTICS_ID"]
    
    ga_code = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{ga_id}', {{ 'cookie_flags': 'SameSite=None;Secure' }});
    </script>
    """
    components.html(ga_code, height=0, width=0)