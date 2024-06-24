import streamlit as st
from auth import get_logged_in_user_email, show_login_button
from db import get_db_connection

def main():
    sidebar_logo = "images/subchef.png"
    st.logo(sidebar_logo)

    st.title("Recetas")

    user_email = get_logged_in_user_email()
    if not user_email:
        st.warning("Por favor, inicia sesión para continuar.")
        show_login_button()
        st.stop()
    else:

        st.success(f"¡Bienvenido {user_email}!")
        st.write("Aquí puedes ver y gestionar tus recetas.")
        if st.button("Logout"):
            st.session_state.email = ''
            st.experimental_rerun()
        
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

if __name__ == "__main__":
    main()




