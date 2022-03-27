from pymongo import MongoClient
from bson.objectid import ObjectId

from .exceptions import IntegrityError, ObjectDoesNotFound
from backend import password_manager


CILENT = MongoClient('localhost', 27017)
DB = CILENT['password_manager']
USERS_COLLECTION = DB['users']
PASSWORD_COLLECTION = DB['passwords']


def get_user_by_data(user_data):
    query = {"$or": [{"username": user_data["username"]}, {"email": user_data["email"]}]}
    return USERS_COLLECTION.find_one(query)


def get_user_if_exist(user_data):
    user = get_user_by_data(user_data)
    if not user:
        raise ObjectDoesNotFound("User with passed username or email dosen't exist")

    return user


def get_user_by_id(_id):
    user = USERS_COLLECTION.find_one({"_id": _id})
    if not user:
        raise ObjectDoesNotFound("User with passed ID dosen't exist")
    
    return user


def register_user(user_data):
    if not user_data['username'] or not user_data['email']:
        raise IntegrityError("Username and email may not be empty")

    user_data['salt'] = password_manager.generate_salt()

    if get_user_by_data(user_data):
        raise IntegrityError("User with passed username or email already exists")

    new_inserted_id = USERS_COLLECTION.insert_one(user_data).inserted_id
    
    return ObjectId(new_inserted_id)


def add_new_password(master_password, user, password_data):
    if not password_data["app_name"] or not password_data["password"]:
        raise IntegrityError("App name and password are required")
    
    query = get_query_object(user, password_data["app_name"])
    if PASSWORD_COLLECTION.find_one(query):
        raise IntegrityError("This app have already password for this user")

    secret_key = password_manager.generate_secret_key(
        password_provided=master_password, 
        salt_provided=user['salt']
    )
    password_hashed = password_manager.encrypt_password(password_data['password'], key=secret_key)
    
    password_data['user_id'] = user['_id']
    password_data['password'] = password_hashed

    PASSWORD_COLLECTION.insert_one(password_data)


def get_query_object(user, app_name):
    return {"user_id": user['_id'], "app_name": app_name }


def get_password(user_salt, password_encrypted, master_password):
    secret_key = password_manager.generate_secret_key(
        password_provided=master_password, 
        salt_provided=user_salt
    )
    password_decrypted = password_manager.decrypt_password(password_encrypted, key=secret_key)

    return password_decrypted


def update_password_data(_id, user_salt, master_password, old_password, password_data):
    if not password_data:
        raise IntegrityError("No data was changed")
    
    secret_key = password_manager.generate_secret_key(master_password, user_salt)
    if not password_manager.valid_secret_key(secret_key, old_password):
        raise IntegrityError("Invalid master password for this app")

    if 'password' in password_data:
        password_data['password'] = password_manager.encrypt_password(password_data['password'], key=secret_key)
    
    return PASSWORD_COLLECTION.update_one({"_id": _id}, {"$set": password_data})


def delete_password_data(_id):
    PASSWORD_COLLECTION.delete_one({"_id" : _id})


def get_user_passwords(user_id, query_data):
    query = {"user_id": user_id, **query_data}
    data = PASSWORD_COLLECTION.find(query)

    return data