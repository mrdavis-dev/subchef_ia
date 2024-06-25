import os
import streamlit as st
from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

def authenticate_user(username, password):
    db = get_db_connection()
    user_collection = db['users']
    user = user_collection.find_one({'username': username})
    
    if user and check_password_hash(user['password'], password):
        return True
    return False

def create_user(username, password):
    db = get_db_connection()
    user_collection = db['users']
    if user_collection.find_one({'username': username}):
        return False
    hashed_password = generate_password_hash(password, method='sha256')
    user_collection.insert_one({'username': username, 'password': hashed_password})
    return True