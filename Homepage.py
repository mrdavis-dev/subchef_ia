import os
import streamlit as st
from streamlit_tags import st_tags
from db import get_db_connection
from auth import authenticate_user, create_user
import google.generativeai as genai

# Configurar la API de Google Generative AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-1.5-flash')

sidebar_logo = "images/subchef.png"
st.logo(sidebar_logo)

def login():
    st.title("Login")

    username = st.text_input("Email")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("Login successful")
            st.session_state.authenticated = True
            st.session_state.username = username
            # Recargar la aplicación para mostrar el contenido principal
            st.experimental_rerun()
        else:
            st.error("Username or password is incorrect")

def signup():
    st.title("Sign Up")

    username = st.text_input("Choose a Email")
    password = st.text_input("Choose a Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')
    
    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match")
        else:
            if create_user(username, password):
                st.success("User created successfully")
            else:
                st.error("Username already exists")

def logout():
    st.session_state.authenticated = False
    st.session_state.username = ''

def save_receta(doc_receta, recetas_collection):
    if doc_receta:
        recetas_collection.insert_one(doc_receta)
        st.success("Receta guardada exitosamente")
    else:
        st.error("Por favor, ingrese un ingrediente y su cantidad")

def main():
    # Inicializar variables de sesión si no existen
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = ''

    st.button("Logout", on_click=logout)
    
    # Encabezado que se muestra siempre
    st.title("🤖 SubChef IA")
    st.subheader("Crea recetas utilizando los ingredientes disponibles en tu despensa.")
    st.text("version beta ⌛")

    if st.session_state.authenticated:
        st.success(f"¡Bienvenido {st.session_state.username}!")

        # Conexión a la base de datos
        db = get_db_connection()
        recetas_collection = db['recetas']

        tipo_receta = st.selectbox(
            "Selecciona el tipo de receta:",
            ("Fitness", "Postres", "Desayuno", "Almuerzo", "Cena", "Meriendas")
        )

        st.write("Ingrese los ingredientes disponibles :red[(presione Enter para agregar cada ingrediente)]:")
        # Utilizando streamlit-tags para manejar los ingredientes como etiquetas
        ingredientes = st_tags(
            label='',
            text='',
            value=[],
            suggestions=[],
            maxtags=100,
            key='1'
        )

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
                
                recetas = prompt.text.split('____')  # Divide el texto en partes por "____"
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
                            'user': st.session_state.username,
                            'titulo': titulo,
                            'cuerpo': cuerpo,
                            'tipo': tipo_receta,
                            'ingredientes': ", ".join(ingredientes)
                        }
                        save_receta(receta_documento, recetas_collection)


    else:
        choice = st.radio("", ["Iniciar sesión", "Registrarse"], index=0, horizontal=True)
        if choice == "Iniciar sesión":
            login()
        elif choice == "Registrarse":
            signup()

        if not st.session_state.authenticated:
            st.warning("Por favor, inicia sesión para continuar.")

if __name__ == '__main__':
    main()
