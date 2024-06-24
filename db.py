# db.py
import os
import streamlit as st
from pymongo import MongoClient

@st.cache_resource
def get_db_connection():
    uri = os.getenv('MONGO_URL')
    client = MongoClient(uri)
    db = client.get_database("test")
    return db
