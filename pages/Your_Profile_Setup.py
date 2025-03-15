import streamlit as st
from pymongo import MongoClient
import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
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

st.title(f"Welcome, {st.session_state.full_name}! Please complete your job application profile.")

# --- Personal Details ---
st.header("Personal Details")
full_name = st.text_input("Full Name", st.session_state.full_name)
email = st.text_input("Email", st.session_state.email, disabled=True)
phone = st.text_input("Phone Number")
address = st.text_input("Address")
city = st.text_input("City")
state = st.text_input("State")
pincode = st.number_input("Pin Code")
linkedin = st.text_input("LinkedIn Profile URL")
github = st.text_input("GitHub Profile URL")
portfolio = st.text_input("Portfolio Website (if any)")
location = st.text_input("Current Location (City, Country)")

# --- Education Details ---
st.header("Education")
highest_degree = st.selectbox("Highest Degree", ["High School", "Diploma", "Bachelor's", "Master's", "PhD"])
university = st.text_input("University/College Name")
field_of_study = st.text_input("Field of Study (e.g., Computer Science, Electrical Engineering)")
graduation_year = st.number_input("Year of Graduation", min_value=1900, max_value=2100, step=1)
cgpa = st.number_input("CGPA (if applicable)", min_value=0.0, max_value=10.0, step=0.1)
certifications = st.text_area("Certifications (Separate by commas)")

# --- Work Experience ---
st.header("Work Experience")
has_experience = st.radio("Do you have prior work experience?", ["Yes", "No"])

work_experience = []
if has_experience == "Yes":
    num_experiences = st.number_input("How many previous jobs have you had?", min_value=1, max_value=10, step=1)
    for i in range(num_experiences):
        with st.expander(f"Work Experience {i+1}"):
            company_name = st.text_input(f"Company Name {i+1}")
            job_title = st.text_input(f"Job Title {i+1}")
            job_duration = st.text_input(f"Duration (e.g., Jan 2020 - Dec 2022) {i+1}")
            job_responsibilities = st.text_area(f"Job Responsibilities {i+1}")
            job_achievements = st.text_area(f"Key Achievements {i+1}")
            work_experience.append({
                "company": company_name,
                "title": job_title,
                "duration": job_duration,
                "responsibilities": job_responsibilities,
                "achievements": job_achievements
            })

# --- Skills ---
st.header("Skills")
technical_skills = st.text_area("Technical Skills (e.g., Python, Java, SQL, React) (Separate by commas)")
soft_skills = st.text_area("Soft Skills (e.g., Communication, Teamwork, Leadership) (Separate by commas)")

# --- Projects ---
st.header("Projects")
num_projects = st.number_input("How many projects have you worked on?", min_value=0, max_value=10, step=1)
projects = []
for i in range(num_projects):
    with st.expander(f"Project {i+1}"):
        project_title = st.text_input(f"Project Title {i+1}")
        project_description = st.text_area(f"Project Description {i+1}")
        project_technologies = st.text_input(f"Technologies Used {i+1} (Separate by commas)")
        project_github = st.text_input(f"GitHub/Portfolio Link {i+1}")
        projects.append({
            "title": project_title,
            "description": project_description,
            "technologies": project_technologies,
            "github": project_github
        })

# --- Internships & Training ---
st.header("Internships & Training")
num_internships = st.number_input("How many internships or training programs have you completed?", min_value=0, max_value=10, step=1)
internships = []
for i in range(num_internships):
    with st.expander(f"Internship/Training {i+1}"):
        intern_company = st.text_input(f"Company/Institute Name {i+1}")
        intern_role = st.text_input(f"Internship Role {i+1}")
        intern_duration = st.text_input(f"Duration (e.g., 3 months) {i+1}")
        intern_responsibilities = st.text_area(f"Key Learnings {i+1}")
        internships.append({
            "company": intern_company,
            "role": intern_role,
            "duration": intern_duration,
            "responsibilities": intern_responsibilities
        })

# --- Career Preferences ---
st.header("Career Preferences")
remote_work = st.radio("Would you prefer remote work?", ["Yes", "No"])
work_outside_india = st.radio("Would you consider working outside India?", ["Yes", "No", "Open to Both"])
preferred_locations_india = st.text_area("Top 5 Preferred Locations in India (Separate by commas)", placeholder="e.g., Delhi, Mumbai, Hyderabad, Pune, Gurugram")
#preferred_locations_abroad = st.text_area("Top 5 Preferred Locations Outside India (Separate by commas)")
preferred_profiles = st.text_area("Top 3 Preferred Profiles (Separate by commas)", placeholder="e.g., Python Developer, Data Scientist")
# Top 5 Preferred Locations (Outside India)
if work_outside_india in ["Yes", "Open to Both"]:
    preferred_locations_abroad = st.text_area(
        "Top 5 Preferred Locations (Outside India) (Separate by commas)",
        placeholder="e.g., New York, London, Sydney, Berlin, Toronto"
    )
else:
    st.text_area(
        "Top 5 Preferred Locations (Outside India) (Separate by commas)",
        disabled=True,
        value="N/A (Not applicable based on your preference)",
        placeholder="N/A (Not applicable based on your preference)"
    )
# --- Resume Upload ---
st.header("Upload Resume")
resume = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

# --- Store User Profile Data in MongoDB ---
def store_user_profile():
    resume_data = resume.read() if resume is not None else None
    profiles_collection.insert_one({
        "email": email,
        "full_name": full_name,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
        "portfolio": portfolio,
        "location": location,
        "highest_degree": highest_degree,
        "university": university,
        "field_of_study": field_of_study,
        "graduation_year": graduation_year,
        "cgpa": cgpa,
        "certifications": certifications.split(","),
        "work_experience": work_experience,
        "technical_skills": technical_skills.split(","),
        "soft_skills": soft_skills.split(","),
        "projects": projects,
        "internships": internships,
        "resume": resume_data,
        "career_preferences": {
            "remote_work": remote_work,
            "work_outside_india": work_outside_india,
            "preferred_locations_india": preferred_locations_india.split(","),
            "preferred_locations_abroad": preferred_locations_abroad.split(","),
            "preferred_profiles": preferred_profiles.split(",")
        }
    })
    return True

if st.button("Save Profile"):
    if resume:
        store_user_profile()
        st.success("Profile saved successfully!")
        st.switch_page("pages/Your_Dashboard.py")  # Redirect to dashboard

    else:
        st.error("Please upload your resume.")

st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False, "email": None, "full_name": None}))
