import streamlit as st
from pymongo import MongoClient
import requests
import json

# MongoDB Connection
MONGO_URI = "mongodb+srv://sachdevarishav449:Parishu449%40@aplica.cozta.mongodb.net/"
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
