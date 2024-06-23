import streamlit as st
from auth import authenticate
from db import get_db_connection


sidebar_logo = "images/subchef.png"
st.logo(sidebar_logo)
# Autenticación
authenticate()

db = get_db_connection()
collection = db['recetas']

st.title("📒 Recetas")
st.subheader("Aqui podras ver todas tus recetas guardadas")

categoria = st.selectbox(
    "Selecciona una categoria:",
    ("Todas", "Fitnes", "Postres", "Desayuno", "Almuerzo", "Cena", "Meriendas")
)

def find_recetas(tipo):
    if categoria == "Todas":
        recetas = collection.find({"user": st.session_state.email})
    else:
        recetas = collection.find({"tipo": categoria, "user": st.session_state.email})
    
    for receta in recetas:
        with st.expander(receta['titulo']):
            st.write(f"**Tipo de receta:** {receta['tipo']}")
            st.write(f"**Ingredientes:** {receta['ingredientes']}")
            st.write(f"**Instrucciones:**\n{receta['cuerpo']}")

if categoria:
    find_recetas(categoria)
