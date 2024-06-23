# auth.py
import streamlit as st
from google_auth_st import add_auth
from db import get_db_connection


st.warning("Necesitas iniciar sesion")

db = get_db_connection()
users_collection = db['users']

def authenticate():

    add_auth()
    if 'email' not in st.session_state:
        st.error("Authentication failed")
        st.stop()
    else:
        user = users_collection.find_one({'email': st.session_state.email})
        if user:
            st.write(f"Bienvenido, {st.session_state.email}!")
        else:
            # Guardar el nuevo usuario en la base de datos
            users_collection.insert_one({'email': st.session_state.email})
            st.write(f"¡Bienvenido, nuevo usuario! Su correo electrónico '{st.session_state.email}' ha sido registrado.")



