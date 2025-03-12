import streamlit as st
from pymongo import MongoClient
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()


DB_NAME = os.getenv("DB")  
C2=os.getenv("C2")

username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))

MONGO_URI = f"mongodb+srv://{username}:{password}@aplica.cozta.mongodb.net/?retryWrites=true&w=majority"

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
profiles_collection = db[C2] 


# Redirect if not authenticated
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("You must be logged in to access this page!")
    st.stop()

st.title(f"Welcome, {st.session_state.full_name}! Your Profile Overview")

# Fetch user profile
user_profile = profiles_collection.find_one({"email": st.session_state.email})

if user_profile:
    # --- Personal Details ---
    st.header("📌 Personal Details")
    st.write(f"**Full Name:** {user_profile.get('full_name', 'N/A')}")
    st.write(f"**Email:** {user_profile.get('email', 'N/A')}")
    st.write(f"**Phone:** {user_profile.get('phone', 'N/A')}")
    st.write(f"**Location:** {user_profile.get('location', 'N/A')}")
    st.write(f"**LinkedIn:** [{user_profile.get('linkedin', 'N/A')}]({user_profile.get('linkedin', '#')})")
    st.write(f"**GitHub:** [{user_profile.get('github', 'N/A')}]({user_profile.get('github', '#')})")
    st.write(f"**Portfolio:** [{user_profile.get('portfolio', 'N/A')}]({user_profile.get('portfolio', '#')})")

    # --- Education ---
    st.header("🎓 Education")
    st.write(f"**Degree:** {user_profile.get('highest_degree', 'N/A')}")
    st.write(f"**University:** {user_profile.get('university', 'N/A')}")
    st.write(f"**Field of Study:** {user_profile.get('field_of_study', 'N/A')}")
    st.write(f"**Graduation Year:** {user_profile.get('graduation_year', 'N/A')}")
    st.write(f"**CGPA:** {user_profile.get('cgpa', 'N/A')}")
    st.write(f"**Certifications:** {', '.join(user_profile.get('certifications', []))}")

    # --- Work Experience ---
    if user_profile.get("work_experience"):
        st.header("💼 Work Experience")
        for idx, job in enumerate(user_profile["work_experience"], 1):
            with st.expander(f"📝 Job {idx}: {job['title']} at {job['company']}"):
                st.write(f"**Company:** {job['company']}")
                st.write(f"**Job Title:** {job['title']}")
                st.write(f"**Duration:** {job['duration']}")
                st.write(f"**Responsibilities:** {job['responsibilities']}")
                st.write(f"**Achievements:** {job['achievements']}")

    # --- Skills ---
    st.header("🔧 Skills")
    st.write(f"**Technical Skills:** {', '.join(user_profile.get('technical_skills', []))}")
    st.write(f"**Soft Skills:** {', '.join(user_profile.get('soft_skills', []))}")

    # --- Projects ---
    if user_profile.get("projects"):
        st.header("🚀 Projects")
        for idx, project in enumerate(user_profile["projects"], 1):
            with st.expander(f"📂 Project {idx}: {project['title']}"):
                st.write(f"**Description:** {project['description']}")
                st.write(f"**Technologies Used:** {project['technologies']}")
                st.write(f"**GitHub/Portfolio:** [{project['github']}]({project['github']})")

    # --- Internships & Training ---
    if user_profile.get("internships"):
        st.header("📚 Internships & Training")
        for idx, intern in enumerate(user_profile["internships"], 1):
            with st.expander(f"🏢 Internship {idx}: {intern['role']} at {intern['company']}"):
                st.write(f"**Company:** {intern['company']}")
                st.write(f"**Role:** {intern['role']}")
                st.write(f"**Duration:** {intern['duration']}")
                st.write(f"**Key Learnings:** {intern['responsibilities']}")

    # --- Resume Download ---
    if user_profile.get("resume"):
        st.header("📄 Resume")
        st.download_button("Download Resume", user_profile["resume"], file_name="resume.pdf")
else:
    st.warning("Profile not found. Please complete your profile.")

st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False, "email": None, "full_name": None}))
st.sidebar.write(f"Welcome, {st.session_state.full_name}!")
