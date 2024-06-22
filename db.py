# db.py
import streamlit as st
from pymongo import MongoClient

@st.cache_resource
def get_db_connection():
    uri = st.secrets["mongo"]["uri"]
    client = MongoClient(uri)
    db = client.get_database("test")
    return db
