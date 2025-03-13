import streamlit as st
import random
import sounddevice as sd
import wavio
import tempfile
import time
import pymongo
from dotenv import load_dotenv
import os
import urllib.parse
import numpy as np

# Load environment variables
load_dotenv()

# MongoDB connection details
DB_NAME = os.getenv("QUESTIONS_DB")
QUESTIONS_C = os.getenv("QUESTIONS_C")
username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))

MONGO_URI = f"mongodb+srv://{username}:{password}@aplica.cozta.mongodb.net/?retryWrites=true&w=majority"

# MongoDB Connection
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[QUESTIONS_C]

# Function to get a random question from MongoDB
def get_random_question():
    questions = list(collection.find())  # Fetch all questions
    if questions:
        return random.choice(questions)
    else:
        return None

# Function to record audio
def record_audio():
    fs = 44100  # Sample rate
    st.write("🎤 **Recording started...** Speak now!")

    audio_data = []  # Store audio chunks
    start_time = time.time()  # Record the time when the recording starts

    # Record audio until stopped
    while st.session_state['recording']:
        # Record 1 second of audio at a time
        audio_chunk = sd.rec(int(fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait until the chunk is recorded
        audio_data.append(audio_chunk)

        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        st.session_state['elapsed_time'] = elapsed_time  # Store elapsed time in session_state
        st.write(f"⏱️ Recording Time: {int(elapsed_time)} seconds")

    # Combine the audio chunks into one array
    audio_data = np.concatenate(audio_data, axis=0)

    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        wavio.write(temp_wav.name, audio_data, fs, sampwidth=2)
        return temp_wav.name

# Streamlit UI
st.title("🎙️ Mock Interview Recorder")
st.write("Record your response to the interview question.")

# Fetch a random question from the database
random_question = get_random_question()

if random_question:
    question_text = random_question['question']
    question_id = str(random_question['_id'])  # Store the question's ObjectId for later reference
    st.write(f"📌 **Interview Question:** {question_text}")
else:
    st.error("No questions available in the database!")

# Initialize session state variables
if 'recording' not in st.session_state:
    st.session_state['recording'] = False

if 'audio_file' not in st.session_state:
    st.session_state['audio_file'] = None

if 'question_id' not in st.session_state:
    st.session_state['question_id'] = None

if 'start_time' not in st.session_state:
    st.session_state['start_time'] = None

if 'elapsed_time' not in st.session_state:
    st.session_state['elapsed_time'] = 0

# Set question ID in session state for tracking
st.session_state['question_id'] = question_id

# Timer to show elapsed recording time
if st.session_state['recording']:
    elapsed_time = st.session_state['elapsed_time']
    minutes, seconds = divmod(int(elapsed_time), 60)  # Convert to minutes and seconds
    st.write(f"⏱️ Recording Time: {minutes:02}:{seconds:02}")

# Debugging: Check session state
st.write(st.session_state)

# Start/Stop Recording Logic
if st.session_state['recording']:
    stop_button = st.button("⏸ Stop Recording")
    if stop_button:
        st.session_state['recording'] = False
        st.write("✅ Recording stopped. You can now upload and transcribe.")
        # As soon as recording stops, provide download option
        st.audio(st.session_state['audio_file'], format="audio/wav")
        st.download_button(
            label="Download Recording",
            data=open(st.session_state['audio_file'], "rb").read(),
            file_name="recorded_answer.wav",
            mime="audio/wav"
        )
        # Debugging: Check session state
        st.write(st.session_state)
else:
    start_button = st.button("🎙 Start Recording")
    if start_button:
        st.session_state['recording'] = True
        st.session_state['start_time'] = time.time()  # Set start time for recording
        st.session_state['audio_file'] = None  # Reset previous recordings
        st.write("✅ Recording started. Speak now!")
        # Record the audio (this will run in the background)
        st.session_state['audio_file'] = record_audio()  # Change duration as per your requirement

        # Debugging: Check session state
        st.write(st.session_state)

# Upload & Transcribe Button
if st.session_state['audio_file']:
    if st.button("⏫ Upload & Convert to Text"):
        st.success("🔄 Uploading & Converting Audio... Please wait.")

        # Simulate Upload (you would handle transcription here)
        with open(st.session_state['audio_file'], "rb") as audio_file:
            audio_data = audio_file.read()

        # Store the answer in the database along with the question id
        answers_collection = db["answers"]
        answer_doc = {
            "question_id": st.session_state['question_id'],
            "answer_audio": audio_data
        }
        answers_collection.insert_one(answer_doc)

        st.session_state['audio_uploaded'] = True
        st.write("✅ Audio uploaded and stored successfully!")

        # Debugging: Check session state
        st.write(st.session_state)
