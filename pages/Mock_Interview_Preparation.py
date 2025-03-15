import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
from aiortc.contrib.media import MediaRecorder
import os
import time
import pymongo
import torch
import random
import urllib.parse
import ollama
from dotenv import load_dotenv
from transformers import pipeline

# Load environment variables
load_dotenv()

DB_NAME = os.getenv("QUESTIONS_DB")
QUESTIONS_C = os.getenv("QUESTIONS_C")
ANSWERS= os.getenv("ANSWERS")
username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))
MONGO_URI = f"mongodb+srv://{username}:{password}@aplica.cozta.mongodb.net/?retryWrites=true&w=majority"

# MongoDB Connection
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[QUESTIONS_C]
answers_collection = db[ANSWERS]

# Redirect if not authenticated
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("You must be logged in to access this page!")
    st.stop()

user_email = st.session_state.email


# Load Whisper model
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v2", device=0 if torch.cuda.is_available() else -1)

# Function to get a random question
def get_random_question():
    questions = list(collection.find())  
    return random.choice(questions)['question'] if questions else "No questions available!"

# Streamlit UI
st.title("🎙️ AI-Powered Mock Interview")

# Ensure question persists across reruns
if "question" not in st.session_state:
    st.session_state.question = get_random_question()

st.subheader(f"📌 Interview Question: {st.session_state.question}")

AUDIO_FILE = "record.wav"

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

if webrtc_ctx.state.playing:
    st.session_state.recording = True
    st.markdown("🟢 **Recording in Progress... Speak Now!**")

# Stop Recording & Play Audio
if not webrtc_ctx.state.playing and st.session_state.recording:
    st.session_state.recording = False  
    time.sleep(1)  

    if os.path.exists(AUDIO_FILE):  
        st.audio(AUDIO_FILE, format="audio/wav")
        st.success("✅ Audio recorded successfully!")
        st.session_state.audio_ready = True  

    else:
        st.error("⚠️ No audio recorded! Please try again.")

# Transcription and Analysis
if "audio_ready" in st.session_state and st.session_state.audio_ready:
    if st.button("📝 Transcribe & Analyze Answer"):
        st.write("⏳ Processing audio...")

        # Transcribe with Whisper
        result = pipe(AUDIO_FILE, return_timestamps=True)
        transcribed_text = result['text']

        st.write("📝 **Transcription:**")
        st.info(transcribed_text)  

        st.write("⏳ Processing feedback...")


        # Call LLaMA-2 for analysis
        prompt = f"""
        You are an expert interview coach. Your task is to analyze the user's interview answer based on clarity, confidence, structure, and relevance.
        Provide constructive feedback and suggest improvements if necessary.

        **Interview Question:** {st.session_state.question}

        **User's Answer:** {transcribed_text}

        **Evaluation:**
        1. Strengths of the response
        2. Areas for improvement
        3. How well does this answer fit an interview scenario?
        4. Suggested improvements to make the answer stronger

        **Your feedback:**
        """
        response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": prompt}])
        analysis = response["message"]

        st.write("📊 **AI Feedback:**")

        # Extract text from the message object
        if hasattr(analysis, 'content'):
            analysis_text = analysis.content  # Extract the actual text
        else:
            analysis_text = str(analysis)  # Convert to string if necessary

        formatted_analysis = analysis_text.replace("\n", "\n\n")  # Adds spacing between points
        st.markdown(f"```\n{formatted_analysis}\n```")  # Displays it as a structured markdown block



        # Save everything to MongoDB
        if user_email:
           answers_collection.insert_one({
               "email": user_email,
               "question": st.session_state.question,
               "transcription": transcribed_text,
               "analysis": formatted_analysis,
            })
        st.success("✅ Response saved to database!")

# Get a new question
if st.button("🔄 Get New Question"):
    st.session_state.question = get_random_question()
    st.rerun()

