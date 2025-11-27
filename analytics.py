# Arquivo: analytics.py
import streamlit as st
import streamlit.components.v1 as components

def inject_ga(measurement_id):
    """
    Injeta o script de rastreamento do Google Analytics 4 (GA4).
    """
    if not measurement_id:
        return

    # Código Javascript padrão do GA4
    ga_code = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());

        gtag('config', '{measurement_id}', {{
            'cookie_flags': 'SameSite=None;Secure'
        }});
    </script>
    """
    
    # Injeta o HTML invisível no app
    # O height=0 garante que não ocupe espaço visual na tela
    components.html(ga_code, height=0, width=0)