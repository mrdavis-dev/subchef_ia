import os
import streamlit as st
from streamlit_tags import st_tags
from auth import authenticate
from db import get_db_connection
import google.generativeai as genai

genai.configure(api_key = st.secrets["gemini"]["api_key"])

model = genai.GenerativeModel('gemini-1.5-flash')


sidebar_logo = "images/subchef.png"
st.logo(sidebar_logo)

client_id = os.getenv('CLIENT_ID')
st.write(f"Client ID: {client_id}")

authenticate()
# Conexión a la base de datos
db = get_db_connection()
recetas_collection = db['recetas']


st.title("🤖 SubChef IA")
st.subheader("Crea recetas utilizando los ingredientes disponibles en tu despensa.")

tipo_receta = st.selectbox(
    "Selecciona el tipo de receta:",
    ("Fitnes", "Postres", "Desayuno", "Almuerzo", "Cena", "Meriendas"))

st.write("Ingrese los ingredientes disponibles (presione Enter para agregar cada ingrediente):")
# Utilizando streamlit-tags para manejar los ingredientes como etiquetas
ingredientes = st_tags(
    label='',
    text='',
    value=[],
    suggestions=[],
    maxtags=100,
    key='1'
)

def save_receta(doc_receta):
    if doc_receta:
        recetas_collection.insert_one(doc_receta)
        st.success("Receta guardada exitosamente")
    else:
        st.error("Por favor, ingrese un ingrediente y su cantidad")

 # Definir y asignar correctamente los ingredientes

if 'recetas_generadas' not in st.session_state:
    st.session_state.recetas_generadas = []

if st.button("Generar Receta", key=f"crear"):
    if ingredientes:
        ingredientes_texto = ", ".join(ingredientes)
        instruccion = f"""
        Tengo los siguientes ingredientes: {ingredientes_texto}. Por favor, genera tres recetas realistas utilizando algunos de estos ingredientes. 
        Cada receta debe incluir un título, una lista de ingredientes (solo de los mencionados) y pasos detallados de preparación. 
        El tipo de receta que busco es {tipo_receta}. 
        Asegúrate de que las recetas sean factibles y prácticas de preparar. separa cada opción con una línea "____".
        """
        # Llamar a la API de generación de contenido
        prompt = model.generate_content(instruccion)
        
        recetas = prompt.text.split('____')  # Divide el texto en partes por "Receta"
        st.session_state.recetas_generadas = []  # Lista para almacenar las recetas generadas
        
        # Filtra recetas vacías y procesa cada receta
        for i, receta in enumerate(recetas, 1):
            receta = receta.strip()
            if receta:
                # Extrae el título (primera línea) y el cuerpo de la receta (resto)
                lines = receta.split('\n', 1)
                titulo = lines[0].strip()
                cuerpo = lines[1].strip() if len(lines) > 1 else ""

                # Guardar receta en la lista de recetas generadas
                st.session_state.recetas_generadas.append((titulo, cuerpo))
    
        if not st.session_state.recetas_generadas:
            st.error("No se han generado recetas con los ingredientes proporcionados.")
    
    else:
        st.error("No hay suficientes ingredientes para generar una receta.")

# Mostrar todas las recetas generadas de manera lineal
if st.session_state.recetas_generadas:
    for i, (titulo, cuerpo) in enumerate(st.session_state.recetas_generadas, 1):
        expander = st.expander(f"Receta {i}: {titulo}")
        with expander:
            st.write(cuerpo)
        
            # Botón para guardar la receta
            if st.button(f"Guardar Receta {i}", key=f"guardar_{i}_{titulo}"):
                receta_documento = {
                    'user': st.session_state.email,
                    'titulo': titulo,
                    'cuerpo': cuerpo,
                    'tipo': tipo_receta,
                    'ingredientes': ", ".join(ingredientes)  # Usa ingredientes_texto aquí
                }
                save_receta(receta_documento)