import streamlit as st
from auth import authenticate

sidebar_logo = "images/paylert.png"
st.logo(sidebar_logo)

# Autenticación
authenticate()