import streamlit as st

def load_css():
    st.markdown("""
        <style>
        body {
            background-color: #F8F9FA;
        }
        h1, h2, h3 {
            color: #1A5276;
        }
        .stButton button {
            background-color: #1A5276;
            color: white;
            border-radius: 10px;
            padding: 0.5em 1em;
        }
        .stButton button:hover {
            background-color: #154360;
        }
        </style>
    """, unsafe_allow_html=True)
