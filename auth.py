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
google_auth = Google_auth(clientId=client_id, clientSecret=client_secret, redirect_uri=redirect_uri)

# Conexión a la base de datos
db = get_db_connection()
users_collection = db['users']

def authenticate():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login_status = google_auth.login()
        if login_status == "authenticated":
            st.session_state["authenticated"] = True
            st.session_state["email"] = google_auth.email
            email = st.session_state["email"]
            
            # Verificar si el usuario ya existe en la base de datos
            user = users_collection.find_one({"email": email})
            if user:
                st.write(f"Bienvenido, {email}!")
            else:
                # Guardar el nuevo usuario en la base de datos
                users_collection.insert_one({"email": email})
                st.write(f"¡Bienvenido, nuevo usuario! Su correo electrónico '{email}' ha sido registrado.")
        else:
            st.error("Autenticación fallida. Por favor, intenta nuevamente.")
            st.stop()
        

    else:
        email = st.session_state["email"]
        st.write(f"Bienvenido, {email}!")

# Llamar a la función de autenticación en el archivo principal
authenticate()