import streamlit as st
from db import get_db_connection
from auth import change_password, delete_user

def main():
    sidebar_logo = "images/subchef.png"
    st.logo(sidebar_logo)

    st.title("Perfil de Usuario")

    user_email = st.session_state.username
    if not user_email:
        st.warning("Por favor, inicia sesión para ver tu perfil.")
        st.stop()

    st.success(f"¡Bienvenido {user_email}!")

    db = get_db_connection()
    users_collection = db['users']

    user_data = users_collection.find_one({"username": user_email})

    if not user_data:
        st.error("No se encontraron datos de usuario. Por favor, inicia sesión nuevamente.")
        st.stop()

    st.write(f"**Usuario:** {user_data['username']}")
    st.write(f"**Email:** {user_data['email']}")

    st.subheader("Editar Contraseña")
    current_password = st.text_input("Contraseña actual:", type="password")
    new_password = st.text_input("Nueva contraseña:", type="password")
    confirm_new_password = st.text_input("Confirmar nueva contraseña:", type="password")

    if st.button("Guardar Cambios de Contraseña"):
        if new_password != confirm_new_password:
            st.error("Las contraseñas nuevas no coinciden.")
        elif change_password(user_email, current_password, new_password):
            st.success("Contraseña actualizada exitosamente.")
        else:
            st.error("Error al actualizar la contraseña. Verifica la contraseña actual.")

    st.subheader("Eliminar Cuenta")
    delete_confirmation = st.checkbox("Confirmar que deseas eliminar tu cuenta")

    if delete_confirmation and st.button("Eliminar Cuenta", key="delete_account"):
        if st.confirm("¿Estás seguro que deseas eliminar tu cuenta? Esta acción no se puede deshacer."):
            if delete_user(user_email):
                st.success("Cuenta eliminada exitosamente.")
                st.session_state.username = ''  # Limpiar la sesión de usuario después de eliminar la cuenta
            else:
                st.error("Error al intentar eliminar la cuenta.")

if __name__ == "__main__":
    main()
