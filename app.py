import streamlit as st
from pymongo import MongoClient
import bcrypt
import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables
load_dotenv()


DB_NAME = os.getenv("DB")  
C1=os.getenv("C1")

username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))

MONGO_URI = f"mongodb+srv://{username}:{password}@aplica.cozta.mongodb.net/?retryWrites=true&w=majority"

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db[C1]  

# Streamlit Session Management
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "email" not in st.session_state:
    st.session_state.email = None

# Password Hashing
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8') if isinstance(hashed, str) else hashed)

# Register New User
def register_user(email, password, full_name, role="user"):
    existing_user = users_collection.find_one({"email": email})
    if existing_user:
        return False  # Email already exists
    hashed_password = hash_password(password)
    users_collection.insert_one({
        "email": email,
        "password": hashed_password,
        "full_name": full_name,
        "role": role
    })
    st.session_state.authenticated = True
    st.session_state.email = email
    st.session_state.full_name = full_name
    st.switch_page("pages/profile_setup.py")
    return True

# Authenticate User
def authenticate_user(email, password):
    user = users_collection.find_one({"email": email})
    if user and check_password(password, user["password"]):
        st.session_state.authenticated = True
        st.session_state.user_role = user["role"]
        st.session_state.email = email
        st.session_state.full_name = user["full_name"]
        st.switch_page("pages/dashboard.py")  # Redirect to dashboard

        return True
    return False

# Logout
def logout():
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.email = None
    st.session_state.full_name = None

    st.rerun()

# UI Components
st.title("Aplica+ Authentication")

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

if menu == "Register":
    st.subheader("Register")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(email, password, full_name):
            st.success(f"Welcome, {full_name}! Redirecting to profile setup...")
        else:
            st.error("Email already exists. Try logging in.")

elif menu == "Login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(email, password):
            st.success(f"Welcome back, {st.session_state.full_name}! Redirecting to dashboard...")
        else:
            st.error("Invalid email or password.")

if st.session_state.authenticated:
    st.sidebar.button("Logout", on_click=logout)
