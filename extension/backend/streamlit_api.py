import streamlit as st
from pymongo import MongoClient
import requests
import json
import urllib.parse
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
# Load environment variables
load_dotenv()

# MongoDB connection details
username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))

MONGO_URI = "mongodb+srv://{}:{}@aplica.cozta.mongodb.net/?retryWrites=true&w=majority".format(username, password)

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client["user-info"] 
collection = db["user-main-details"] 

st.title("Your Student Profile")

email = st.text_input("Enter Student Email:")
if st.button("Fetch Student Data"):
    api_url = f"http://localhost:5001/get_student_data?email={email}"
    response = requests.get(api_url)

    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Student not found or API error.")
