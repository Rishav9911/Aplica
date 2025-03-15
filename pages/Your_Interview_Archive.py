import streamlit as st
from pymongo import MongoClient
import pandas as pd
import urllib.parse
import pymongo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_NAME = os.getenv("QUESTIONS_DB")
ANSWERS= os.getenv("ANSWERS")
username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))
MONGO_URI = f"mongodb+srv://{username}:{password}@aplica.cozta.mongodb.net/?retryWrites=true&w=majority"

# MongoDB Connection
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
answers_collection = db[ANSWERS]

# Redirect if not authenticated
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("You must be logged in to access this page!")
    st.stop()

user_email = st.session_state.email  # Email of the logged-in user

st.title("📂 Your Past Mock Interview Responses")
st.write("Here are all the mock interview responses you've submitted:")

# Fetch interview responses for the logged-in user
user_responses = list(answers_collection.find({"email": user_email}))

if not user_responses:
    st.info("ℹ️ No interview responses found. Try answering a question first!")
    st.stop()

# Convert to DataFrame for better display
df = pd.DataFrame(user_responses, columns=["question", "transcription", "analysis"])

# Drop MongoDB ObjectId for cleaner display
df = df.drop(columns=["_id"], errors="ignore")  # "errors='ignore'" prevents KeyError

# Display table
st.dataframe(df, hide_index=True)

# Expandable Sections for Detailed View
for response in user_responses:
    with st.expander(f"📝 {response['question']}"):
        st.write(f"**Your Answer:**\n{response['transcription']}")
        st.write(f"**AI Analysis & Feedback:**\n{response['analysis']}")

# "Practice More" Button
st.markdown("---")
if st.button("🚀 Practice More"):
    st.switch_page("pages/Mock_Interview_Preparation.py")

st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False, "email": None, "full_name": None}))
