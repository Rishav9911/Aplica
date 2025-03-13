import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
from aiortc.contrib.media import MediaRecorder
import os
import time
import pymongo
import random
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_NAME = os.getenv("QUESTIONS_DB")
QUESTIONS_C = os.getenv("QUESTIONS_C")
username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))

MONGO_URI = f"mongodb+srv://{username}:{password}@aplica.cozta.mongodb.net/?retryWrites=true&w=majority"

# MongoDB Connection
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[QUESTIONS_C]
answers_collection = db["answers"]

# Function to get a random question
def get_random_question():
    questions = list(collection.find())  # Fetch all questions
    if questions:
        return random.choice(questions)['question']
    else:
        return "No questions available!"

st.title("🎙️ Mock Interview Recorder")

AUDIO_FILE = "record.wav"

# Ensure question persists across reruns
if "question" not in st.session_state:
    st.session_state.question = get_random_question()

st.subheader(f"📌 Interview Question: {st.session_state.question}")

# Function to create a MediaRecorder that saves audio to a file
def recorder_factory():
    return MediaRecorder(AUDIO_FILE)

# WebRTC Component
webrtc_ctx = webrtc_streamer(
    key="sendonly-audio",
    mode=WebRtcMode.SENDONLY,
    in_recorder_factory=recorder_factory,
    client_settings=ClientSettings(
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"audio": True, "video": False},
    ),
)

# Track recording status
if "recording" not in st.session_state:
    st.session_state.recording = False

# Update UI based on recording state
if webrtc_ctx.state.playing:
    st.session_state.recording = True
    st.markdown("🟢 **Recording in Progress... Speak Now!**")

# Stop Recording & Play Audio
if not webrtc_ctx.state.playing and st.session_state.recording:
    st.session_state.recording = False  # Reset state
    
    time.sleep(1)  # Ensure file is saved
    
    if os.path.exists(AUDIO_FILE):  # Check if recording exists
        st.audio(AUDIO_FILE, format="audio/wav")
        st.success("✅ Audio recorded successfully!")
        
        # Save recording to MongoDB
        #with open(AUDIO_FILE, "rb") as f:
         #   audio_bytes = f.read()
          #  answers_collection.insert_one({
           #     "question": st.session_state.question,
            #    "answer_audio": audio_bytes
            #})
        #st.success("✅ Response saved to database!")
    else:
        st.error("⚠️ No audio recorded! Please try again.")

# Button to get a new question
if st.button("🔄 Get New Question"):
    st.session_state.question = get_random_question()
    st.rerun()
