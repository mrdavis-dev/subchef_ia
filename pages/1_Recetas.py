import streamlit as st
from db import get_db_connection

def main():
    sidebar_logo = "images/subchef.png"
    st.logo(sidebar_logo)

    st.title("Recetas")

    user_email = st.session_state.username
    if not user_email:
        st.warning("Por favor, inicia sesión para continuar.")
        st.stop()
    else:
        st.success(f"¡Bienvenido {user_email}!")
        st.write("Aquí puedes ver y gestionar tus recetas.")
        
        if st.button("Logout"):
            st.session_state.username = ''  # Limpiar la sesión de usuario
            st.experimental_rerun()  # Recargar la aplicación para aplicar cambios
        
        db = get_db_connection()
        collection = db['recetas']

        st.title("📒 Recetas")
        st.subheader("Aquí puedes ver todas tus recetas guardadas")

        categoria = st.selectbox(
            "Selecciona una categoría:",
            ("Todas", "Fitness", "Postres", "Desayuno", "Almuerzo", "Cena", "Meriendas")
        )

        def find_recetas(tipo):
            if categoria == "Todas":
                recetas = collection.find({"user": user_email})
            else:
                recetas = collection.find({"tipo": categoria, "user": user_email})
            
            for receta in recetas:
                with st.expander(receta['titulo']):
                    st.write(f"**Tipo de receta:** {receta['tipo']}")
                    st.write(f"**Ingredientes:** {receta['ingredientes']}")
                    st.write(f"**Instrucciones:**\n{receta['cuerpo']}")

        if categoria:
            find_recetas(categoria)

if __name__ == "__main__":
    main()
