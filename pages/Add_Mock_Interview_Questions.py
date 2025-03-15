import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import urllib.parse

# Load environment variables
load_dotenv()

# MongoDB connection details
DB_NAME = os.getenv("QUESTIONS_DB")  
QUESTIONS_C = os.getenv("QUESTIONS_C")
username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))

MONGO_URI = "mongodb+srv://{}:{}@aplica.cozta.mongodb.net/?retryWrites=true&w=majority".format(username, password)

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[QUESTIONS_C] 

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("You must be logged in to access this page!")
    st.stop()

# Streamlit App
st.title("Interview Question Manager")
st.subheader("Add a Custom Interview Question(only one)")

# User input for question
question = st.text_area("Enter your custom interview question:")

if st.button("Submit"):
    if question.strip():
        collection.insert_one({"question": question})
        st.success("Question added successfully!")
        st.rerun()
    else:
        st.warning("Please enter a question before submitting.")

st.subheader("Interview Questions")
questions = collection.find()
for q in questions:
    st.write(f"- {q['question']}")

st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False, "email": None, "full_name": None}))
