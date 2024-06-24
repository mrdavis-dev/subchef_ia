import os
import streamlit as st
from db import get_db_connection
import firebase_admin
from firebase_admin import auth, exceptions, credentials, initialize_app
import asyncio
from httpx_oauth.clients.google import GoogleOAuth2
import json

# Cargar credenciales desde variables de entorno
firebase_credentials = os.getenv('FIREBASE_CREDENTIALS')
if firebase_credentials:
    cred = credentials.Certificate(json.loads(firebase_credentials))
    try:
        firebase_admin.get_app()
    except ValueError:
        initialize_app(cred)
else:
    st.error("No se encontraron credenciales de Firebase en las variables de entorno.")

# Inicializar cliente Google OAuth2
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_url = os.getenv("redirect_uri")

client = GoogleOAuth2(client_id=client_id, client_secret=client_secret)

# Conexión a la base de datos
db = get_db_connection()
users_collection = db['users']

async def get_access_token(client: GoogleOAuth2, redirect_url: str, code: str):
    return await client.get_access_token(code, redirect_url)

async def get_email(client: GoogleOAuth2, token: str):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email

def get_logged_in_user_email():
    try:
        code = st.query_params.get('code')
        if code:
            token = asyncio.run(get_access_token(client, redirect_url, code))  # No es necesario indexar si solo hay un código

            if token:
                user_id, user_email = asyncio.run(get_email(client, token['access_token']))
                if user_email:
                    # Verificar si el usuario ya existe en Firebase
                    try:
                        user = auth.get_user_by_email(user_email)
                    except exceptions.FirebaseError:
                        user = auth.create_user(email=user_email)
                    
                    # Verificar si el usuario ya existe en MongoDB
                    if not users_collection.find_one({"email": user_email}):
                        users_collection.insert_one({"email": user_email})

                    st.session_state.email = user.email
                    # Forzar a Streamlit a recargar la aplicación
                    st.rerun()
                    return user.email
        return None
    except Exception as e:
        st.error(f"Error durante el inicio de sesión: {e}")
        return None

def show_login_button():
    authorization_url = asyncio.run(client.get_authorization_url(
        redirect_url,
        scope=["email", "profile"],
        extras_params={"access_type": "offline"},
    ))
    st.markdown(f'<a href="{authorization_url}" target="_self">Iniciar sesión</a>', unsafe_allow_html=True)
    get_logged_in_user_email()