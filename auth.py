# auth.py
import streamlit as st
from google_auth_st import add_auth

st.warning("Necesitas iniciar sesion")
def authenticate():

    add_auth()
    if 'email' not in st.session_state:
        st.error("Authentication failed")
        st.stop()
    else:
        st.write(f"Welcome, {st.session_state.email}")
