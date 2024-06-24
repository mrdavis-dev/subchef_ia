# auth.py
import os
import streamlit as st
from StreamlitGauth.google_auth import Google_auth
from db import get_db_connection

# Configurar las credenciales de Google OAuth
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = os.getenv("redirect_uri")

# Inicializar la autenticación de Google
login = Google_auth(clientId=client_id, clientSecret=client_secret, redirect_uri=redirect_uri)

db = get_db_connection()
users_collection = db['users']

def authenticate():
    if login == "authenticated":
            # Si el usuario está autenticado, obtener el email del estado de la sesión
            email = st.session_state.get('email')
            if email:
                user = users_collection.find_one({'email': email})
                if user:
                    st.write(f"Bienvenido, {email}!")
                else:
                    # Guardar el nuevo usuario en la base de datos
                    users_collection.insert_one({'email': email})
                    st.write(f"¡Bienvenido, nuevo usuario! Su correo electrónico '{email}' ha sido registrado.")
            else:
                st.error("Authentication failed")
                st.stop()
    else:
        st.warning("Necesitas iniciar sesión")

authenticate()



