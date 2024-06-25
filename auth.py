import bcrypt
from db import get_db_connection

def generate_password_hash(password):
    # Genera un hash de contraseña usando bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def check_password_hash(hashed_password, password):
    # Verifica si la contraseña sin cifrar coincide con el hash almacenado
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

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
    hashed_password = generate_password_hash(password)
    user_collection.insert_one({'username': username, 'password': hashed_password})
    return True

def change_password(username, current_password, new_password):
    db = get_db_connection()
    user_collection = db['users']
    user = user_collection.find_one({'username': username})
    
    if user and check_password_hash(user['password'], current_password):
        hashed_new_password = generate_password_hash(new_password)
        user_collection.update_one({'username': username}, {'$set': {'password': hashed_new_password}})
        return True
    return False

def delete_user(username):
    db = get_db_connection()
    user_collection = db['users']
    result = user_collection.delete_one({'username': username})
    return result.deleted_count > 0  # Devuelve True si se eliminó algún usuario
