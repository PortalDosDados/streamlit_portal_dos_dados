import streamlit as st

st.title("Contato")

st.write("""
Se quiser trocar ideias sobre engenharia, dados e automação, entre em contato.
""")

with st.form("contact_form"):
    nome = st.text_input("Nome")
    email = st.text_input("E-mail")
    mensagem = st.text_area("Mensagem")

    enviado = st.form_submit_button("Enviar")

    if enviado:
        st.success(f"Mensagem enviada com sucesso, {nome}! Entrarei em contato em breve.")
