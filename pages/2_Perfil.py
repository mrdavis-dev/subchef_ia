import streamlit as st
from auth import get_logged_in_user_email, show_login_button

sidebar_logo = "images/subchef.png"
st.logo(sidebar_logo)

st.subheader("En proceso...")
