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

st.markdown("""
    <style>
        /* Center the main title */
        h1 {
            text-align: center;
            color: #ff6600;
            font-size: 32px;
            font-weight: bold;
        }

        /* Style section headers */
        h2 {
            color: #0077b6;
            border-bottom: 3px solid #0077b6;
            padding-bottom: 5px;
        }

        /* Sidebar Styling */
        .css-1d391kg {
            background-color: #f4f4f4 !important;
            border-right: 3px solid #ff6600;
        }

        /* Style Expander Sections */
        .st-expander {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }

        /* Style Sidebar Logout Button */
        div.stButton > button {
            background-color: #ff6600;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px;
            width: 100%;
        }

        div.stButton > button:hover {
            background-color: #cc5500;
        }

        /* Profile Section Styling */
        .profile-box {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }

        /* Download Resume Button */
        .stDownloadButton button {
            background-color: #0077b6;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px;
        }

        .stDownloadButton button:hover {
            background-color: #005f91;
        }

        /* Hide Streamlit Default Menu & Footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)



# Redirect if not authenticated
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("You must be logged in to access this page!")
    st.stop()

st.title(f"Welcome, {st.session_state.full_name}!")
st.title(f"Your Profile Overview")

# Fetch user profile
user_profile = profiles_collection.find_one({"email": st.session_state.email})

if user_profile:
    # --- Personal Details ---
    st.header("📌 Personal Details")
    st.write(f"**Full Name:** {user_profile.get('full_name', 'N/A')}")
    st.write(f"**Email:** {user_profile.get('email', 'N/A')}")
    st.write(f"**Phone:** {user_profile.get('phone', 'N/A')}")
    st.write(f"**Address:** {user_profile.get('address', 'N/A')}")
    st.write(f"**City:** {user_profile.get('city', 'N/A')}")
    st.write(f"**State:** {user_profile.get('state', 'N/A')}")
    st.write(f"**Pin Code:** {user_profile.get('pincode', 'N/A')}")
    st.write(f"**Location:** {user_profile.get('location', 'N/A')}")
    st.write(f"**LinkedIn:** [{user_profile.get('linkedin', 'N/A')}]({user_profile.get('linkedin', '#')})")
    st.write(f"**GitHub:** [{user_profile.get('github', 'N/A')}]({user_profile.get('github', '#')})")
    st.write(f"**Portfolio:** [{user_profile.get('portfolio', 'N/A')}]({user_profile.get('portfolio', '#')})")

    # --- Education ---
    st.header("🎓 Education")
    st.write(f"**Degree:** {user_profile.get('highest_degree', 'N/A')}")
    st.write(f"**University:** {user_profile.get('university', 'N/A')}")
    st.write(f"**Course:** {user_profile.get('course', 'N/A')}")
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
    
    # --- Career Preferences ---
    if "career_preferences" in user_profile:
        st.header("🌍 Career Preferences")
        st.write(f"**Remote Work Preference:** {user_profile['career_preferences'].get('remote_work', 'N/A')}")
        st.write(f"**Work Outside India Preference:** {user_profile['career_preferences'].get('work_outside_india', 'N/A')}")
        st.write(f"**Preferred Locations (India):** {', '.join(user_profile['career_preferences'].get('preferred_locations_india', []))}")
        st.write(f"**Preferred Locations (Outside India):** {', '.join(user_profile['career_preferences'].get('preferred_locations_abroad', []))}")
        st.write(f"**Preferred Profiles:** {', '.join(user_profile['career_preferences'].get('preferred_profiles', []))}")

    # --- Resume Download ---
    if user_profile.get("resume"):
        st.header("📄 Resume")
        st.download_button("Download Resume", user_profile["resume"], file_name="resume.pdf")
else:
    st.warning("Profile not found. Please complete your profile.")

st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False, "email": None, "full_name": None}))
st.sidebar.write(f"Welcome, {st.session_state.full_name}!")
